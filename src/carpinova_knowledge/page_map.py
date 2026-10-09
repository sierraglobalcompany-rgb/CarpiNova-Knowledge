from __future__ import annotations

import gzip
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

_PAGE_RE = re.compile(r'^\s*(\d{1,4})\s*$')


def _candidate(page: Mapping[str, Any]) -> int | None:
    height = float(page.get('height', 0) or 0)
    candidates: list[int] = []
    for block in page.get('text_blocks', []):
        bbox = block.get('bbox') or [0, 0, 0, 0]
        if height and float(bbox[1]) < height * 0.82:
            continue
        m = _PAGE_RE.match(str(block.get('text', '')).strip())
        if m:
            candidates.append(int(m.group(1)))
    return candidates[-1] if candidates else None


def build_page_map(audit: Mapping[str, Any], overrides: Mapping[int | str, int | None]) -> dict[str, Any]:
    normalized_overrides = {int(k): v for k, v in overrides.items()}
    raw_candidates = {int(p['pdf_page']): _candidate(p) for p in audit.get('pages', [])}
    counts = Counter(v for v in raw_candidates.values() if v is not None)
    result = []
    for page in audit.get('pages', []):
        pdf_page = int(page['pdf_page'])
        if pdf_page in normalized_overrides:
            printed = normalized_overrides[pdf_page]
            status = 'verified' if printed is not None else 'not_printed'
        else:
            printed = raw_candidates[pdf_page]
            if printed is None:
                status = 'unresolved'
            elif counts[printed] > 1:
                status = 'unresolved'
            else:
                status = 'candidate'
        result.append({'pdf_page': pdf_page, 'printed_page': printed, 'mapping_status': status})
    return {'pages': result}


def _read_json(path: Path) -> Any:
    path = Path(path)
    if path.suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8') as fh:
            return json.load(fh)
    return json.loads(path.read_text(encoding='utf-8'))


def write_page_map(audit_path: Path, overrides_path: Path, out_path: Path) -> dict[str, Any]:
    audit = _read_json(Path(audit_path))
    overrides = json.loads(Path(overrides_path).read_text(encoding='utf-8'))
    result = build_page_map(audit, overrides)
    Path(out_path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result
