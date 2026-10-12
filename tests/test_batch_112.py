import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_112_recovers_exact_source_page_184() -> None:
    report = build_batch_report(ROOT, "batch-112")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 1,
        "content": 0,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    page_dir = ROOT / "books" / "cpnc-2025" / "pages" / "p0184"
    content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
    assert content == []

    visual = json.loads((page_dir / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual["visuals"])

    audit = (ROOT / "audits" / "f1" / "source-gap-p0184.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit
    assert "PENDING — SOURCE_IMAGE_UNAVAILABLE" not in audit


def test_batch_112_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] >= 286
    assert report["pending_pages"] <= 9
    assert 184 not in report["pending_pdf_pages"]
    assert report["duplicate_batch_pages"] == []
