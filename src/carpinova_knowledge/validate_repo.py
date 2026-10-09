from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .ids import page_id as canonical_page_id
from .render_docs import _render
from .schema_loader import validate_instance


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _error(errors: list[dict[str, Any]], code: str, path: Path, object_id: str | None, message: str, field: str | None = None) -> None:
    item: dict[str, Any] = {"code": code, "file": str(path), "message": message}
    if object_id:
        item["object_id"] = object_id
    if field:
        item["field"] = field
    errors.append(item)


def _source_bounds_ok(source: dict[str, Any]) -> bool:
    region = source.get("region") or {}
    try:
        x = float(region["x"]); y = float(region["y"])
        w = float(region["width"]); h = float(region["height"])
    except (KeyError, TypeError, ValueError):
        return False
    return 0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1 and x + w <= 1 and y + h <= 1


def _iter_sources(kind: str, record: dict[str, Any]) -> Iterable[dict[str, Any]]:
    if kind in {"content", "figure", "measurement"} and isinstance(record.get("source"), dict):
        yield record["source"]
    if kind == "rule":
        for source in record.get("sources", []):
            if isinstance(source, dict):
                yield source


def validate_repository(root: Path) -> dict[str, Any]:
    root = Path(root)
    errors: list[dict[str, Any]] = []
    ids: dict[str, Path] = {}
    refs: list[tuple[str, Path, str | None, str]] = []

    page_maps: dict[str, dict[int, dict[str, Any]]] = {}
    for path in root.glob("books/*/page-map.json"):
        data = _load(path)
        book_id = str(data.get("book_id", path.parent.name))
        pages = data.get("pages", [])
        page_maps[book_id] = {int(p["pdf_page"]): p for p in pages}
        verified_printed: dict[int, list[dict[str, Any]]] = {}
        for page in pages:
            if page.get("mapping_status") == "verified" and page.get("printed_page") is not None:
                verified_printed.setdefault(int(page["printed_page"]), []).append(page)
        for printed_page, matches in verified_printed.items():
            if len(matches) > 1:
                _error(
                    errors,
                    "duplicate_verified_printed_page",
                    path,
                    None,
                    f"printed page {printed_page} has {len(matches)} verified physical mappings",
                )

    for page_dir in sorted(root.glob("books/*/pages/p*")):
        if not page_dir.is_dir():
            continue
        page_path = page_dir / "page.json"
        if not page_path.exists():
            _error(errors, "missing_page_record", page_dir, None, "page.json is required")
            continue
        page = _load(page_path)
        pid = page.get("page_id")
        for message in validate_instance("page", page):
            _error(errors, "schema_error", page_path, pid, message)
        try:
            expected_pid = canonical_page_id(str(page["book_id"]), int(page["pdf_page"]))
            if pid != expected_pid:
                _error(errors, "page_identity_mismatch", page_path, pid, f"expected {expected_pid}")
        except Exception as exc:
            _error(errors, "page_identity_mismatch", page_path, pid, str(exc))

        if pid in ids:
            _error(errors, "duplicate_id", page_path, pid, f"already defined in {ids[pid]}")
        elif pid:
            ids[pid] = page_path

        book_map = page_maps.get(str(page.get("book_id")), {})
        mapped = book_map.get(int(page.get("pdf_page", 0) or 0))
        if mapped is not None:
            for key in ("page_id", "printed_page", "mapping_status"):
                if mapped.get(key) != page.get(key):
                    _error(errors, "page_map_mismatch", page_path, pid, f"{key} differs from page-map", key)

        groups = [
            ("content", page_dir / "content.json", "content"),
            ("measurement", page_dir / "measurements.json", "measurement"),
            ("rule", page_dir / "rules.json", "rule"),
        ]
        records_by_kind: dict[str, list[dict[str, Any]]] = {}
        for kind, path, schema in groups:
            if not path.exists():
                _error(errors, "missing_required_file", path, pid, f"{path.name} is required")
                records_by_kind[kind] = []
                continue
            records = _load(path)
            if not isinstance(records, list):
                _error(errors, "schema_error", path, pid, "top-level value must be a list")
                records = []
            records_by_kind[kind] = records
            id_field = {"content": "content_id", "measurement": "measurement_id", "rule": "rule_id"}[kind]
            for record in records:
                oid = record.get(id_field)
                for message in validate_instance(schema, record):
                    _error(errors, "schema_error", path, oid, message)
                if oid in ids:
                    _error(errors, "duplicate_id", path, oid, f"already defined in {ids[oid]}")
                elif oid:
                    ids[oid] = path
                if record.get("page_id") != pid:
                    _error(errors, "page_identity_mismatch", path, oid, "record page_id differs from owning page")
                for source in _iter_sources(kind, record):
                    if source.get("pdf_page") != page.get("pdf_page") or source.get("book_id") != page.get("book_id"):
                        _error(errors, "source_page_mismatch", path, oid, "source does not point to owning page")
                    if not _source_bounds_ok(source):
                        _error(errors, "source_region_out_of_bounds", path, oid, "source region must fit within [0,1] page bounds")
                if kind == "content":
                    for ref in record.get("derived_from_content_ids", []):
                        refs.append((ref, path, oid, "derived_from_content_ids"))
                if kind == "measurement" and record.get("status") == "VALIDATED" and not record.get("visual_verification"):
                    _error(errors, "measurement_visual_verification_required", path, oid, "VALIDATED technical measurement requires visual verification evidence")

        figures_dir = page_dir / "figures"
        if figures_dir.exists():
            for path in sorted(figures_dir.glob("*.json")):
                record = _load(path)
                oid = record.get("figure_id")
                for message in validate_instance("figure", record):
                    _error(errors, "schema_error", path, oid, message)
                if oid in ids:
                    _error(errors, "duplicate_id", path, oid, f"already defined in {ids[oid]}")
                elif oid:
                    ids[oid] = path
                if record.get("page_id") != pid:
                    _error(errors, "page_identity_mismatch", path, oid, "figure page_id differs from owning page")
                for source in _iter_sources("figure", record):
                    if source.get("pdf_page") != page.get("pdf_page") or source.get("book_id") != page.get("book_id"):
                        _error(errors, "source_page_mismatch", path, oid, "source does not point to owning page")
                    if not _source_bounds_ok(source):
                        _error(errors, "source_region_out_of_bounds", path, oid, "source region must fit within [0,1] page bounds")
                reconstruction = record.get("reconstruction") or {}
                if reconstruction.get("deterministic_required") and reconstruction.get("preferred_renderer") == "image" and reconstruction.get("generative_image_allowed"):
                    _error(errors, "deterministic_figure_generative_only", path, oid, "deterministic figure cannot rely only on generative image rendering")
                for ref in record.get("measurements", []):
                    refs.append((ref, path, oid, "measurements"))

        content_records = records_by_kind.get("content", [])
        generated = {
            "source.md": _render(content_records, "source_transcription", "Source transcription"),
            "normalized.md": _render(content_records, "normalized_text", "Normalized text"),
            "learning.md": _render(content_records, "learning_text", "Learning text"),
        }
        for filename, expected in generated.items():
            path = page_dir / filename
            actual = path.read_text(encoding="utf-8") if path.exists() else None
            if actual != expected:
                _error(errors, "stale_generated_markdown", path, pid, "generated Markdown does not match canonical content.json")

    for path in sorted(root.glob("lessons/**/*.json")):
        lesson = _load(path)
        oid = lesson.get("lesson_id")
        for message in validate_instance("lesson", lesson):
            _error(errors, "schema_error", path, oid, message)
        if oid in ids:
            _error(errors, "duplicate_id", path, oid, f"already defined in {ids[oid]}")
        elif oid:
            ids[oid] = path
        for ref in lesson.get("source_content_ids", []):
            refs.append((ref, path, oid, "source_content_ids"))
        for step in lesson.get("steps", []):
            for ref in step.get("content_ids", []):
                refs.append((ref, path, oid, "steps.content_ids"))
            for ref in step.get("figure_ids", []):
                refs.append((ref, path, oid, "steps.figure_ids"))

    for ref, path, oid, field in refs:
        if ref not in ids:
            _error(errors, "unresolved_reference", path, oid, f"reference {ref} does not resolve", field)

    for index_path in root.glob("books/*/index.json"):
        index = _load(index_path)
        book_id = str(index.get("book_id", index_path.parent.name))
        mapped_pages = set(page_maps.get(book_id, {}))
        for section in index.get("sections", []):
            pr = section.get("physical_range") or {}
            start, end = pr.get("start"), pr.get("end")
            if not isinstance(start, int) or not isinstance(end, int) or start > end or start not in mapped_pages or end not in mapped_pages:
                _error(errors, "index_range_invalid", index_path, section.get("section_id"), "physical range is invalid or outside page map")

    return {"valid": not errors, "error_count": len(errors), "errors": errors}
