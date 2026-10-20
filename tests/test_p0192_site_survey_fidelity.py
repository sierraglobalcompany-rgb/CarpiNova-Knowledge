"""Page 192: preserve source-specified site utilities without fabricating a back design."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from carpinova_knowledge.build_dist import build_book_distribution
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
    assert "levantamiento" in data["normalized_text"]
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


def test_book_distribution_retains_p0192_words_and_exact_manifest(tmp_path: Path) -> None:
    out = tmp_path / "knowledge-1.2.0"
    manifest = build_book_distribution(ROOT, "cpnc-2025", out)
    bundle = json.loads((out / "knowledge.bundle.json").read_text(encoding="utf-8"))

    assert manifest["scope"] == "BOOK"
    assert manifest["knowledge_version"] == "1.2.0"
    assert manifest["source_page_count"] == 295
    assert manifest["counts"]["pages"] == 252
    assert len([p for p in bundle["pages"] if p["page_id"]
                == "PAGE-CPNC-2025-P0192"]) == 1
    original = _canonical()
    matches = [r for r in bundle["content"] if r["content_id"] == CID]
    assert len(matches) == 1
    assert matches[0] == original
    assert "hidrosanitarios" in matches[0]["normalized_text"]
    assert all(r.get("status") != "EXECUTABLE" for r in bundle["rules"])
    for name, expected in manifest["files"].items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == expected
