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
    / "p0209"
    / "figures"
    / "fig-001.json"
)
MEASUREMENTS_PATH = (
    ROOT
    / "books"
    / "cpnc-2025"
    / "pages"
    / "p0209"
    / "measurements.json"
)

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0209-001",
    "MEAS-CPNC-2025-P0209-002",
    "MEAS-CPNC-2025-P0209-003",
    "MEAS-CPNC-2025-P0209-004",
    "MEAS-CPNC-2025-P0209-005",
    "MEAS-CPNC-2025-P0209-006",
    "MEAS-CPNC-2025-P0209-007",
]

EXPECTED_PRIMITIVES = {
    "frame": "polyline",
    "stop": "rect",
    "trim": "polyline",
    "door-leaf": "rect",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "stop", "to": "frame", "type": "part_of"},
    {"from": "trim", "to": "frame", "type": "covers_perimeter_gap"},
    {"from": "door-leaf", "to": "stop", "type": "closes_against"},
]

EXPECTED_LABELS = [
    ("frame", "Anchos listados: 8, 10, 12 o 14 cm"),
    ("stop", "Carga: 4 cm"),
    ("trim", "Moldura/tapaluz: normalmente 3 cm"),
]

EXPECTED_MEASUREMENT_VALUES = {
    "MEAS-CPNC-2025-P0209-001": (8, "cm"),
    "MEAS-CPNC-2025-P0209-002": (10, "cm"),
    "MEAS-CPNC-2025-P0209-003": (12, "cm"),
    "MEAS-CPNC-2025-P0209-004": (14, "cm"),
    "MEAS-CPNC-2025-P0209-005": (4, "cm"),
    "MEAS-CPNC-2025-P0209-006": (4, "cm"),
    "MEAS-CPNC-2025-P0209-007": (3, "cm"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0209_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0209-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0209"
    assert figure["type"] == "dimensioned_drawing"
    assert figure["source"]["pdf_page"] == 209
    assert figure["source"]["printed_page"] == 187
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
    assert [a["id"] for a in figure["annotations"]] == [
        "ann-frame-widths",
        "ann-stop-width",
        "ann-trim-width",
    ]
    for annotation in figure["annotations"]:
        assert annotation["placement"]["precision"] == "approximate"
        _assert_normalized(annotation["placement"]["x"])
        _assert_normalized(annotation["placement"]["y"])

    assert figure["layers"] == [
        {
            "id": "geometry",
            "order": 10,
            "entity_ids": ["frame", "stop", "trim", "door-leaf"],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": [
                "ann-frame-widths",
                "ann-stop-width",
                "ann-trim-width",
            ],
        },
    ]


def test_p0209_fig001_preserves_source_semantics_without_metric_geometry() -> None:
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

    assert all(not measurement_id.startswith("MEAS-CPNC-2025-P0208-") for measurement_id in figure["measurements"])

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
    assert "36 mm" in notes
    assert "P0208" in notes
    assert "no se duplica" in notes


def test_p0209_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-entity-id="frame"' in svg_first
    assert 'data-annotation-id="ann-trim-width"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
