"""Page 192: preserve source-specified site utilities without fabricating a back design."""
from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_docs import _render

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "books" / "cpnc-2025" / "pages" / "p0192"
CID = "CONTENT-CPNC-2025-P0192-001"


def _canonical() -> dict:
    records = json.loads((PAGE / "content.json").read_text(encoding="utf-8"))
    assert len(records) == 1
    assert records[0]["content_id"] == CID
    return records[0]


def test_p0192_source_and_normalization_retains_electric_and_hydrosanitary_points() -> None:
    page = json.loads((PAGE / "page.json").read_text(encoding="utf-8"))
    data = _canonical()

    assert (page["pdf_page"], page["printed_page"]) == (192, 170)
    assert (data["source"]["pdf_page"], data["source"]["printed_page"]) == (192, 170)
    assert data["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert "UBICACIÓN PUNTOS ELECTRICOS, HIDROSANITARIOS" in data["source_transcription"]
    assert "ubicación de puntos eléctricos e hidrosanitarios" in data["normalized_text"]
    assert "puntos eléctricos e hidrosanitarios" in data["learning_text"]
    assert "toma de medidas en obra" in data["normalized_text"]
    # Survey instructions cannot authorize a solution for an unmeasured kitchen.
    assert "recort" not in data["normalized_text"].lower()
    assert "perfor" not in data["normalized_text"].lower()
    assert "sin fondo" not in data["normalized_text"].lower()


def test_p0192_derived_markdown_is_exact_output_of_existing_renderer() -> None:
    records = json.loads((PAGE / "content.json").read_text(encoding="utf-8"))
    for name, field, label in (
        ("normalized.md", "normalized_text", "Normalized text"),
        ("source.md", "source_transcription", "Source transcription"),
        ("learning.md", "learning_text", "Learning text"),
    ):
        assert (PAGE / name).read_text(encoding="utf-8") == _render(records, field, label)


def test_p0192_visual_inventory_links_same_source_page() -> None:
    visual = json.loads((PAGE / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["pdf_page"] == 192
    assert visual["page_id"] == "PAGE-CPNC-2025-P0192"
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert any(item["figure_id"] == "FIG-CPNC-2025-P0192-001"
               and item["kind"] == "site_measurement_form"
               for item in visual["visuals"])

