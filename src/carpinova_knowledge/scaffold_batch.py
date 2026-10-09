from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .render_docs import render_page_docs


def _write_json_if_missing(path: Path, value: Any) -> None:
    if not path.exists():
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scaffold_batch(batch: dict[str, Any], page_map: dict[str, Any], root: Path) -> list[Path]:
    root = Path(root)
    pages_root = root / "books" / batch["book_id"] / "pages"
    pages_root.mkdir(parents=True, exist_ok=True)
    mapped: list[Path] = []

    for printed in batch["printed_pages"]:
        hits = [
            p
            for p in page_map["pages"]
            if p.get("printed_page") == printed and p.get("mapping_status") == "verified"
        ]
        if len(hits) != 1:
            raise ValueError(f"printed page {printed} lacks an unambiguous verified mapping")
        page = hits[0]
        page_dir = pages_root / f"p{int(page['pdf_page']):04d}"
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "figures").mkdir(exist_ok=True)
        _write_json_if_missing(page_dir / "page.json", page)
        _write_json_if_missing(page_dir / "content.json", [])
        _write_json_if_missing(page_dir / "measurements.json", [])
        _write_json_if_missing(page_dir / "rules.json", [])
        render_page_docs(page_dir)
        mapped.append(page_dir)
    return mapped
