from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_050_breakdown_optimization_edge_banding_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-050")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 3
    assert (ROOT / "audits" / "f1" / "source-gap-p0178.md").exists()
