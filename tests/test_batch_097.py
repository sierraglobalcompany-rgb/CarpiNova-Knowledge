import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_097_blank_transition_and_glossary_title_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-097")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
    assert report["counts"]["content"] == 1
    assert report["counts"]["figures"] == 0
    assert report["counts"]["measurements"] == 0
    assert report["counts"]["rules"] == 0

    blank_content = json.loads(
        (ROOT / "books" / "cpnc-2025" / "pages" / "p0276" / "content.json").read_text(
            encoding="utf-8"
        )
    )
    assert blank_content == []

    glossary_content = json.loads(
        (ROOT / "books" / "cpnc-2025" / "pages" / "p0277" / "content.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(glossary_content) == 1
    item = glossary_content[0]
    assert item["source_transcription"] == "GLOSARIO\nPARA QUE APRENDAS MÁS DE CARPINTERÍA"
    assert item["source"]["pdf_page"] == 277
    assert item["source"]["printed_page"] == 255
