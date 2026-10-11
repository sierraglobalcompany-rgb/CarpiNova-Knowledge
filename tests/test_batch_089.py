from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_089_closet_and_kitchen_checklist_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-089")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
