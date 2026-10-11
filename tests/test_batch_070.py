from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_070_murphy_bed_cabinet_vertical_hardware_page_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-070")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1
