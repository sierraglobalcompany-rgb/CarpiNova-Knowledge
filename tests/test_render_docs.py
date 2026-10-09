from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_docs import GENERATED_WARNING, render_page_docs


def _content(cid: str, source: str, normalized: str, learning: str) -> dict:
    return {
        "content_id": cid,
        "source_transcription": source,
        "normalized_text": normalized,
        "learning_text": learning,
    }


def test_render_docs_are_generated_from_canonical_json_in_id_order(tmp_path: Path) -> None:
    content = [
        _content("CONTENT-CPNC-2025-P0110-002", "S2", "N2", "L2"),
        _content("CONTENT-CPNC-2025-P0110-001", "S1", "N1", "L1"),
    ]
    (tmp_path / "content.json").write_text(json.dumps(content), encoding="utf-8")

    render_page_docs(tmp_path)

    source = (tmp_path / "source.md").read_text(encoding="utf-8")
    normalized = (tmp_path / "normalized.md").read_text(encoding="utf-8")
    learning = (tmp_path / "learning.md").read_text(encoding="utf-8")
    assert GENERATED_WARNING in source
    assert source.index("S1") < source.index("S2")
    assert normalized.index("N1") < normalized.index("N2")
    assert learning.index("L1") < learning.index("L2")


def test_render_docs_recreates_edited_markdown_from_json(tmp_path: Path) -> None:
    content = [_content("CONTENT-CPNC-2025-P0110-001", "Source", "Normalized", "Learning")]
    (tmp_path / "content.json").write_text(json.dumps(content), encoding="utf-8")
    render_page_docs(tmp_path)
    (tmp_path / "learning.md").write_text("tampered", encoding="utf-8")
    render_page_docs(tmp_path)
    assert "tampered" not in (tmp_path / "learning.md").read_text(encoding="utf-8")
    assert "Learning" in (tmp_path / "learning.md").read_text(encoding="utf-8")
