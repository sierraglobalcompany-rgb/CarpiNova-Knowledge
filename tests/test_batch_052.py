from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_052_adhesive_advertising_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-052")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
