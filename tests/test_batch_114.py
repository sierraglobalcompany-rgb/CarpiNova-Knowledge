import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_114_recovers_exact_source_pages_189_190() -> None:
    report = build_batch_report(ROOT, "batch-114")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 9,
        "figures": 1,
        "measurements": 9,
        "rules": 8,
    }

    p189 = ROOT / "books" / "cpnc-2025" / "pages" / "p0189"
    p190 = ROOT / "books" / "cpnc-2025" / "pages" / "p0190"
    source_189 = (p189 / "source.md").read_text(encoding="utf-8")
    source_190 = (p190 / "source.md").read_text(encoding="utf-8")

    for fragment in (
        "Además, se debe verificar:",
        "Teorema de pitágoras",
        "El mueble bajo llega hasta 90 cm incluyendo el mesón",
        "se recomienda dejar 61 cms",
        "si en la parte trasera mide 100 cm y en la delantera 98 cm",
        "Debes trabajar con la medida menor",
    ):
        assert fragment in source_189

    for fragment in (
        "Desde el interior y desde el exterior del vano",
        "réstale 1 cm",
        "Las puertas deben funcionar perfectamente a escuadra",
        "Otros casos: centros de entretenimiento y estudios",
        "En la toma de medidas está el éxito de un proyecto de carpintería.",
    ):
        assert fragment in source_190

    visual = json.loads((p189 / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert any(item["meaningful"] is True for item in visual["visuals"])
    assert (p189 / "figures" / "fig-001.json").exists()

    audit_189 = (ROOT / "audits" / "f1" / "source-gap-p0189.md").read_text(encoding="utf-8")
    audit_190 = (ROOT / "audits" / "f1" / "source-gap-p0190.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit_189 and "SOURCE_IMAGE_UNAVAILABLE" not in audit_189
    assert "RESOLVED" in audit_190 and "SOURCE_IMAGE_UNAVAILABLE" not in audit_190


def test_batch_114_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] == 289
    assert report["pending_pages"] == 6
    assert report["pending_pdf_pages"] == [194, 195, 202, 207, 213, 223]
    assert report["duplicate_batch_pages"] == []
