from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_055_cortecloud_summary_and_measurement_intro_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-055")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
