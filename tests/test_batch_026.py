from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_026_lift_arms_and_installation_guides_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-026")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
