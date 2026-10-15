from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0163" / "figures" / "fig-001.json"

EXPECTED_BOUNDS = {
    "rafter-square": {"x": 0.05, "y": 0.05, "width": 0.42, "height": 0.28},
    "combination-square": {"x": 0.56, "y": 0.04, "width": 0.39, "height": 0.31},
    "carpenter-square": {"x": 0.05, "y": 0.40, "width": 0.47, "height": 0.30},
    "bubble-level": {"x": 0.38, "y": 0.72, "width": 0.43, "height": 0.20},
}

EXPECTED_ANNOTATIONS = {
    "rafter-square": ("ann-rafter-square", "Escuadra Rafter"),
    "combination-square": ("ann-combination-square", "Escuadra combinada"),
    "carpenter-square": ("ann-carpenter-square", "Escuadra carpintero"),
    "bubble-level": ("ann-bubble-level", "Nivel de burbuja"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0163_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0163-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0163"
    assert figure["type"] == "illustration"
    assert figure["source"]["pdf_page"] == 163
    assert figure["source"]["printed_page"] == 141
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == []
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


def test_p0163_fig001_keeps_only_source_backed_tool_regions_renderable() -> None:
    figure = _figure()
    assert len(figure["entities"]) == len(EXPECTED_BOUNDS)
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == set(EXPECTED_BOUNDS)
    for entity_id, expected_bounds in EXPECTED_BOUNDS.items():
        geometry = entities[entity_id]["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry["primitive"] == "rect"
        assert geometry["bounds"] == expected_bounds
        assert "dimensions" not in geometry
        assert "points" not in geometry
        assert "bbox" not in geometry

    assert figure["relationships"] == [
        {
            "from": "rafter-square",
            "to": "carpenter-square",
            "type": "same_reference_group",
        },
        {
            "from": "combination-square",
            "to": "carpenter-square",
            "type": "same_reference_group",
        },
        {
            "from": "bubble-level",
            "to": "carpenter-square",
            "type": "same_reference_group",
        },
    ]


def test_p0163_fig001_preserves_exact_labels_and_complete_layer_references() -> None:
    figure = _figure()

    assert len(figure["annotations"]) == len(EXPECTED_ANNOTATIONS)
    annotations = {annotation["target_entity_id"]: annotation for annotation in figure["annotations"]}
    assert set(annotations) == set(EXPECTED_ANNOTATIONS)

    for target_entity_id, (annotation_id, text) in EXPECTED_ANNOTATIONS.items():
        annotation = annotations[target_entity_id]
        assert annotation["id"] == annotation_id
        assert annotation["text"] == text
        placement = annotation["placement"]
        assert placement["precision"] == "approximate"
        assert 0 <= placement["x"] <= 1
        assert 0 <= placement["y"] <= 1

    assert figure["layers"] == [
        {
            "id": "tools",
            "order": 10,
            "entity_ids": [
                "rafter-square",
                "combination-square",
                "carpenter-square",
                "bubble-level",
            ],
        },
        {
            "id": "labels",
            "order": 20,
            "annotation_ids": [
                "ann-rafter-square",
                "ann-combination-square",
                "ann-carpenter-square",
                "ann-bubble-level",
            ],
        },
    ]


def test_p0163_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in EXPECTED_BOUNDS:
        assert first.count(f'data-entity-id="{entity_id}"') == 1
    for annotation_id, text in EXPECTED_ANNOTATIONS.values():
        assert first.count(f'data-annotation-id="{annotation_id}"') == 1
        assert f">{text}<" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
