from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_067_murphy_bed_intro_tools_and_mechanism_parts_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-067")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
