from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_024_hardware_introduction_and_hinges_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-024")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 8
