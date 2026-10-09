from __future__ import annotations

import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from .build_dist import build_distribution
from .validate_repo import validate_repository

REQUIRED_PAGE_FILES = (
    "page.json",
    "content.json",
    "measurements.json",
    "rules.json",
    "source.md",
    "normalized.md",
    "learning.md",
    "visual-inventory.json",
)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_batch(root: Path, batch_id: str) -> dict[str, Any]:
    wanted = batch_id.lower()
    for path in sorted(root.glob("books/*/batches/*.json")):
        record = _load(path)
        if path.stem.lower() == wanted or str(record.get("batch_id", "")).lower() == wanted:
            return record
        if wanted.startswith("batch-") and str(record.get("batch_id", "")).lower() == wanted:
            return record
    raise ValueError(f"batch not found: {batch_id}")


def _finding(findings: list[dict[str, Any]], code: str, message: str, **extra: Any) -> None:
    item = {"code": code, "message": message}
    item.update(extra)
    findings.append(item)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _distribution_fresh(root: Path, batch_id: str, findings: list[dict[str, Any]]) -> None:
    actual = root / "dist" / "pilot"
    if not actual.exists():
        _finding(findings, "distribution_missing", "dist/pilot is missing")
        return
    try:
        with tempfile.TemporaryDirectory() as td:
            expected = Path(td) / "dist"
            build_distribution(root, batch_id, expected)
            for name in ("knowledge.bundle.json", "figures.bundle.json", "lessons.bundle.json", "manifest.json"):
                if not (actual / name).exists() or (actual / name).read_bytes() != (expected / name).read_bytes():
                    _finding(findings, "distribution_stale", f"{name} does not match current canonical knowledge", file=str(actual / name))
    except ValueError as exc:
        _finding(findings, "distribution_unverifiable", str(exc))


def build_pilot_report(root: Path, batch_id: str) -> dict[str, Any]:
    root = Path(root)
    findings: list[dict[str, Any]] = []
    batch = _find_batch(root, batch_id)
    book_id = str(batch["book_id"])

    page_map_path = root / "books" / book_id / "page-map.json"
    page_map = _load(page_map_path)
    by_printed: dict[int, list[dict[str, Any]]] = {}
    for item in page_map.get("pages", []):
        if item.get("printed_page") is not None:
            by_printed.setdefault(int(item["printed_page"]), []).append(item)

    page_dirs: list[Path] = []
    for printed in batch["printed_pages"]:
        candidates = by_printed.get(int(printed), [])
        verified = [item for item in candidates if item.get("mapping_status") == "verified"]
        if len(verified) != 1:
            _finding(findings, "ambiguous_page_mapping", f"printed page {printed} does not have exactly one verified physical page", printed_page=printed)
            continue
        page_dirs.append(root / "books" / book_id / "pages" / f"p{int(verified[0]['pdf_page']):04d}")

    validation = validate_repository(root)
    if not validation["valid"]:
        _finding(findings, "validation_error", f"repository validator returned {validation['error_count']} errors", errors=validation["errors"])

    all_content: list[dict[str, Any]] = []
    all_measurements: list[dict[str, Any]] = []
    all_rules: list[dict[str, Any]] = []
    all_figures: list[dict[str, Any]] = []
    figure_paths: dict[str, Path] = {}

    for page_dir in page_dirs:
        for filename in REQUIRED_PAGE_FILES:
            if not (page_dir / filename).exists():
                _finding(findings, "missing_required_page_file", f"{filename} is missing", file=str(page_dir / filename))

        if (page_dir / "content.json").exists():
            all_content.extend(_load(page_dir / "content.json"))
        if (page_dir / "measurements.json").exists():
            records = _load(page_dir / "measurements.json")
            all_measurements.extend(records)
            for record in records:
                source = record.get("source")
                if not isinstance(source, dict) or not isinstance(source.get("region"), dict):
                    _finding(findings, "measurement_source_missing", "technical measurement lacks source location", object_id=record.get("measurement_id"))
        if (page_dir / "rules.json").exists():
            all_rules.extend(_load(page_dir / "rules.json"))

        for fig_path in sorted((page_dir / "figures").glob("*.json")) if (page_dir / "figures").exists() else []:
            figure = _load(fig_path)
            all_figures.append(figure)
            if figure.get("figure_id"):
                figure_paths[str(figure["figure_id"])] = fig_path

        inventory_path = page_dir / "visual-inventory.json"
        if inventory_path.exists():
            inventory = _load(inventory_path)
            for visual in inventory.get("visuals", []):
                if visual.get("meaningful") is True:
                    figure_id = visual.get("figure_id")
                    if not figure_id or figure_id not in figure_paths:
                        _finding(findings, "meaningful_visual_without_figure", "meaningful visual has no resolvable FigureSpec", file=str(inventory_path), inventory_id=visual.get("inventory_id"), figure_id=figure_id)

    measurement_ids = {str(item.get("measurement_id")) for item in all_measurements if item.get("measurement_id")}
    reconstruction_rows: list[dict[str, Any]] = []
    for figure in all_figures:
        fid = str(figure.get("figure_id", ""))
        issues: list[str] = []
        entities = figure.get("entities") or []
        entity_ids = {str(entity.get("id")) for entity in entities if entity.get("id")}
        if not entities:
            issues.append("no important entities recorded")
        for entity in entities:
            precision = (entity.get("geometry") or {}).get("precision")
            if precision not in {"exact", "approximate", "unknown"}:
                issues.append(f"entity {entity.get('id')} lacks explicit geometry precision")
        reconstruction = figure.get("reconstruction") or {}
        if not reconstruction.get("preferred_renderer"):
            issues.append("preferred reconstruction mode missing")
        for relationship in figure.get("relationships", []):
            for key in ("from", "to"):
                ref = relationship.get(key)
                if ref and ref not in entity_ids:
                    issues.append(f"relationship {key}={ref} does not bind to an entity")
        for annotation in figure.get("annotations", []):
            entity_ref = annotation.get("entity_id")
            measurement_ref = annotation.get("measurement_id")
            if entity_ref and entity_ref not in entity_ids:
                issues.append(f"annotation entity {entity_ref} does not resolve")
            if measurement_ref and measurement_ref not in measurement_ids:
                issues.append(f"annotation measurement {measurement_ref} does not resolve")
            if not entity_ref and not measurement_ref:
                issues.append("annotation is not bound to an entity or measurement")
        if figure.get("type") in {"technical_diagram", "dimensioned_drawing", "process_diagram", "assembly_sequence", "table"} and not figure.get("educational_sequence"):
            issues.append("technical/process figure lacks educational sequence")
        row = {"figure_id": fid, "pass": not issues, "issues": issues}
        reconstruction_rows.append(row)
        for issue in issues:
            _finding(findings, "figure_reconstruction_gap", issue, figure_id=fid, file=str(figure_paths.get(fid, "")))

    lessons = [_load(path) for path in sorted(root.glob("lessons/**/*.json"))]
    figure_types = Counter(str(item.get("type")) for item in all_figures)
    measurement_statuses = Counter(str(item.get("status")) for item in all_measurements)
    content_types = Counter(str(item.get("content_type")) for item in all_content)
    warnings_conflicts = sum(1 for item in all_measurements if item.get("status") in {"CONFLICT", "REJECTED"})

    if validation["valid"]:
        _distribution_fresh(root, batch_id, findings)

    counts = {
        "pages": len(page_dirs),
        "content": len(all_content),
        "content_by_type": dict(sorted(content_types.items())),
        "figures_total": len(all_figures),
        "figures_by_type": dict(sorted(figure_types.items())),
        "measurements": len(all_measurements),
        "measurements_by_status": dict(sorted(measurement_statuses.items())),
        "rule_candidates": sum(1 for item in all_rules if item.get("status") == "CANDIDATE"),
        "rule_reviewed": sum(1 for item in all_rules if item.get("status") == "REVIEWED"),
        "concepts": content_types.get("concept", 0),
        "lessons": len(lessons),
        "warnings_conflicts": warnings_conflicts,
        "validation_errors": validation["error_count"],
    }
    report = {
        "batch_id": batch["batch_id"],
        "book_id": book_id,
        "result": "GO" if not findings else "NO_GO",
        "counts": counts,
        "reconstruction_audit": {"all_pass": all(row["pass"] for row in reconstruction_rows), "figures": reconstruction_rows},
        "findings": findings,
    }
    return report


def render_pilot_report(report: dict[str, Any]) -> str:
    c = report["counts"]
    lines = [
        "# CarpiNova Knowledge F0 — Auditoría de aceptación del piloto",
        "",
        f"**Resultado: {report['result']}**",
        "",
        f"- Lote: `{report['batch_id']}`",
        f"- Libro: `{report['book_id']}`",
        f"- Páginas: {c['pages']}",
        f"- Contenidos: {c['content']}",
        f"- Figuras: {c['figures_total']}",
        f"- Medidas: {c['measurements']}",
        f"- Reglas candidatas: {c['rule_candidates']}",
        f"- Lecciones: {c['lessons']}",
        f"- Errores del validador: {c['validation_errors']}",
        "",
        "## Figuras por tipo",
        "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in c["figures_by_type"].items())
    lines.extend(["", "## Medidas por estado", ""])
    lines.extend(f"- {name}: {count}" for name, count in c["measurements_by_status"].items())
    lines.extend(["", "## Auditoría de reconstrucción", ""])
    for item in report["reconstruction_audit"]["figures"]:
        state = "PASS" if item["pass"] else "FAIL"
        lines.append(f"- `{item['figure_id']}`: {state}")
        for issue in item["issues"]:
            lines.append(f"  - {issue}")
    lines.extend(["", "## Hallazgos", ""])
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(f"- **{finding['code']}**: {finding['message']}")
    else:
        lines.append("- Sin hallazgos bloqueantes.")
    return "\n".join(lines).rstrip() + "\n"
