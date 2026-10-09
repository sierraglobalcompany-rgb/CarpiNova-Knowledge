from __future__ import annotations
import json
from pathlib import Path

_WARNING = '<!-- GENERATED from canonical content.json; do not edit manually -->\n\n'


def _render(records: list[dict], field: str) -> str:
    parts=[_WARNING]
    for rec in sorted(records,key=lambda r:r.get('id','')):
        parts.append(f"## {rec.get('id','UNKNOWN')}\n\n{rec.get(field,'').strip()}\n\n")
    return ''.join(parts).rstrip() + '\n'


def render_page_docs(page_dir: Path) -> None:
    page_dir=Path(page_dir)
    content_path=page_dir/'content.json'
    records=json.loads(content_path.read_text(encoding='utf-8')) if content_path.exists() else []
    mapping={'source.md':'source_transcription','normalized.md':'normalized_text','learning.md':'learning_text'}
    for filename,field in mapping.items():
        (page_dir/filename).write_text(_render(records,field),encoding='utf-8')
