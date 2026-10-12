from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .report_batch import REQUIRED_PAGE_FILES


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _batch_pdf_pages(root: Path, book_id: str, batch: dict[str, Any]) -> list[int]:
    if batch.get("pdf_pages"):
        return [int(page) for page in batch["pdf_pages"]]

    page_map = _load(root / "books" / book_id / "page-map.json")
    by_printed: dict[int, list[dict[str, Any]]] = {}
    for page in page_map.get("pages", []):
        if page.get("printed_page") is not None:
            by_printed.setdefault(int(page["printed_page"]), []).append(page)

    result: list[int] = []
    for printed in batch.get("printed_pages", []):
        verified = [
            page
            for page in by_printed.get(int(printed), [])
            if page.get("mapping_status") == "verified"
        ]
        if len(verified) == 1:
            result.append(int(verified[0]["pdf_page"]))
    return result


def build_coverage_report(root: Path, book_id: str) -> dict[str, Any]:
    root = Path(root)
    book_dir = root / "books" / book_id
    manifest = _load(book_dir / "manifest.json")
    total_pages = int(manifest["pdf_page_count"])

    assignments: Counter[int] = Counter()
    for path in sorted((book_dir / "batches").glob("*.json")):
        batch = _load(path)
        if str(batch.get("book_id")) != book_id:
            continue
        assignments.update(_batch_pdf_pages(root, book_id, batch))

    complete: list[int] = []
    classified: list[int] = []
    pending: list[int] = []

    for pdf_page in range(1, total_pages + 1):
        page_dir = book_dir / "pages" / f"p{pdf_page:04d}"
        if not page_dir.exists():
            pending.append(pdf_page)
            continue
        if all((page_dir / filename).exists() for filename in REQUIRED_PAGE_FILES):
            complete.append(pdf_page)
        elif (page_dir / "page.json").exists():
            classified.append(pdf_page)
        else:
            pending.append(pdf_page)

    duplicate_batch_pages = sorted(page for page, count in assignments.items() if count > 1)
    assigned_pages = sorted(assignments)
    unassigned_pages = [page for page in range(1, total_pages + 1) if page not in assignments]

    return {
        "book_id": book_id,
        "total_pages": total_pages,
        "complete_pages": len(complete),
        "classified_pages": len(classified),
        "pending_pages": len(pending),
        "complete_pdf_pages": complete,
        "classified_pdf_pages": classified,
        "pending_pdf_pages": pending,
        "assigned_pages": len(assigned_pages),
        "unassigned_pages": len(unassigned_pages),
        "duplicate_batch_pages": duplicate_batch_pages,
        "complete": len(complete) == total_pages and not duplicate_batch_pages,
    }


def render_coverage_report(report: dict[str, Any]) -> str:
    total = report["total_pages"]
    complete = report["complete_pages"]
    percentage = (complete / total * 100) if total else 0.0
    lines = [
        "# CarpiNova Knowledge — Cobertura F1",
        "",
        f"- Libro: `{report['book_id']}`",
        f"- Páginas físicas: {total}",
        f"- Completas: {complete} ({percentage:.1f} %)",
        f"- Clasificadas parcialmente: {report['classified_pages']}",
        f"- Pendientes: {report['pending_pages']}",
        f"- Asignadas a lotes: {report['assigned_pages']}",
        f"- Sin asignar: {report['unassigned_pages']}",
        f"- Duplicadas entre lotes: {len(report['duplicate_batch_pages'])}",
        "",
    ]
    if report["duplicate_batch_pages"]:
        lines.append(
            "Duplicadas: " + ", ".join(str(page) for page in report["duplicate_batch_pages"])
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
