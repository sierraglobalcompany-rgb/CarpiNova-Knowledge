from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_025_telescopic_slides_and_omega_hinges_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-025")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
