from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_092_closet_and_kitchen_bath_delivery_forms_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-092")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
