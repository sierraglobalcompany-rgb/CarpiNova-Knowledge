from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping
from typing import Any

from .ids import page_id

_PAGE_NUMBER = re.compile(r"^\s*(\d{1,4})\s*$")


def _candidate(page: Mapping[str, Any]) -> int | None:
    height = float(page.get("height_pt", 0.0) or 0.0)
    if height <= 0:
        return None
    values: list[int] = []
    for block in page.get("text_blocks", []):
        text = str(block.get("text", ""))
        bbox = block.get("bbox") or []
        if len(bbox) != 4:
            continue
        y0 = float(bbox[1])
        if y0 < height * 0.85:
            continue
        match = _PAGE_NUMBER.fullmatch(text)
        if match:
            values.append(int(match.group(1)))
    unique = sorted(set(values))
    return unique[0] if len(unique) == 1 else None


def build_page_map(
    audit: Mapping[str, Any], overrides: Mapping[int | str, int | None]
) -> dict[str, Any]:
    book_id = str(audit["book_id"])
    normalized_overrides = {int(key): value for key, value in overrides.items()}
    candidates = {int(page["pdf_page"]): _candidate(page) for page in audit["pages"]}
    counts = Counter(value for value in candidates.values() if value is not None)

    entries: list[dict[str, Any]] = []
    for page in audit["pages"]:
        pdf_page = int(page["pdf_page"])
        candidate = candidates[pdf_page]
        if pdf_page in normalized_overrides:
            printed = normalized_overrides[pdf_page]
            status = "not_printed" if printed is None else "verified"
        else:
            printed = candidate
            if candidate is None or counts[candidate] > 1:
                status = "unresolved"
            else:
                status = "candidate"
        entries.append(
            {
                "page_id": page_id(book_id, pdf_page),
                "book_id": book_id,
                "pdf_page": pdf_page,
                "printed_page": printed,
                "mapping_status": status,
            }
        )
    return {"book_id": book_id, "pages": entries}
