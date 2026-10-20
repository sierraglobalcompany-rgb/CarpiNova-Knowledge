"""MVP5 Paso 5 guided curriculum: source-backed links, no duplicate carpentry truth."""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BOOK_PAGES = ROOT / "books" / "cpnc-2025" / "pages"
MODULE_FILES = (
    ("01-cotizar-y-preparar-visita.json", 7),
    ("02-organizar-la-produccion.json", 5),
    ("03-entrega-calidad-y-posventa.json", 5),
    ("04-presupuesto-y-analisis-de-costos.json", 3),
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(("filename", "expected_steps"), MODULE_FILES)
def test_paso5_lesson_uses_only_canonical_content_and_renderable_figures(
    filename: str, expected_steps: int,
) -> None:
    lesson = _load(ROOT / "lessons" / "paso5" / filename)
    assert len(lesson["steps"]) == expected_steps
    assert [step["order"] for step in lesson["steps"]] == list(range(1, expected_steps + 1))
    all_step_content = [cid for step in lesson["steps"] for cid in step["content_ids"]]
    assert len(all_step_content) == len(set(all_step_content))
    assert lesson["source_content_ids"] == all_step_content
    for cid in all_step_content:
        match = re.fullmatch(r"CONTENT-CPNC-2025-P(\d{4})-(\d{3})", cid)
        assert match is not None, cid
        page = int(match.group(1))
        assert 235 <= page <= 270
        content = _load(BOOK_PAGES / f"p{page:04d}" / "content.json")
        assert any(record["content_id"] == cid for record in content), cid
    for step in lesson["steps"]:
        for fid in step.get("figure_ids", []):
            match = re.fullmatch(r"FIG-CPNC-2025-P(\d{4})-(\d{3})", fid)
            assert match is not None, fid
            page, number = (int(x) for x in match.groups())
            assert any(f"-P{page:04d}-" in cid for cid in step["content_ids"])
            figure = _load(
                BOOK_PAGES / f"p{page:04d}" / "figures" / f"fig-{number:03d}.json"
            )
            assert figure["figure_id"] == fid
            assert figure["reconstruction"].get("render_contract") == "normalized-2d-v1"


def test_paso5_route_has_four_distinct_modules_and_preserves_dual_p0270_content() -> None:
    lessons = [_load(ROOT / "lessons" / "paso5" / filename) for filename, _ in MODULE_FILES]
    assert len({lesson["lesson_id"] for lesson in lessons}) == 4
    assert [lesson["lesson_id"] for lesson in lessons] == sorted(
        lesson["lesson_id"] for lesson in lessons
    )
    assert sum(len(lesson["steps"]) for lesson in lessons) == 20
    assert lessons[-1]["steps"][-1]["content_ids"] == [
        "CONTENT-CPNC-2025-P0270-001",
        "CONTENT-CPNC-2025-P0270-002",
    ]
