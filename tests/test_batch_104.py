import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def _load(page: int, filename: str):
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_104_glossary_s_t_u_v_x_definitions_are_visually_grounded() -> None:
    report = build_batch_report(ROOT, "batch-104")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 64,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    p0290 = _load(290, "content.json")
    assert len(p0290) == 33
    assert p0290[0]["source_transcription"] == "Sierra: Herramienta para cortar madera."
    assert p0290[5]["source_transcription"].startswith("Sobina; Especie de clavija")
    assert p0290[-1]["source_transcription"].endswith("para asentar")
    assert all(item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED" for item in p0290)

    p0291 = _load(291, "content.json")
    assert len(p0291) == 31
    assert p0291[0]["content_type"] == "reference"
    assert p0291[0]["source_transcription"] == "sobre ellos los rieles."
    assert p0291[1]["source_transcription"] == "Trazar: Transferir el contorno de una superficie a otra."
    assert p0291[-1]["source_transcription"] == "xilófago: Se dice de los insectos que roen la madera."
    assert all(item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED" for item in p0291)
