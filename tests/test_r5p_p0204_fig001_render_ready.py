from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0204" / "figures" / "fig-001.json"

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0204-001",
    "MEAS-CPNC-2025-P0204-002",
    "MEAS-CPNC-2025-P0204-003",
    "MEAS-CPNC-2025-P0204-004",
]

EXPECTED_PRIMITIVES = {
    "stile": "rect",
    "closet-internal-overhead": "rect",
    "closet-external-overhead": "rect",
    "closet-body": "rect",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "stile", "to": "closet-internal-overhead", "type": "supports"},
    {
        "from": "closet-internal-overhead",
        "to": "closet-body",
        "type": "integrated_configuration",
    },
    {
        "from": "closet-external-overhead",
        "to": "closet-body",
        "type": "independent_configuration",
    },
]

EXPECTED_ANNOTATIONS = {
    "stile": ("ann-stile", "PARAL 190 cm x45cm"),
    "closet-internal-overhead": ("ann-internal-overhead", "maletero interno"),
    "closet-external-overhead": (
        "ann-external-overhead",
        "maletero independiente (externo)",
    ),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0204_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0204-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0204"
    assert figure["type"] == "dimensioned_drawing"
    assert figure["source"]["pdf_page"] == 204
    assert figure["source"]["printed_page"] == 182
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == EXPECTED_MEASUREMENTS
    assert figure["reconstruction"] == {
        "preferred_renderer": "svg",
        "deterministic_required": True,
        "generative_image_allowed": False,
        "render_contract": "normalized-2d-v1",
    }
    assert figure["camera"] == {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
    }


def test_p0204_fig001_preserves_source_entities_relationships_and_labels() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == set(EXPECTED_PRIMITIVES)
    for entity_id, expected_primitive in EXPECTED_PRIMITIVES.items():
        geometry = entities[entity_id]["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry["primitive"] == expected_primitive
        assert "dimensions" not in geometry
        assert "bbox" not in geometry
        assert "points" not in geometry

        bounds = geometry["bounds"]
        _assert_normalized(bounds["x"])
        _assert_normalized(bounds["y"])
        assert 0 < bounds["width"] <= 1
        assert 0 < bounds["height"] <= 1
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1

    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == EXPECTED_MEASUREMENTS

    annotations = {
        annotation["target_entity_id"]: annotation for annotation in figure["annotations"]
    }
    assert set(annotations) == set(EXPECTED_ANNOTATIONS)
    for target_entity_id, (annotation_id, text) in EXPECTED_ANNOTATIONS.items():
        annotation = annotations[target_entity_id]
        assert annotation["id"] == annotation_id
        assert annotation["text"] == text
        placement = annotation["placement"]
        assert placement["precision"] == "approximate"
        _assert_normalized(placement["x"])
        _assert_normalized(placement["y"])

    assert figure["layers"] == [
        {
            "id": "closet-reference",
            "order": 10,
            "entity_ids": ["closet-body", "stile"],
        },
        {
            "id": "overhead-configurations",
            "order": 20,
            "entity_ids": [
                "closet-internal-overhead",
                "closet-external-overhead",
            ],
        },
        {
            "id": "labels",
            "order": 30,
            "annotation_ids": [
                "ann-stile",
                "ann-internal-overhead",
                "ann-external-overhead",
            ],
        },
    ]


def test_p0204_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in EXPECTED_PRIMITIVES:
        assert first.count(f'data-entity-id="{entity_id}"') == 1
    for annotation_id, text in EXPECTED_ANNOTATIONS.values():
        assert first.count(f'data-annotation-id="{annotation_id}"') == 1
        assert f">{text}<" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
