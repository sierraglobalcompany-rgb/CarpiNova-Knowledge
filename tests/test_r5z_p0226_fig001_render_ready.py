from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0226" / "figures" / "fig-001.json"

EXPECTED_ENTITY_TYPES = {
    "tv-board": "tv_support_board",
    "upper-cabinet": "entertainment_center_upper_module",
    "tv": "television",
    "cable-holes": "connection_holes",
    "electrical-box": "electrical_box",
    "cleat": "chamfer_cleat",
}

EXPECTED_PRIMITIVES = {entity_id: "rect" for entity_id in EXPECTED_ENTITY_TYPES}

EXPECTED_RELATIONSHIPS = [
    {"from": "tv", "to": "tv-board", "type": "mounted_on"},
    {"from": "cable-holes", "to": "tv-board", "type": "passes_through"},
    {"from": "electrical-box", "to": "tv-board", "type": "relocated_into"},
    {"from": "cleat", "to": "upper-cabinet", "type": "supports"},
]

EXPECTED_LABELS = [
    ("tv-board", "El tablón recibe el peso del T.V. y opcionalmente alguna repisa"),
    ("cable-holes", "Conexiones mediante perforaciones hechas con broca"),
    ("electrical-box", "Caja eléctrica trasladada del muro al mueble"),
]

EXPECTED_ANNOTATION_IDS = [
    "ann-tv-board",
    "ann-cable-holes",
    "ann-electrical-box",
]


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0226_fig001_declares_frozen_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0226-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0226"
    assert figure["type"] == "mixed"
    assert figure["source"]["pdf_page"] == 226
    assert figure["source"]["printed_page"] == 204
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == []

    assert figure["reconstruction"].get("render_contract") == "normalized-2d-v1"
    assert figure["reconstruction"]["preferred_renderer"] == "svg"
    assert figure["reconstruction"]["deterministic_required"] is True
    assert figure["reconstruction"]["generative_image_allowed"] is False
    assert figure.get("camera") == {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
    }

    assert [(a["target_entity_id"], a["text"]) for a in figure["annotations"]] == EXPECTED_LABELS
    assert [a.get("id") for a in figure["annotations"]] == EXPECTED_ANNOTATION_IDS
    for annotation in figure["annotations"]:
        placement = annotation.get("placement")
        assert placement is not None
        assert placement["precision"] == "approximate"
        _assert_normalized(placement["x"])
        _assert_normalized(placement["y"])

    layers = figure.get("layers")
    assert layers == [
        {
            "id": "geometry",
            "order": 10,
            "entity_ids": [
                "tv-board",
                "upper-cabinet",
                "tv",
                "cable-holes",
                "electrical-box",
                "cleat",
            ],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": EXPECTED_ANNOTATION_IDS,
        },
    ]
    assert len(layers[0]["entity_ids"]) == len(set(layers[0]["entity_ids"])) == 6
    assert len(layers[1]["annotation_ids"]) == len(set(layers[1]["annotation_ids"])) == 3


def test_p0226_fig001_preserves_source_truth_without_inventing_measurements() -> None:
    figure = _figure()

    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == []

    entities = {entity["id"]: entity for entity in figure["entities"]}
    assert set(entities) == set(EXPECTED_ENTITY_TYPES)

    for entity_id, entity_type in EXPECTED_ENTITY_TYPES.items():
        entity = entities[entity_id]
        assert entity["type"] == entity_type
        geometry = entity["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry.get("primitive") == EXPECTED_PRIMITIVES[entity_id]
        assert "dimensions" not in geometry
        assert "bbox" not in geometry

        bounds = geometry.get("bounds")
        assert bounds is not None
        _assert_normalized(bounds["x"])
        _assert_normalized(bounds["y"])
        assert bounds["width"] > 0
        assert bounds["height"] > 0
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1

    semantic_text = " ".join(
        [
            figure["purpose"],
            figure["review"]["notes"],
            figure["accessibility"]["summary"],
        ]
    ).lower()
    assert "no" in semantic_text and "estándar" in semantic_text
    assert "métric" in semantic_text or "escala" in semantic_text
    assert "fabricación" in semantic_text
    assert "carga" in semantic_text or "estructur" in semantic_text

    serialized = json.dumps(figure, ensure_ascii=False).lower()
    for forbidden_claim in (
        "120 kgf",
        "45°",
        "45 grados",
        "diámetro",
        "tolerancia",
    ):
        assert forbidden_claim not in serialized


def test_p0226_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-entity-id="tv-board"' in svg_first
    assert 'data-entity-id="upper-cabinet"' in svg_first
    assert 'data-entity-id="cable-holes"' in svg_first
    assert 'data-entity-id="electrical-box"' in svg_first
    assert 'data-entity-id="cleat"' in svg_first
    assert 'data-annotation-id="ann-tv-board"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
