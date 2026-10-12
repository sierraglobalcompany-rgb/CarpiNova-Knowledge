from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_057_separator_source_boundary_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-057")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1
