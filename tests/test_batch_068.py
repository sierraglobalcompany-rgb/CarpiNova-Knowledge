from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_068_murphy_bed_external_dimensions_parts_and_cut_list_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-068")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
