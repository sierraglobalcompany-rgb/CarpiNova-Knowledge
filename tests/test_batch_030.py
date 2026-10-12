from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_030_blank_transition_pages_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-030")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
    assert report["counts"]["content"] == 0
    assert report["counts"]["figures"] == 0
    assert report["counts"]["measurements"] == 0
    assert report["counts"]["rules"] == 0
