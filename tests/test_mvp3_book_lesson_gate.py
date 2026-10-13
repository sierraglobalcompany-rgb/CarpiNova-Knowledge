from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.build_dist import build_book_distribution


ROOT = Path(__file__).resolve().parents[1]
LESSON_ID = "LESSON-SLIDES-X-2X-PILOT"
LESSON_TITLE = "Calcular e instalar correderas con X y 2X"


def test_book_1_0_emits_guided_lesson_for_carpinova_pc_mvp3(tmp_path: Path) -> None:
    out = tmp_path / "book"

    manifest = build_book_distribution(ROOT, "cpnc-2025", out)
    bundle = json.loads((out / "lessons.bundle.json").read_text(encoding="utf-8"))
    lesson = next((item for item in bundle["lessons"] if item["lesson_id"] == LESSON_ID), None)

    assert manifest["knowledge_version"] == "1.0.0"
    assert manifest["book_id"] == "cpnc-2025"
    assert manifest["scope"] == "BOOK"
    assert lesson is not None
    assert lesson["title"] == LESSON_TITLE
    assert [step["order"] for step in lesson["steps"]] == [1, 2, 3, 4, 5]
    assert len(lesson["steps"]) == 5
