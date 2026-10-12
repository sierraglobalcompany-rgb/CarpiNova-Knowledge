from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_083_quotation_visit_infographic_and_measurement_register_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-083")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
