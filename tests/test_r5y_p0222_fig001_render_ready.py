from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0222" / "figures" / "fig-001.json"

EXPECTED_ENTITY_TYPES = {
    "vertical-G": "cabinet_vertical_G",
    "upper-half-moon-stop": "upper_half_moon_stop",
    "ball-joint-plate": "ball_joint_plate",
    "male-pivot-plate": "male_pivot_plate",
}

EXPECTED_PRIMITIVES = {
    "vertical-G": "rect",
    "upper-half-moon-stop": "rect",
    "ball-joint-plate": "rect",
    "male-pivot-plate": "rect",
}

EXPECTED_RELATIONSHIPS = [
    {"from": "upper-half-moon-stop", "to": "vertical-G", "type": "mounted_on"},
    {"from": "ball-joint-plate", "to": "vertical-G", "type": "mounted_on"},
    {"from": "male-pivot-plate", "to": "vertical-G", "type": "mounted_on"},
]

EXPECTED_LABELS = [
    ("vertical-G", "Vertical derecho o izquierdo en aglomerado o tríplex de 18 mm"),
    ("upper-half-moon-stop", "Tope media luna superior"),
    ("ball-joint-plate", "Platina con rótula"),
    ("male-pivot-plate", "Platina de pivote macho"),
]

EXPECTED_ANNOTATION_IDS = [
    "ann-vertical-G",
    "ann-upper-half-moon-stop",
    "ann-ball-joint-plate",
    "ann-male-pivot-plate",
]

EXPECTED_MEASUREMENTS = ["MEAS-CPNC-2025-P0222-001"]


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0222_fig001_declares_frozen_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0222-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0222"
    assert figure["type"] == "technical_diagram"
    assert figure["source"]["pdf_page"] == 222
    assert figure["source"]["printed_page"] == 200
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
            "entity_ids": [
                "vertical-G",
                "upper-half-moon-stop",
                "ball-joint-plate",
                "male-pivot-plate",
            ],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": EXPECTED_ANNOTATION_IDS,
        },
    ]


def test_p0222_fig001_preserves_source_truth_and_unresolved_values() -> None:
    figure = _figure()

    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == EXPECTED_MEASUREMENTS

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
    assert "posición relativa" in semantic_text
    assert "métric" in semantic_text
    assert "fabricación" in semantic_text

    review_notes = figure["review"]["notes"].lower()
    assert "18.4" in review_notes
    assert "76.7" in review_notes
    assert "sin unidad explícita recuperable" in review_notes

    annotation_text = " ".join(a["text"] for a in figure["annotations"])
    assert "18.4" not in annotation_text
    assert "76.7" not in annotation_text

    serialized = json.dumps(figure, ensure_ascii=False)
    for forbidden_measurement in (
        "MEAS-CPNC-2025-P0222-002",
        "MEAS-CPNC-2025-P0222-003",
        "MEAS-CPNC-2025-P0222-004",
        "MEAS-CPNC-2025-P0222-005",
        "MEAS-CPNC-2025-P0222-006",
        "MEAS-CPNC-2025-P0222-007",
    ):
        assert forbidden_measurement not in serialized


def test_p0222_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-entity-id="vertical-G"' in svg_first
    assert 'data-entity-id="upper-half-moon-stop"' in svg_first
    assert 'data-annotation-id="ann-vertical-G"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
