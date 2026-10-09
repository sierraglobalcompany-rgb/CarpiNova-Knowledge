from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .validate_repo import validate_repository

SCHEMA_VERSION = "0.1.0"
KNOWLEDGE_VERSION = "0.1.0"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _stable_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _write_stable(path: Path, value: Any) -> str:
    data = _stable_bytes(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def _find_batch(root: Path, batch_id: str) -> tuple[Path, dict[str, Any]]:
    wanted = batch_id.strip().upper()
    if not wanted.startswith("BATCH-"):
        wanted = f"BATCH-{wanted.removeprefix('batch-').upper()}"
    for path in sorted(root.glob("books/*/batches/*.json")):
        record = _load(path)
        if str(record.get("batch_id", "")).upper() == wanted or path.stem.lower() == batch_id.lower():
            return path, record
    raise ValueError(f"batch not found: {batch_id}")


def _resolve_page_dirs(root: Path, batch: dict[str, Any]) -> list[Path]:
    book_id = str(batch["book_id"])
    page_map_path = root / "books" / book_id / "page-map.json"
    page_map = _load(page_map_path)
    by_printed: dict[int, list[dict[str, Any]]] = {}
    for item in page_map.get("pages", []):
        if item.get("printed_page") is not None and item.get("mapping_status") == "verified":
            by_printed.setdefault(int(item["printed_page"]), []).append(item)
    dirs: list[Path] = []
    for printed in batch["printed_pages"]:
        matches = by_printed.get(int(printed), [])
        if len(matches) != 1:
            raise ValueError(f"batch printed page {printed} is not unambiguously verified")
        mapped = matches[0]
        dirs.append(root / "books" / book_id / "pages" / f"p{int(mapped['pdf_page']):04d}")
    return dirs


def _collect_records(page_dirs: list[Path], filename: str, id_field: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for page_dir in page_dirs:
        path = page_dir / filename
        if not path.exists():
            continue
        value = _load(path)
        if isinstance(value, list):
            records.extend(value)
    return sorted(records, key=lambda item: str(item.get(id_field, "")))


def _collect_figures(page_dirs: list[Path]) -> list[dict[str, Any]]:
    figures: list[dict[str, Any]] = []
    for page_dir in page_dirs:
        for path in sorted((page_dir / "figures").glob("*.json")):
            figures.append(_load(path))
    return sorted(figures, key=lambda item: str(item.get("figure_id", "")))


def _collect_lessons(root: Path, content_ids: set[str], figure_ids: set[str]) -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    for path in sorted(root.glob("lessons/**/*.json")):
        lesson = _load(path)
        refs = set(lesson.get("source_content_ids", []))
        step_content = {ref for step in lesson.get("steps", []) for ref in step.get("content_ids", [])}
        step_figures = {ref for step in lesson.get("steps", []) for ref in step.get("figure_ids", [])}
        if refs | step_content <= content_ids and step_figures <= figure_ids:
            lessons.append(lesson)
    return sorted(lessons, key=lambda item: str(item.get("lesson_id", "")))


def build_distribution(root: Path, batch_id: str, out_dir: Path) -> dict[str, Any]:
    root = Path(root)
    out_dir = Path(out_dir)
    report = validate_repository(root)
    if not report["valid"]:
        raise ValueError(f"knowledge repository is invalid: {report['error_count']} errors")

    _, batch = _find_batch(root, batch_id)
    page_dirs = _resolve_page_dirs(root, batch)
    pages = sorted((_load(d / "page.json") for d in page_dirs), key=lambda item: item["page_id"])
    content = _collect_records(page_dirs, "content.json", "content_id")
    measurements = _collect_records(page_dirs, "measurements.json", "measurement_id")
    rules = _collect_records(page_dirs, "rules.json", "rule_id")
    figures = _collect_figures(page_dirs)
    lessons = _collect_lessons(root, {c["content_id"] for c in content}, {f["figure_id"] for f in figures})

    knowledge_bundle = {
        "schema_version": SCHEMA_VERSION,
        "knowledge_version": KNOWLEDGE_VERSION,
        "book_id": batch["book_id"],
        "batch_id": batch["batch_id"],
        "pages": pages,
        "content": content,
        "measurements": measurements,
        "rules": rules,
        "taxonomy": {},
    }
    figure_bundle = {
        "schema_version": SCHEMA_VERSION,
        "knowledge_version": KNOWLEDGE_VERSION,
        "book_id": batch["book_id"],
        "batch_id": batch["batch_id"],
        "figures": figures,
    }
    lesson_bundle = {
        "schema_version": SCHEMA_VERSION,
        "knowledge_version": KNOWLEDGE_VERSION,
        "book_id": batch["book_id"],
        "batch_id": batch["batch_id"],
        "lessons": lessons,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    hashes = {
        "knowledge.bundle.json": _write_stable(out_dir / "knowledge.bundle.json", knowledge_bundle),
        "figures.bundle.json": _write_stable(out_dir / "figures.bundle.json", figure_bundle),
        "lessons.bundle.json": _write_stable(out_dir / "lessons.bundle.json", lesson_bundle),
    }
    source_manifest = _load(root / "books" / str(batch["book_id"]) / "manifest.json")
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "knowledge_version": KNOWLEDGE_VERSION,
        "book_id": batch["book_id"],
        "batch_id": batch["batch_id"],
        "source_manifest_sha256": source_manifest["source_sha256"],
        "files": hashes,
        "counts": {
            "pages": len(pages),
            "content": len(content),
            "measurements": len(measurements),
            "rules": len(rules),
            "figures": len(figures),
            "lessons": len(lessons),
            "taxonomy_records": 0,
        },
    }
    _write_stable(out_dir / "manifest.json", manifest)
    return manifest
