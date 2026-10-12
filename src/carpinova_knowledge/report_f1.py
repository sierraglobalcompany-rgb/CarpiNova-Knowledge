from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .report_batch import REQUIRED_PAGE_FILES

_SOURCE_GAP_RE = re.compile(r"source-gap-p(\d{4})\.md$")


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_source_gaps(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    result: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for path in sorted((root / "audits" / "f1").glob("source-gap-p*.md")):
        match = _SOURCE_GAP_RE.fullmatch(path.name)
        if match is None:
            continue
        pdf_page = int(match.group(1))
        page_dir = pages_dir / f"p{pdf_page:04d}"
        complete = page_dir.is_dir() and all(
            (page_dir / filename).exists() for filename in REQUIRED_PAGE_FILES
        )
        result.append(
            {
                "file": str(path),
                "pdf_page": pdf_page,
                "status": "RESOLVED_HISTORICAL" if complete else "OPEN",
            }
        )
    return result


def find_visual_findings(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    findings: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for page_dir in sorted(pages_dir.glob("p*")):
        if not page_dir.is_dir():
            continue
        figure_ids: set[str] = set()
        figures_dir = page_dir / "figures"
        if figures_dir.exists():
            for figure_path in sorted(figures_dir.glob("*.json")):
                figure = _load(figure_path)
                if figure.get("figure_id"):
                    figure_ids.add(str(figure["figure_id"]))

        inventory_path = page_dir / "visual-inventory.json"
        if not inventory_path.exists():
            continue
        inventory = _load(inventory_path)
        for visual in inventory.get("visuals", []):
            if visual.get("meaningful") is not True:
                continue
            figure_id = visual.get("figure_id")
            if visual.get("exclusion_reason"):
                continue
            if figure_id and str(figure_id) in figure_ids:
                continue
            findings.append(
                {
                    "code": "meaningful_visual_without_figure",
                    "file": str(inventory_path),
                    "inventory_id": visual.get("inventory_id"),
                }
            )
    return findings
