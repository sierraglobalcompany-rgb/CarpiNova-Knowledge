import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def _load(page: int, filename: str):
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_103_glossary_p_q_r_s_definitions_are_visually_grounded() -> None:
    report = build_batch_report(ROOT, "batch-103")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 57,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    p0288 = _load(288, "content.json")
    assert len(p0288) == 29
    assert p0288[0]["source_transcription"] == "Palo: Trozo de madera más largo que grueso."
    assert p0288[14]["source_transcription"] == (
        "Perfil : Herraje de aluminio que presta un servicio funcional o estético en un "
        "proyecto de carpintería, ejemplo :\nPerfil Manija\nPerfil Gola\n"
        "Perfil puerta de aluminio\nPerfil para repisa"
    )
    assert p0288[-1]["source_transcription"] == (
        "Quijera: Cada una de las dos ramas de la horquilla que se forma en el extremo de "
        "un madero al hacer una caja para que entre la garganta de otro."
    )
    assert all(item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED" for item in p0288)

    p0289 = _load(289, "content.json")
    assert len(p0289) == 28
    assert p0289[0]["source_transcription"] == (
        "Raigal: Entre madereros, extremo del madero que corresponde a la raíz del árbol."
    )
    assert p0289[14]["source_transcription"].startswith(
        "Retraso : hacer el ensamble de un mueble iniciando el primer paral"
    )
    assert p0289[26]["source_transcription"] == (
        "Serrín: Conjunta de partículas que se desprenden de la madera cuando se sierra.\nAserrín."
    )
    assert p0289[-1]["source_transcription"] == (
        "Serrucho: Sierra de hoja ancha para realizar cortes finos y de precisión."
    )
    assert all(item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED" for item in p0289)
