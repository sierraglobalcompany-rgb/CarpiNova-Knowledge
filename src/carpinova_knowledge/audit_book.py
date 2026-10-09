from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pymupdf


BookAudit = dict[str, Any]

_VECTOR_PAINT_OP = re.compile(rb"(?<!\S)(?:S|s|f\*?|F|B\*?|b\*?)(?!\S)")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _text_blocks(page: pymupdf.Page) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text, block_no, block_type = block[:7]
        blocks.append(
            {
                "bbox": [float(x0), float(y0), float(x1), float(y1)],
                "text": str(text),
                "block_no": int(block_no),
                "block_type": int(block_type),
            }
        )
    return blocks


def _vector_drawing_count(page: pymupdf.Page) -> int:
    content = page.read_contents() or b""
    return len(_VECTOR_PAINT_OP.findall(content))


def audit_book(pdf_path: Path, book_id: str, output_dir: Path) -> BookAudit:
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audits").mkdir(parents=True, exist_ok=True)

    source_sha256 = _sha256(pdf_path)
    pages: list[dict[str, Any]] = []
    with pymupdf.open(pdf_path) as doc:
        for index, page in enumerate(doc, start=1):
            blocks = _text_blocks(page)
            text_length = sum(len(block["text"]) for block in blocks)
            pages.append(
                {
                    "pdf_page": index,
                    "width_pt": float(page.rect.width),
                    "height_pt": float(page.rect.height),
                    "text_length": text_length,
                    "text_blocks": blocks,
                    "image_count": len(page.get_images(full=True)),
                    "vector_drawing_count": _vector_drawing_count(page),
                }
            )
        page_count = doc.page_count

    manifest = {
        "book_id": book_id,
        "source_filename": pdf_path.name,
        "source_sha256": source_sha256,
        "pdf_page_count": page_count,
    }
    audit = {"book_id": book_id, "pages": pages}

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "audits" / "raw-page-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {"manifest": manifest, "pages": pages}
