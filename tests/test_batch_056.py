from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_056_measurement_reference_and_site_form_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-056")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
