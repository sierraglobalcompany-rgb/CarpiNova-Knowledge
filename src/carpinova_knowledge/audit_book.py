from __future__ import annotations

import gzip
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import fitz


_VECTOR_PAINT_RE = re.compile(rb'(?:(?<=\s)|^)(?:S|s|f\*?|F|B\*?|b\*?)(?=\s|$)')

def _fast_vector_operator_count(doc: fitz.Document, page: fitz.Page) -> int:
    # Fast, deterministic proxy for vector painting operations. It avoids the
    # expensive geometry expansion of get_drawings() on illustration-heavy pages.
    count = 0
    for xref in page.get_contents():
        try:
            stream = doc.xref_stream(xref)
        except Exception:
            continue
        count += len(_VECTOR_PAINT_RE.findall(stream))
    return count


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def audit_book(pdf_path: Path, book_id: str, output_dir: Path) -> dict[str, Any]:
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    audit_dir = output_dir / 'audits'
    audit_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    try:
        pages = []
        for idx, page in enumerate(doc):
            rect = page.rect
            blocks = page.get_text('blocks')
            text = page.get_text('text')
            pages.append({
                'pdf_page': idx + 1,
                'width': float(rect.width),
                'height': float(rect.height),
                'text_length': len(text),
                'text_blocks': [
                    {
                        'bbox': [float(v) for v in block[:4]],
                        'text': str(block[4]),
                        'block_no': int(block[5]),
                        'block_type': int(block[6]),
                    }
                    for block in blocks
                ],
                'embedded_image_count': len(page.get_images(full=True)),
                'vector_drawing_count': _fast_vector_operator_count(doc, page),
            })
        manifest = {
            'book_id': book_id,
            'source_filename': pdf_path.name,
            'source_sha256': _sha256(pdf_path),
            'pdf_page_count': doc.page_count,
        }
    finally:
        doc.close()

    audit = {'book_id': book_id, 'pages': pages}
    (output_dir / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    with gzip.open(audit_dir / 'raw-page-audit.json.gz', 'wt', encoding='utf-8', compresslevel=9) as fh:
        json.dump(audit, fh, ensure_ascii=False, separators=(',', ':'))
        fh.write('\n')
    return {'manifest': manifest, 'audit': audit}
