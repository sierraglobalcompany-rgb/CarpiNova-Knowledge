from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pymupdf

from carpinova_knowledge.audit_book import audit_book


PPM_1X1 = b"P6\n1 1\n255\n\xff\x00\x00"


def _make_synthetic_pdf(path: Path) -> None:
    doc = pymupdf.open()
    p1 = doc.new_page(width=300, height=400)
    p1.insert_text((40, 50), "Page one text")

    p2 = doc.new_page(width=320, height=420)
    p2.insert_text((40, 50), "Page two with image")
    p2.insert_image(pymupdf.Rect(40, 80, 80, 120), stream=PPM_1X1)

    p3 = doc.new_page(width=340, height=440)
    p3.insert_text((40, 50), "Page three vector")
    p3.draw_line((40, 100), (240, 100), color=(0, 0, 0), width=2)
    doc.save(path)
    doc.close()


def test_audit_book_reports_objective_pdf_metadata(tmp_path: Path) -> None:
    pdf = tmp_path / "sample.pdf"
    _make_synthetic_pdf(pdf)
    out = tmp_path / "book"

    audit = audit_book(pdf, "cpnc-test", out)

    expected_sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    assert audit["manifest"]["book_id"] == "cpnc-test"
    assert audit["manifest"]["source_filename"] == "sample.pdf"
    assert audit["manifest"]["source_sha256"] == expected_sha
    assert audit["manifest"]["pdf_page_count"] == 3

    pages = audit["pages"]
    assert [p["pdf_page"] for p in pages] == [1, 2, 3]
    assert pages[0]["width_pt"] == 300
    assert pages[0]["height_pt"] == 400
    assert pages[0]["text_length"] > 0
    assert pages[0]["image_count"] == 0
    assert pages[1]["image_count"] == 1
    assert pages[2]["vector_drawing_count"] >= 1
    assert pages[0]["text_blocks"]

    manifest_path = out / "manifest.json"
    audit_path = out / "audits" / "raw-page-audit.json"
    assert manifest_path.exists()
    assert audit_path.exists()
    assert json.loads(manifest_path.read_text(encoding="utf-8"))["source_sha256"] == expected_sha
    assert len(json.loads(audit_path.read_text(encoding="utf-8"))["pages"]) == 3
