from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_077_market_study_and_business_infographic_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-077")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
