from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_027_hydraulic_piston_and_cylindrical_lock_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-027")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
