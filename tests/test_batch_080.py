from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_080_quoting_infographic_and_social_media_capture_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-080")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
