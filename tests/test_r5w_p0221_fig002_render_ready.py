from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0221" / "figures" / "fig-002.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0221" / "measurements.json"

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0221-001",
    "MEAS-CPNC-2025-P0221-002",
    "MEAS-CPNC-2025-P0221-003",
    "MEAS-CPNC-2025-P0221-004",
]

EXPECTED_ENTITY_TYPES = {
    "lateral-B": "melamine_particleboard_side_B",
    "through-hole": "female_pivot_through_hole",
    "female-pivot-plate": "female_pivot_plate",
    "internal-face": "internal_face_of_side_B",
}

EXPECTED_PRIMITIVES = {
    "lateral-B": "rect",
    "through-hole": "polyline",
    "female-pivot-plate": "rect",
    "internal-face": "line",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "through-hole", "to": "lateral-B", "type": "passes_through"},
    {"from": "female-pivot-plate", "to": "internal-face", "type": "mounted_on"},
]

EXPECTED_LABELS = [
    ("through-hole", "Ø 25 mm pasante; 23 cm desde borde trasero; 4.8 cm desde borde superior"),
    ("female-pivot-plate", "Asegurar con tornillos plateados"),
    ("internal-face", "La platina pivote hembra queda en la cara interna del lateral B"),
]

EXPECTED_ANNOTATION_IDS = [
    "ann-through-hole",
    "ann-female-pivot-plate",
    "ann-internal-face",
]

EXPECTED_MEASUREMENT_VALUES = {
    "MEAS-CPNC-2025-P0221-001": (18, "mm"),
    "MEAS-CPNC-2025-P0221-002": (25, "mm"),
    "MEAS-CPNC-2025-P0221-003": (23, "cm"),
    "MEAS-CPNC-2025-P0221-004": (4.8, "cm"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def _assert_normalized_point(point: dict) -> None:
    _assert_normalized(point["x"])
    _assert_normalized(point["y"])


def test_p0221_fig002_declares_frozen_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0221-002"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0221"
    assert figure["type"] == "dimensioned_drawing"
    assert figure["source"]["pdf_page"] == 221
    assert figure["source"]["printed_page"] == 199
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == EXPECTED_MEASUREMENTS
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

    assert figure.get("layers") == [
        {
            "id": "geometry",
            "order": 10,
            "entity_ids": ["lateral-B", "through-hole", "female-pivot-plate", "internal-face"],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": EXPECTED_ANNOTATION_IDS,
        },
    ]


def test_p0221_fig002_preserves_source_semantics_with_non_metric_geometry() -> None:
    figure = _figure()
    measurements = _measurements()

    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == EXPECTED_MEASUREMENTS

    by_id = {item["measurement_id"]: item for item in measurements}
    assert set(by_id) == set(EXPECTED_MEASUREMENTS)
    for measurement_id, (value, unit) in EXPECTED_MEASUREMENT_VALUES.items():
        assert by_id[measurement_id]["value"] == value
        assert by_id[measurement_id]["unit"] == unit
        assert by_id[measurement_id]["status"] == "VISUALLY_VERIFIED"

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

    for entity_id in ("lateral-B", "female-pivot-plate"):
        bounds = entities[entity_id]["geometry"].get("bounds")
        assert bounds is not None
        _assert_normalized(bounds["x"])
        _assert_normalized(bounds["y"])
        assert bounds["width"] > 0
        assert bounds["height"] > 0
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1

    hole_points = entities["through-hole"]["geometry"].get("points")
    assert hole_points is not None
    assert len(hole_points) >= 5
    assert hole_points[0] == hole_points[-1]
    for point in hole_points:
        _assert_normalized_point(point)

    face_points = entities["internal-face"]["geometry"].get("points")
    assert face_points is not None
    assert len(face_points) == 2
    for point in face_points:
        _assert_normalized_point(point)

    semantic_text = " ".join(
        [
            figure["review"]["notes"],
            figure["accessibility"]["summary"],
        ]
    ).lower()
    assert "no codifica escala física" in semantic_text
    assert "mediciones" in semantic_text
    assert "fuente" in semantic_text
    assert "18 mm" in semantic_text
    assert "25 mm" in semantic_text
    assert "23 cm" in semantic_text
    assert "4.8 cm" in semantic_text


def test_p0221_fig002_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-entity-id="through-hole"' in svg_first
    assert 'data-annotation-id="ann-through-hole"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
