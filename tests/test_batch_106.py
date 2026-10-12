import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def _load(page: int, filename: str):
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_106_final_printed_page_and_back_cover_are_visually_grounded() -> None:
    report = build_batch_report(ROOT, "batch-106")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 1,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    p0294 = _load(294, "content.json")
    assert p0294 == []
    p0294_visuals = _load(294, "visual-inventory.json")
    assert p0294_visuals["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in p0294_visuals["visuals"])

    p0295 = _load(295, "content.json")
    assert len(p0295) == 1
    assert p0295[0]["content_type"] == "reference"
    assert p0295[0]["source_transcription"] == "Hágalo en casa"
    assert p0295[0]["source"]["printed_page"] is None
    assert p0295[0]["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    p0295_visuals = _load(295, "visual-inventory.json")
    assert p0295_visuals["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in p0295_visuals["visuals"])
