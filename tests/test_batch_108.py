import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def _load(page: int, filename: str):
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_108_recovers_pages_161_162_from_exact_2025_source() -> None:
    report = build_batch_report(ROOT, "batch-108")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
    assert report["counts"]["figures"] == 1

    p0161 = _load(161, "content.json")
    assert p0161[0]["source_transcription"] == "facilitar la construcción de muros."
    assert any("25.4" in item["source_transcription"] for item in p0161)
    assert any("Tipos de escuadras y nivel" in item["source_transcription"] for item in p0161)
    assert all(
        item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
        for item in p0161
    )

    p0162 = _load(162, "content.json")
    assert any("Escuadra de carpintero" in item["source_transcription"] for item in p0162)
    assert any("falsa escuadra" in item["source_transcription"] for item in p0162)
    assert any("nivel de burbuja" in item["source_transcription"] for item in p0162)
    assert any("fondo mínimo del clóset es de 60 cm" in item["source_transcription"] for item in p0162)
    assert p0162[-1]["source_transcription"].endswith("En estos casos, se toma la medida menor")
    assert all(
        item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
        for item in p0162
    )

    p0163 = _load(163, "content.json")
    carry = p0162[-1]["source_transcription"].rsplit(". ", 1)[-1] + " " + p0163[0]["source_transcription"]
    assert "En estos casos, se toma la medida menor del vano y se instalan molduras" in carry

    visual_161 = _load(161, "visual-inventory.json")
    assert visual_161["inspection_status"] == "VISUALLY_VERIFIED"
    assert any(item["meaningful"] is True and item.get("figure_id") for item in visual_161["visuals"])

    visual_162 = _load(162, "visual-inventory.json")
    assert visual_162["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual_162["visuals"])
