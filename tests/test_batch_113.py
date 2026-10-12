import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_113_recovers_exact_source_page_186() -> None:
    report = build_batch_report(ROOT, "batch-113")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 1,
        "content": 6,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    page_dir = ROOT / "books" / "cpnc-2025" / "pages" / "p0186"
    source = (page_dir / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "¿Cómo funciona Cortecloud para el carpintero?",
        "las 24 horas del día",
        "1. Diseñar módulos",
        "2. Despiezar manualmente",
        "3. Cotizar en tiempo real",
        "Visualización en 3D y control de errores",
        "Armado fácil con etiquetas QR",
        "más de 300 piezas",
        "Perforaciones para tarugos, minifix o tornillos de ensamble",
        "Todo esto acelera el armado y evita errores en la instalación.",
    ):
        assert fragment in source

    assert json.loads((page_dir / "measurements.json").read_text(encoding="utf-8")) == []
    assert json.loads((page_dir / "rules.json").read_text(encoding="utf-8")) == []

    visual = json.loads((page_dir / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual["visuals"])

    audit = (ROOT / "audits" / "f1" / "source-gap-p0186.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit
    assert "PENDING — SOURCE_IMAGE_UNAVAILABLE" not in audit


def test_batch_113_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] == 287
    assert report["pending_pages"] == 8
    assert 186 not in report["pending_pdf_pages"]
    assert report["duplicate_batch_pages"] == []
