from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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
        batch = _load(path)
        if path.stem.lower() == wanted or str(batch.get("batch_id", "")).lower() == wanted:
            return batch
    raise ValueError(f"batch not found: {batch_id}")


def _page_dirs(root: Path, batch: dict[str, Any], findings: list[dict[str, Any]]) -> list[Path]:
    book_id = str(batch["book_id"])
    base = root / "books" / book_id / "pages"
    if batch.get("pdf_pages"):
        return [base / f"p{int(page):04d}" for page in batch["pdf_pages"]]

    page_map = _load(root / "books" / book_id / "page-map.json")
    by_printed: dict[int, list[dict[str, Any]]] = {}
    for page in page_map.get("pages", []):
        if page.get("printed_page") is not None:
            by_printed.setdefault(int(page["printed_page"]), []).append(page)

    result: list[Path] = []
    for printed in batch.get("printed_pages", []):
        verified = [
            page
            for page in by_printed.get(int(printed), [])
            if page.get("mapping_status") == "verified"
        ]
        if len(verified) != 1:
            findings.append(
                {
                    "code": "ambiguous_page_mapping",
                    "message": f"printed page {printed} does not have exactly one verified mapping",
                }
            )
            continue
        result.append(base / f"p{int(verified[0]['pdf_page']):04d}")
    return result


def build_batch_report(root: Path, batch_id: str) -> dict[str, Any]:
    root = Path(root)
    batch = _find_batch(root, batch_id)
    findings: list[dict[str, Any]] = []
    page_dirs = _page_dirs(root, batch, findings)

    validation = validate_repository(root)
    if not validation["valid"]:
        findings.append(
            {
                "code": "validation_error",
                "message": f"repository validator returned {validation['error_count']} errors",
            }
        )

    content_count = 0
    figure_count = 0
    measurement_count = 0
    rule_count = 0

    for page_dir in page_dirs:
        for filename in REQUIRED_PAGE_FILES:
            path = page_dir / filename
            if not path.exists():
                findings.append(
                    {
                        "code": "missing_required_page_file",
                        "message": f"{filename} is missing",
                        "file": str(path),
                    }
                )

        if (page_dir / "content.json").exists():
            content_count += len(_load(page_dir / "content.json"))

        if (page_dir / "measurements.json").exists():
            measurements = _load(page_dir / "measurements.json")
            measurement_count += len(measurements)
            for measurement in measurements:
                source = measurement.get("source")
                if not isinstance(source, dict) or not isinstance(source.get("region"), dict):
                    findings.append(
                        {
                            "code": "measurement_source_missing",
                            "message": "technical measurement lacks source location",
                            "object_id": measurement.get("measurement_id"),
                        }
                    )

        if (page_dir / "rules.json").exists():
            rule_count += len(_load(page_dir / "rules.json"))

        figures_dir = page_dir / "figures"
        figure_ids: set[str] = set()
        if figures_dir.exists():
            for figure_path in sorted(figures_dir.glob("*.json")):
                figure = _load(figure_path)
                figure_count += 1
                if figure.get("figure_id"):
                    figure_ids.add(str(figure["figure_id"]))

        inventory_path = page_dir / "visual-inventory.json"
        if inventory_path.exists():
            inventory = _load(inventory_path)
            for visual in inventory.get("visuals", []):
                if visual.get("meaningful") is not True:
                    continue
                figure_id = visual.get("figure_id")
                excluded = bool(visual.get("exclusion_reason"))
                if not excluded and (not figure_id or str(figure_id) not in figure_ids):
                    findings.append(
                        {
                            "code": "meaningful_visual_without_figure",
                            "message": "meaningful visual has no FigureSpec or exclusion reason",
                            "file": str(inventory_path),
                        }
                    )

    return {
        "batch_id": batch["batch_id"],
        "book_id": batch["book_id"],
        "result": "GO" if not findings else "NO_GO",
        "counts": {
            "pages": len(page_dirs),
            "content": content_count,
            "figures": figure_count,
            "measurements": measurement_count,
            "rules": rule_count,
        },
        "findings": findings,
    }


def render_batch_report(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "# CarpiNova Knowledge — Auditoría de lote",
        "",
        f"**Resultado: {report['result']}**",
        "",
        f"- Lote: `{report['batch_id']}`",
        f"- Libro: `{report['book_id']}`",
        f"- Páginas: {counts['pages']}",
        f"- Contenidos: {counts['content']}",
        f"- Figuras: {counts['figures']}",
        f"- Medidas: {counts['measurements']}",
        f"- Reglas: {counts['rules']}",
        "",
        "## Hallazgos",
        "",
    ]
    if report["findings"]:
        lines.extend(
            f"- **{finding['code']}**: {finding['message']}" for finding in report["findings"]
        )
    else:
        lines.append("- Sin hallazgos bloqueantes.")
    return "\n".join(lines).rstrip() + "\n"
