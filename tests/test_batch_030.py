from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_030_sliding_overview_and_closet_comparison_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-030")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
