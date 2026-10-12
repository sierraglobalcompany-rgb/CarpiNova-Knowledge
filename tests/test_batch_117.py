import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_117_recovers_exact_source_page_207() -> None:
    report = build_batch_report(ROOT, "batch-117")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 1,
        "content": 3,
        "figures": 0,
        "measurements": 4,
        "rules": 5,
    }

    p207 = ROOT / "books" / "cpnc-2025" / "pages" / "p0207"
    source = (p207 / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "Puertas",
        "Las puertas estándar deben instalarse a escuadra.",
        "La medida ideal del vano es de 80 cm de ancho por 210 cm de alto",
        "lo cual permite el paso de una silla de ruedas.",
        "Mide la altura del vano a la izquierda y a la derecha.",
        "Mide el ancho en tres puntos: superior, medio e inferior.",
        "Toma siempre la medida menor y réstale 1 cm para tolerancia.",
        "Las posibles diferencias entre muro y madera se tapan con tapaluz o molduras.",
    ):
        assert fragment in source

    measurements = json.loads((p207 / "measurements.json").read_text(encoding="utf-8"))
    values = {(item["value"], item["unit"]) for item in measurements}
    for expected in ((80, "cm"), (210, "cm"), (3, "count"), (1, "cm")):
        assert expected in values

    visual = json.loads((p207 / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual["visuals"])

    audit = (ROOT / "audits" / "f1" / "source-gap-p0207.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit


def test_batch_117_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] == 295
    assert report["pending_pages"] == 0
    assert report["pending_pdf_pages"] == []
    assert report["duplicate_batch_pages"] == []
