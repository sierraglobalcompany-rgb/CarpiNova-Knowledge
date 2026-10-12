from pathlib import Path

from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_audit_pending_pdf_pages() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["pending_pdf_pages"] == []
