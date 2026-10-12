import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def _load(page: int, filename: str):
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_107_recovers_missing_tool_pages_from_exact_source() -> None:
    report = build_batch_report(ROOT, "batch-107")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 2,
        "content": 11,
        "figures": 0,
        "measurements": 0,
        "rules": 0,
    }

    p0150 = _load(150, "content.json")
    assert len(p0150) == 5
    assert p0150[0]["source_transcription"].startswith("El taladro es, en mi opinión")
    assert "mandril" in p0150[1]["source_transcription"]
    assert "función de percutor" in p0150[2]["source_transcription"]
    assert "torque" in p0150[3]["source_transcription"]
    assert "selector de velocidades" in p0150[4]["source_transcription"]
    assert all(
        item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
        for item in p0150
    )

    p0160 = _load(160, "content.json")
    assert len(p0160) == 6
    assert p0160[0]["source_transcription"].startswith("Conclusión")
    assert p0160[1]["source_transcription"].startswith("El Flexómetro")
    assert "mecanismo retráctil" in p0160[2]["source_transcription"]
    assert "leve movimiento" in p0160[3]["source_transcription"]
    assert "medidas internas" in p0160[4]["source_transcription"]
    assert "pequeños rombos" in p0160[5]["source_transcription"]
    assert all(
        item["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
        for item in p0160
    )

    for page in (150, 160):
        visuals = _load(page, "visual-inventory.json")
        assert visuals["inspection_status"] == "VISUALLY_VERIFIED"
        assert all(item["meaningful"] is False for item in visuals["visuals"])
