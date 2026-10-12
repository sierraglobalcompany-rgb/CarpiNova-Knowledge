from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_048_product_reference_advertising_pages_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-048")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 4
