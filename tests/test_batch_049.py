from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_049_separator_source_boundary_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-049")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1
    assert (ROOT / "audits" / "f1" / "source-gap-p0172.md").exists()
    assert (ROOT / "audits" / "f1" / "source-gap-p0173.md").exists()
    assert (ROOT / "audits" / "f1" / "source-gap-p0174.md").exists()
