from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_046_installation_conclusion_source_boundaries_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-046")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1
    assert (ROOT / "audits" / "f1" / "source-gap-p0161.md").exists()
    assert (ROOT / "audits" / "f1" / "source-gap-p0162.md").exists()
    assert (ROOT / "audits" / "f1" / "source-gap-p0164.md").exists()
