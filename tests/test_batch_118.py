import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_118_recovers_exact_source_pages_213_and_223() -> None:
    report = build_batch_report(ROOT, "batch-118")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 7,
        "figures": 0,
        "measurements": 16,
        "rules": 11,
    }

    p213 = ROOT / "books" / "cpnc-2025" / "pages" / "p0213"
    source_213 = (p213 / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "Camas",
        "Las medidas de cama dependen del colchón, que generalmente tiene un largo de 1.90 m.",
        "Los anchos más comunes son:",
        "0.80 m",
        "1.80 m",
        "La estructura interna de la cama (llamada armillas) debe construirse para que el colchón encaje perfectamente.",
        "Estas armillas se refuerzan lateralmente para soportar el tendido de tablas o láminas",
    ):
        assert fragment in source_213

    measurements_213 = json.loads((p213 / "measurements.json").read_text(encoding="utf-8"))
    values_213 = {(item["value"], item["unit"]) for item in measurements_213}
    for expected in (
        (1.9, "m"),
        (0.8, "m"),
        (0.9, "m"),
        (1.0, "m"),
        (1.2, "m"),
        (1.4, "m"),
        (1.6, "m"),
        (1.8, "m"),
    ):
        assert expected in values_213

    p223 = ROOT / "books" / "cpnc-2025" / "pages" / "p0223"
    source_223 = (p223 / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "Estudios y comedores",
        "Altura: entre 75 cm y 78 cm",
        "Profundidad mínima: 60 cm (según normativas de seguridad laboral)",
        "Bordes: redondeados",
        "Altura de la mesa: 78 cm",
        "Si ves TV desde un sofá, el centro de la pantalla debe quedar a 120 cm del piso.",
        "Si ves TV acostado, la base inferior del televisor debe quedar a 80 cm del piso.",
        "medida estandarizada llamada VESA",
    ):
        assert fragment in source_223

    measurements_223 = json.loads((p223 / "measurements.json").read_text(encoding="utf-8"))
    values_223 = {(item["value"], item["unit"]) for item in measurements_223}
    for expected in (
        (75, "cm"),
        (78, "cm"),
        (60, "cm"),
        (45, "cm"),
        (120, "cm"),
        (80, "cm"),
    ):
        assert expected in values_223

    for page in (p213, p223):
        visual = json.loads((page / "visual-inventory.json").read_text(encoding="utf-8"))
        assert visual["inspection_status"] == "VISUALLY_VERIFIED"
        assert all(item["meaningful"] is False for item in visual["visuals"])

    for pdf_page in (213, 223):
        audit = (ROOT / "audits" / "f1" / f"source-gap-p{pdf_page:04d}.md").read_text(
            encoding="utf-8"
        )
        assert "RESOLVED" in audit


def test_batch_118_completes_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["total_pages"] == 295
    assert report["complete_pages"] == 295
    assert report["pending_pages"] == 0
    assert report["pending_pdf_pages"] == []
    assert report["duplicate_batch_pages"] == []
    assert report["complete"] is True
