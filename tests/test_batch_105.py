import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def _load(page: int, filename: str):
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_105_glossary_z_and_closing_page_are_visually_grounded() -> None:
    report = build_batch_report(ROOT, "batch-105")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 4,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    p0292 = _load(292, "content.json")
    assert len(p0292) == 3
    assert [item["source_transcription"] for item in p0292] == [
        "Zanca: Madero inclinado que sirve de apoyo a los peldaños de una escalera.",
        "Zócalo: Cuerpo inferior de un edificio u obra, que sirve para elevar los basamentos a un mismo nivel. Parte inferior de las paredes.",
        "Zoquete: Trozo cuadrado de madera anclado a la pared para asegurar los marcos de las puertas y ventanas.",
    ]
    assert all(item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED" for item in p0292)

    p0293 = _load(293, "content.json")
    assert len(p0293) == 1
    assert p0293[0]["content_type"] == "reference"
    assert p0293[0]["source_transcription"] == "CARPINTERÍA PARA\nNO CARPINTER@S\nCAMILO CALLE"
    assert p0293[0]["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
