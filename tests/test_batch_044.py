from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_044_circular_saws_safety_and_cuts_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-044")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
