from pathlib import Path
import hashlib
import fitz

from carpinova_knowledge.audit_book import audit_book


def test_audit_book_collects_objective_page_metadata(tmp_path: Path):
    pdf = tmp_path / 'synthetic.pdf'
    doc = fitz.open()
    p1 = doc.new_page(width=300, height=400)
    p1.insert_text((50, 50), 'hello page one')
    p2 = doc.new_page(width=300, height=400)
    p2.insert_text((50, 50), 'page two')
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 10, 10), 0)
    pix.clear_with(200)
    p2.insert_image(fitz.Rect(20, 80, 80, 140), pixmap=pix)
    p3 = doc.new_page(width=300, height=400)
    shape = p3.new_shape()
    shape.draw_rect(fitz.Rect(20, 20, 100, 100))
    shape.finish(color=(0, 0, 0))
    shape.commit()
    doc.save(pdf)
    doc.close()

    out = tmp_path / 'out'
    result = audit_book(pdf, 'TEST-BOOK', out)

    assert result['manifest']['pdf_page_count'] == 3
    assert result['manifest']['source_sha256'] == hashlib.sha256(pdf.read_bytes()).hexdigest()
    pages = result['audit']['pages']
    assert [p['pdf_page'] for p in pages] == [1, 2, 3]
    assert pages[0]['text_length'] > 0
    assert pages[1]['embedded_image_count'] >= 1
    assert pages[2]['vector_drawing_count'] >= 1
    assert pages[0]['width'] == 300
    assert pages[0]['height'] == 400
    assert (out / 'manifest.json').exists()
    assert (out / 'audits' / 'raw-page-audit.json.gz').exists()
