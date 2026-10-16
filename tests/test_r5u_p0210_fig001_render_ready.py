from __future__ import annotations

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
    / "p0210"
    / "figures"
    / "fig-001.json"
)
MEASUREMENTS_PATH = (
    ROOT
    / "books"
    / "cpnc-2025"
    / "pages"
    / "p0210"
    / "measurements.json"
)

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0210-001",
    "MEAS-CPNC-2025-P0210-002",
    "MEAS-CPNC-2025-P0210-003",
    "MEAS-CPNC-2025-P0210-004",
    "MEAS-CPNC-2025-P0210-005",
]

EXPECTED_PRIMITIVES = {
    "opening": "rect",
    "tape": "polyline",
    "frame": "polyline",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "tape", "to": "opening", "type": "measures"},
    {"from": "frame", "to": "opening", "type": "dimensioned_from"},
]

EXPECTED_LABELS = [
    ("opening", "Ejemplo visual: 209 cm de alto y 79 cm de ancho"),
    ("opening", "Medir en varias partes y trabajar con la medida menor"),
    ("frame", "Colillado: cortes a 45°"),
    ("frame", "MDP de 15 mm según la fuente"),
]

EXPECTED_ANNOTATION_IDS = [
    "ann-opening-example",
    "ann-measure-minimum",
    "ann-frame-miter",
    "ann-frame-material",
]

EXPECTED_MEASUREMENT_VALUES = {
    "MEAS-CPNC-2025-P0210-001": (209, "cm"),
    "MEAS-CPNC-2025-P0210-002": (79, "cm"),
    "MEAS-CPNC-2025-P0210-003": (5, "mm"),
    "MEAS-CPNC-2025-P0210-004": (45, "deg"),
    "MEAS-CPNC-2025-P0210-005": (15, "mm"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0210_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0210-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0210"
    assert figure["type"] == "mixed"
    assert figure["source"]["pdf_page"] == 210
    assert figure["source"]["printed_page"] == 188
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
    assert [(a["target_entity_id"], a["text"]) for a in figure["annotations"]] == EXPECTED_LABELS
    assert [a["id"] for a in figure["annotations"]] == EXPECTED_ANNOTATION_IDS
    for annotation in figure["annotations"]:
        assert annotation["placement"]["precision"] == "approximate"
        _assert_normalized(annotation["placement"]["x"])
        _assert_normalized(annotation["placement"]["y"])

    assert figure["layers"] == [
        {
            "id": "geometry",
            "order": 10,
            "entity_ids": ["opening", "tape", "frame"],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": EXPECTED_ANNOTATION_IDS,
        },
    ]


def test_p0210_fig001_preserves_source_semantics_without_metric_geometry() -> None:
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
    assert set(entities) == set(EXPECTED_PRIMITIVES)
    for entity_id, primitive in EXPECTED_PRIMITIVES.items():
        geometry = entities[entity_id]["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry["primitive"] == primitive
        assert "dimensions" not in geometry
        assert "bbox" not in geometry
        if primitive == "rect":
            bounds = geometry["bounds"]
            _assert_normalized(bounds["x"])
            _assert_normalized(bounds["y"])
            assert bounds["width"] > 0
            assert bounds["height"] > 0
            assert bounds["x"] + bounds["width"] <= 1
            assert bounds["y"] + bounds["height"] <= 1
        else:
            points = geometry["points"]
            assert len(points) >= 2
            for point in points:
                _assert_normalized(point["x"])
                _assert_normalized(point["y"])

    notes = figure["review"]["notes"]
    assert "no codifica escala física" in notes
    assert "209" in notes and "79" in notes
    assert "ejemplo" in notes.lower()
    assert "5 mm" in notes
    assert "fuente" in notes.lower()


def test_p0210_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-entity-id="opening"' in svg_first
    assert 'data-annotation-id="ann-frame-material"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
