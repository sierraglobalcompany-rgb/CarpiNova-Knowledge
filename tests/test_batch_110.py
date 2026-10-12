import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_110_recovers_exact_source_pages_172_174() -> None:
    report = build_batch_report(ROOT, "batch-110")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 3,
        "content": 1,
        "figures": 1,
        "measurements": 0,
        "rules": 0,
    }

    for page in (172, 174):
        page_dir = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}"
        content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
        assert content == []

    page_173 = ROOT / "books" / "cpnc-2025" / "pages" / "p0173"
    source = (page_173 / "source.md").read_text(encoding="utf-8")
    assert "PASO 4" in source
    assert "DESPIECE" in source
    assert "OPTIMIZACIÓN" in source
    assert "HÁGALO EN CASA" in source
    assert (page_173 / "figures" / "fig-001.json").exists()

    for page in (172, 173, 174):
        audit = (ROOT / "audits" / "f1" / f"source-gap-p{page:04d}.md").read_text(
            encoding="utf-8"
        )
        assert "RESOLVED" in audit
        assert "PENDING — SOURCE_IMAGE_UNAVAILABLE" not in audit


def test_batch_110_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] >= 284
    assert report["pending_pages"] <= 11
    for page in (172, 173, 174):
        assert page not in report["pending_pdf_pages"]
    assert report["duplicate_batch_pages"] == []
