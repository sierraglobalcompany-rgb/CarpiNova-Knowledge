from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_032_closet_comparison_and_sd_simple_manual_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-032")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
