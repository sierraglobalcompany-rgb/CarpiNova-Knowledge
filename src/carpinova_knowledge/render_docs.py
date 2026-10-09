from __future__ import annotations

import json
from pathlib import Path

GENERATED_WARNING = "<!-- GENERATED FROM content.json; DO NOT EDIT DIRECTLY -->"


def _render(records: list[dict], field: str, title: str) -> str:
    lines = [GENERATED_WARNING, "", f"# {title}", ""]
    for record in sorted(records, key=lambda item: item.get("content_id", "")):
        cid = record.get("content_id", "UNKNOWN")
        lines.extend([f"## {cid}", "", str(record.get(field, "")), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_page_docs(page_dir: Path) -> None:
    page_dir = Path(page_dir)
    records = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise TypeError("content.json must contain a list of ContentSpec records")
    outputs = {
        "source.md": ("source_transcription", "Source transcription"),
        "normalized.md": ("normalized_text", "Normalized text"),
        "learning.md": ("learning_text", "Learning text"),
    }
    for filename, (field, title) in outputs.items():
        (page_dir / filename).write_text(_render(records, field, title), encoding="utf-8")
