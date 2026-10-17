from __future__ import annotations

import json
from pathlib import Path

import pytest

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]

FIGURES = {
    "p0235": ROOT / "books" / "cpnc-2025" / "pages" / "p0235" / "figures" / "fig-001.json",
    "p0237": ROOT / "books" / "cpnc-2025" / "pages" / "p0237" / "figures" / "fig-001.json",
    "p0242": ROOT / "books" / "cpnc-2025" / "pages" / "p0242" / "figures" / "fig-001.json",
    "p0245": ROOT / "books" / "cpnc-2025" / "pages" / "p0245" / "figures" / "fig-001.json",
    "p0248": ROOT / "books" / "cpnc-2025" / "pages" / "p0248" / "figures" / "fig-001.json",
    "p0250": ROOT / "books" / "cpnc-2025" / "pages" / "p0250" / "figures" / "fig-001.json",
}

EXPECTED_SOURCE_PAGES = {
    "p0235": (235, 213),
    "p0237": (237, 215),
    "p0242": (242, 220),
    "p0245": (245, 223),
    "p0248": (248, 226),
    "p0250": (250, 228),
}


def _figure(page: str) -> dict:
    return json.loads(FIGURES[page].read_text(encoding="utf-8"))


def _annotation_id(entity_id: str) -> str:
    return f"ann-{entity_id}"


@pytest.mark.parametrize("page", FIGURES)
def test_batch_preserves_source_identity_and_existing_semantics(page: str) -> None:
    figure = _figure(page)
    pdf_page, printed_page = EXPECTED_SOURCE_PAGES[page]

    assert figure["page_id"] == f"PAGE-CPNC-2025-P{pdf_page:04d}"
    assert figure["figure_id"] == f"FIG-CPNC-2025-P{pdf_page:04d}-001"
    assert figure["type"] == "process_diagram"
    assert figure["source"]["pdf_page"] == pdf_page
    assert figure["source"]["printed_page"] == printed_page
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == []
    assert figure["entities"]
    assert figure["annotations"]
    assert figure["educational_sequence"]


@pytest.mark.parametrize("page", FIGURES)
def test_batch_uses_existing_normalized_contract_without_new_primitives(page: str) -> None:
    figure = _figure(page)
    reconstruction = figure["reconstruction"]

    assert reconstruction.get("render_contract") == "normalized-2d-v1"
    assert reconstruction["preferred_renderer"] == "svg"
    assert reconstruction["deterministic_required"] is True
    assert reconstruction["generative_image_allowed"] is False
    assert figure["camera"] == {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
    }

    entity_ids = [entity["id"] for entity in figure["entities"]]
    for entity in figure["entities"]:
        geometry = entity["geometry"]
        assert geometry["primitive"] == "rect"
        assert geometry["precision"] == "approximate"
        assert "bounding_box" not in geometry
        bounds = geometry["bounds"]
        assert 0 <= bounds["x"] <= 1
        assert 0 <= bounds["y"] <= 1
        assert bounds["width"] > 0
        assert bounds["height"] > 0
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1

    annotations = figure["annotations"]
    assert [annotation["target_entity_id"] for annotation in annotations] == entity_ids
    assert [annotation["id"] for annotation in annotations] == [
        _annotation_id(entity_id) for entity_id in entity_ids
    ]
    for annotation in annotations:
        placement = annotation["placement"]
        assert placement["precision"] == "approximate"
        assert 0 <= placement["x"] <= 1
        assert 0 <= placement["y"] <= 1

    assert figure["layers"] == [
        {"id": "geometry", "order": 10, "entity_ids": entity_ids},
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": [_annotation_id(entity_id) for entity_id in entity_ids],
        },
    ]

    semantic_guardrail = " ".join(
        [figure["accessibility"]["summary"], figure["review"]["notes"]]
    ).lower()
    assert "métric" in semantic_guardrail or "escala" in semantic_guardrail


@pytest.mark.parametrize("page", FIGURES)
def test_batch_renders_deterministically(page: str) -> None:
    figure = _figure(page)
    first = render_normalized_2d_svg(figure)
    second = render_normalized_2d_svg(figure)

    assert first == second
    assert first.startswith("<svg")
    assert 'data-layer-id="geometry"' in first
    assert 'data-layer-id="labels"' in first
    for entity in figure["entities"]:
        assert f'data-entity-id="{entity["id"]}"' in first
        assert f'data-annotation-id="{_annotation_id(entity["id"])}"' in first


def test_batch_preserves_known_source_irregularities_without_completion() -> None:
    p0235 = json.dumps(_figure("p0235"), ensure_ascii=False)
    for text in (
        "Sin garantía",
        "Sin cumplir plazos",
        "Trabajo abandonado",
        "Contratos sin ejecutar",
        "Buena atención al cliente",
        "Garantía y posventa",
        "Conocimiento técnico",
    ):
        assert text in p0235

    p0237 = json.dumps(_figure("p0237"), ensure_ascii=False)
    assert "1 Identifica el sector maderero de tu ciudad" in p0237
    assert "2 Establece contacto por WhatsApp" in p0237
    assert "5 Obtén listas de precios y catálogos" in p0237
    assert "Preséntate personalmentte" in p0237
    assert p0237.count("Obtén listas de precios y catálogos") >= 2

    p0242 = json.dumps(_figure("p0242"), ensure_ascii=False)
    for text in ("40%", "15%", "45%", "0.4", "0,6 / 0,5/ 0,4"):
        assert text in p0242
    assert "Calcular el costo por tablero y dividir" in p0242
    assert _figure("p0242")["measurements"] == []

    p0248 = json.dumps(_figure("p0248"), ensure_ascii=False)
    assert p0248.count("Permite previsualizar el mueble") >= 2
    assert p0248.count("Dibuja sus dimensiones en la pared") >= 2

    p0250 = json.dumps(_figure("p0250"), ensure_ascii=False)
    for text in (
        "ACCESOS",
        "TAMAÑO DE PIEZAS",
        "CONEXIONES",
        "GUARDAS O ZÓCALOS",
        "MOLDURAS",
        "TIPO DE ANCLAJES",
    ):
        assert text in p0250
    assert _figure("p0250")["measurements"] == []


def test_batch_repository_stays_valid() -> None:
    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
