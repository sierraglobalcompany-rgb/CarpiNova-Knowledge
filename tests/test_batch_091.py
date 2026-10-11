from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_091_delivery_checklist_intro_and_door_delivery_form_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-091")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
