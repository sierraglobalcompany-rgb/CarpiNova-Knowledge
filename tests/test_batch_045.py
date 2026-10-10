from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_045_handheld_circular_saw_source_boundary_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-045")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1
    assert (ROOT / "audits" / "f1" / "source-gap-p0160.md").exists()
