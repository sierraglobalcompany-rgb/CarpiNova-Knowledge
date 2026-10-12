from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_109_recovers_exact_source_page_164() -> None:
    report = build_batch_report(ROOT, "batch-109")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1

    page_dir = ROOT / "books" / "cpnc-2025" / "pages" / "p0164"
    source = (page_dir / "source.md").read_text(encoding="utf-8")
    assert "LISTADO HERRAMIENTAS" in source
    assert "Brocas madera y lamina 1/8 3/16 3/8" in source
    assert "INSTALACIÓN" in source
    assert "Brocas  x 2" in source
    assert "Gafas seguridad" in source

    audit = (ROOT / "audits" / "f1" / "source-gap-p0164.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit
    assert "PENDING — SOURCE_IMAGE_UNAVAILABLE" not in audit


def test_batch_109_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] >= 281
    assert report["pending_pages"] <= 14
    assert 164 not in report["pending_pdf_pages"]
    assert report["duplicate_batch_pages"] == []
