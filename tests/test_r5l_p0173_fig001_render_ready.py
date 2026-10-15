from __future__ import annotations

import copy
import html
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0173" / "figures" / "fig-001.json"

EXPECTED_BOUNDS = {
    "poster-field": {"x": 0.06, "y": 0.04, "width": 0.88, "height": 0.92},
    "step-label": {"x": 0.55, "y": 0.18, "width": 0.27, "height": 0.07},
    "main-title": {"x": 0.10, "y": 0.24, "width": 0.80, "height": 0.18},
    "optimization-title": {"x": 0.19, "y": 0.42, "width": 0.68, "height": 0.13},
    "mouse-icon": {"x": 0.08, "y": 0.45, "width": 0.19, "height": 0.28},
    "brand-text": {"x": 0.31, "y": 0.57, "width": 0.42, "height": 0.17},
}

EXPECTED_ANNOTATIONS = {
    "step-label": ("ann-step-label", "PASO 4"),
    "main-title": ("ann-main-title", "DESPIECE &"),
    "optimization-title": ("ann-optimization-title", "OPTIMIZACIÓN"),
    "brand-text": ("ann-brand-text", "HÁGALO EN CASA"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0173_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0173-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0173"
    assert figure["type"] == "illustration"
    assert figure["source"]["pdf_page"] == 173
    assert figure["source"]["printed_page"] == 151
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


def test_p0173_fig001_keeps_only_source_backed_regions_renderable() -> None:
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
        {"from": "step-label", "to": "main-title", "type": "above"},
        {"from": "optimization-title", "to": "main-title", "type": "below"},
        {"from": "brand-text", "to": "optimization-title", "type": "below"},
        {"from": "mouse-icon", "to": "brand-text", "type": "left_of"},
    ]


def test_p0173_fig001_preserves_exact_labels_and_complete_layer_references() -> None:
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
            "id": "background",
            "order": 10,
            "entity_ids": ["poster-field"],
        },
        {
            "id": "titles",
            "order": 20,
            "entity_ids": ["step-label", "main-title", "optimization-title"],
            "annotation_ids": ["ann-step-label", "ann-main-title", "ann-optimization-title"],
        },
        {
            "id": "lower-graphic",
            "order": 30,
            "entity_ids": ["mouse-icon", "brand-text"],
            "annotation_ids": ["ann-brand-text"],
        },
    ]


def test_p0173_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in EXPECTED_BOUNDS:
        assert first.count(f'data-entity-id="{entity_id}"') == 1
    for annotation_id, text in EXPECTED_ANNOTATIONS.values():
        assert first.count(f'data-annotation-id="{annotation_id}"') == 1
        assert f">{html.escape(text)}<" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
