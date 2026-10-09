from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_generic_batch_report_accepts_f0_pilot() -> None:
    report = build_batch_report(ROOT, "batch-000-pilot")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 8
