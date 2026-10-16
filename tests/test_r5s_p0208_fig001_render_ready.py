from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = (
    ROOT
    / "books"
    / "cpnc-2025"
    / "pages"
    / "p0208"
    / "figures"
    / "fig-001.json"
)
MEASUREMENTS_PATH = (
    ROOT
    / "books"
    / "cpnc-2025"
    / "pages"
    / "p0208"
    / "measurements.json"
)

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0208-001",
    "MEAS-CPNC-2025-P0208-002",
    "MEAS-CPNC-2025-P0208-003",
    "MEAS-CPNC-2025-P0208-004",
    "MEAS-CPNC-2025-P0208-005",
]

EXPECTED_PRIMITIVES = {
    "door-leaf": "rect",
    "internal-frame": "rect",
    "door-skin": "rect",
    "lock": "polyline",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "internal-frame", "to": "door-leaf", "type": "inside"},
    {"from": "door-skin", "to": "internal-frame", "type": "covers"},
    {"from": "lock", "to": "door-leaf", "type": "installed_on"},
]

EXPECTED_LABELS = [
    ("door-leaf", "Espesor puerta estándar 36 mm"),
    ("lock", "90 cm desde piso; 6 cm desde canto"),
]


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0208_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0208-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0208"
    assert figure["type"] == "dimensioned_drawing"
    assert figure["source"]["pdf_page"] == 208
    assert figure["source"]["printed_page"] == 186
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


def test_p0208_fig001_preserves_source_semantics_without_metric_inference() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == set(EXPECTED_PRIMITIVES)
    for entity_id, expected_primitive in EXPECTED_PRIMITIVES.items():
        geometry = entities[entity_id]["geometry"]
        assert geometry["precision"] == "approximate"
        assert "primitive" in geometry
        assert geometry["primitive"] == expected_primitive
        assert "dimensions" not in geometry
        assert "bbox" not in geometry

        if expected_primitive == "rect":
            assert "points" not in geometry
            bounds = geometry["bounds"]
            _assert_normalized(bounds["x"])
            _assert_normalized(bounds["y"])
            assert 0 < bounds["width"] <= 1
            assert 0 < bounds["height"] <= 1
            assert bounds["x"] + bounds["width"] <= 1
            assert bounds["y"] + bounds["height"] <= 1
        else:
            assert "bounds" not in geometry
            points = geometry["points"]
            assert len(points) >= 2
            for point in points:
                _assert_normalized(point["x"])
                _assert_normalized(point["y"])

    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == EXPECTED_MEASUREMENTS

    measurements = {item["measurement_id"]: item for item in _measurements()}
    expected_values = {
        "MEAS-CPNC-2025-P0208-001": (4, "mm"),
        "MEAS-CPNC-2025-P0208-002": (5.5, "mm"),
        "MEAS-CPNC-2025-P0208-003": (36, "mm"),
        "MEAS-CPNC-2025-P0208-004": (90, "cm"),
        "MEAS-CPNC-2025-P0208-005": (6, "cm"),
    }
    assert set(measurements) == set(expected_values)
    for measurement_id, (value, unit) in expected_values.items():
        assert measurements[measurement_id]["value"] == value
        assert measurements[measurement_id]["unit"] == unit
        assert measurements[measurement_id]["status"] == "VISUALLY_VERIFIED"

    annotations = figure["annotations"]
    assert [(item["target_entity_id"], item["text"]) for item in annotations] == EXPECTED_LABELS
    annotation_ids = []
    for annotation in annotations:
        annotation_id = annotation["id"]
        assert annotation_id not in annotation_ids
        annotation_ids.append(annotation_id)
        placement = annotation["placement"]
        assert placement["precision"] == "approximate"
        _assert_normalized(placement["x"])
        _assert_normalized(placement["y"])

    layers = figure["layers"]
    assert layers
    assert [layer["order"] for layer in layers] == sorted(layer["order"] for layer in layers)
    assert len({layer["order"] for layer in layers}) == len(layers)

    layered_entities = [entity_id for layer in layers for entity_id in layer.get("entity_ids", [])]
    layered_annotations = [
        annotation_id for layer in layers for annotation_id in layer.get("annotation_ids", [])
    ]
    assert layered_entities == list(EXPECTED_PRIMITIVES)
    assert layered_annotations == annotation_ids
    assert len(layered_entities) == len(set(layered_entities))
    assert len(layered_annotations) == len(set(layered_annotations))

    notes = figure["review"]["notes"]
    assert "no codifica escala física" in notes
    assert "bastidor interno" in notes
    assert "conceptual" in notes or "pedagógica" in notes


def test_p0208_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in EXPECTED_PRIMITIVES:
        assert first.count(f'data-entity-id="{entity_id}"') == 1
    for annotation in figure["annotations"]:
        assert first.count(f'data-annotation-id="{annotation["id"]}"') == 1
        assert f'>{annotation["text"]}<' in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
