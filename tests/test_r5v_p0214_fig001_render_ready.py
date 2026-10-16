from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0214" / "figures" / "fig-001.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0214" / "measurements.json"

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0214-001",
    "MEAS-CPNC-2025-P0214-002",
    "MEAS-CPNC-2025-P0214-003",
    "MEAS-CPNC-2025-P0214-004",
    "MEAS-CPNC-2025-P0214-005",
    "MEAS-CPNC-2025-P0214-006",
    "MEAS-CPNC-2025-P0214-007",
    "MEAS-CPNC-2025-P0214-008",
]

EXPECTED_ENTITY_TYPES = {
    "mattress": "mattress_reference",
    "bed": "bed_frame",
    "nightstands": "nightstands",
    "bed-section": "bed_material_section",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "mattress", "to": "bed", "type": "defines_bed_size"},
    {"from": "mattress", "to": "nightstands", "type": "top_height_aligned"},
]

EXPECTED_LABELS = [
    ("mattress", "Anchos: 90, 140, 160 y 180 cm; largo: 190 cm; opción 200 × 200 cm"),
    ("nightstands", "La medida del nochero es libre; la fuente recomienda alinear su altura con el colchón"),
    ("bed-section", "Calibre mínimo recomendado: 30 mm"),
]

EXPECTED_ANNOTATION_IDS = [
    "ann-mattress-sizes",
    "ann-nightstand-height",
    "ann-bed-min-caliber",
]

EXPECTED_MEASUREMENT_VALUES = {
    "MEAS-CPNC-2025-P0214-001": (90, "cm"),
    "MEAS-CPNC-2025-P0214-002": (140, "cm"),
    "MEAS-CPNC-2025-P0214-003": (160, "cm"),
    "MEAS-CPNC-2025-P0214-004": (180, "cm"),
    "MEAS-CPNC-2025-P0214-005": (190, "cm"),
    "MEAS-CPNC-2025-P0214-006": (200, "cm"),
    "MEAS-CPNC-2025-P0214-007": (200, "cm"),
    "MEAS-CPNC-2025-P0214-008": (30, "mm"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0214_fig001_declares_frozen_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0214-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0214"
    assert figure["type"] == "mixed"
    assert figure["source"]["pdf_page"] == 214
    assert figure["source"]["printed_page"] == 192
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
            "entity_ids": ["mattress", "bed", "nightstands", "bed-section"],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": EXPECTED_ANNOTATION_IDS,
        },
    ]


def test_p0214_fig001_preserves_source_semantics_with_non_metric_geometry() -> None:
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
        assert geometry.get("primitive") == "rect"
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

    notes = figure["review"]["notes"].lower()
    assert "no codifica escala física" in notes
    assert "no tienen medidas estándar" in notes or "no tiene medidas estándar" in notes
    assert "30 mm" in notes
    assert "recomend" in notes
    assert "fuente" in notes


def test_p0214_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-entity-id="mattress"' in svg_first
    assert 'data-annotation-id="ann-bed-min-caliber"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
