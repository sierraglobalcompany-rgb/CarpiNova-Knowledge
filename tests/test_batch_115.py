import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_115_recovers_exact_source_pages_194_195() -> None:
    report = build_batch_report(ROOT, "batch-115")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 5,
        "figures": 0,
        "measurements": 24,
        "rules": 8,
    }

    p194 = ROOT / "books" / "cpnc-2025" / "pages" / "p0194"
    p195 = ROOT / "books" / "cpnc-2025" / "pages" / "p0195"

    assert json.loads((p194 / "content.json").read_text(encoding="utf-8")) == []
    assert json.loads((p194 / "measurements.json").read_text(encoding="utf-8")) == []
    assert json.loads((p194 / "rules.json").read_text(encoding="utf-8")) == []
    visual_194 = json.loads((p194 / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual_194["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual_194["visuals"])

    source_195 = (p195 / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "Medidas estándar del mobiliario",
        "Este apoyo tiene una altura estándar de 10 cm y una profundidad de 54 cm.",
        "La altura estándar del mueble bajo es de 78 cm.",
        "para un total de 90 cm de altura desde el suelo hasta la superficie del mesón.",
        "La profundidad del mueble bajo debe ser de 57 cm",
        "para un total de 58.5 cm.",
        "El mueble alto debe tener una altura mínima de 60 cm, siendo 70 cm lo ideal.",
        "La profundidad del mueble alto debe ser de 35 cm como máximo.",
        "Zona de refrigeración: 100 cm (1 metro)",
        "Zona de cocción: 61 cm",
        "Zona de lavado: 65 cm",
        "Supongamos que tienes un espacio de 2.80 m.",
        "Te quedan 50 cm disponibles, espacio ideal para una cajonera de utensilios.",
    ):
        assert fragment in source_195

    visual_195 = json.loads((p195 / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual_195["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual_195["visuals"])

    audit_194 = (ROOT / "audits" / "f1" / "source-gap-p0194.md").read_text(encoding="utf-8")
    audit_195 = (ROOT / "audits" / "f1" / "source-gap-p0195.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit_194 and "SOURCE_IMAGE_UNAVAILABLE" not in audit_194
    assert "RESOLVED" in audit_195


def test_batch_115_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] >= 291
    assert report["pending_pages"] <= 4
    assert 194 not in report["pending_pdf_pages"]
    assert 195 not in report["pending_pdf_pages"]
    assert report["duplicate_batch_pages"] == []
