from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0161" / "figures" / "fig-001.json"

EXPECTED_BOUNDS = {
    "ruler-body": {"x": 0.12, "y": 0.08, "width": 0.78, "height": 0.80},
    "imperial-scale": {"x": 0.15, "y": 0.08, "width": 0.75, "height": 0.42},
    "metric-scale": {"x": 0.15, "y": 0.50, "width": 0.75, "height": 0.38},
    "fraction-list": {"x": 0.00, "y": 0.05, "width": 0.22, "height": 0.90},
}

EXPECTED_ANNOTATIONS = {
    ("imperial-scale", "in"),
    ("metric-scale", "cm"),
    ("fraction-list", "1/8”, 1/4”, 5/16”, 3/8”, 1/2”, 5/8”, 3/4”, 7/8”, 1”"),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0161_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0161-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0161"
    assert figure["type"] == "illustration"
    assert figure["source"]["pdf_page"] == 161
    assert figure["source"]["printed_page"] == 139
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


def test_p0161_fig001_keeps_only_source_backed_entities_renderable_without_metric_inference() -> None:
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
            "from": "fraction-list",
            "to": "imperial-scale",
            "type": "explains_markings",
        },
        {
            "from": "imperial-scale",
            "to": "metric-scale",
            "type": "same_physical_ruler",
        },
    ]


def test_p0161_fig001_preserves_exact_labels_and_complete_layer_references() -> None:
    figure = _figure()

    assert len(figure["annotations"]) == len(EXPECTED_ANNOTATIONS)
    assert {
        (annotation["target_entity_id"], annotation["text"])
        for annotation in figure["annotations"]
    } == EXPECTED_ANNOTATIONS

    annotation_ids: set[str] = set()
    for annotation in figure["annotations"]:
        assert isinstance(annotation.get("id"), str) and annotation["id"]
        annotation_ids.add(annotation["id"])
        placement = annotation.get("placement")
        assert isinstance(placement, dict)
        assert placement["precision"] == "approximate"
        assert 0 <= placement["x"] <= 1
        assert 0 <= placement["y"] <= 1
    assert len(annotation_ids) == len(figure["annotations"])

    referenced_entities: list[str] = []
    referenced_annotations: list[str] = []
    orders: list[int] = []
    for layer in figure["layers"]:
        assert "description" not in layer
        orders.append(layer["order"])
        referenced_entities.extend(layer.get("entity_ids", []))
        referenced_annotations.extend(layer.get("annotation_ids", []))

    assert orders == sorted(orders)
    assert set(referenced_entities) == set(EXPECTED_BOUNDS)
    assert len(referenced_entities) == len(EXPECTED_BOUNDS)
    assert set(referenced_annotations) == annotation_ids
    assert len(referenced_annotations) == len(annotation_ids)


def test_p0161_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in EXPECTED_BOUNDS:
        assert first.count(f'data-entity-id="{entity_id}"') == 1
    for annotation in figure["annotations"]:
        assert first.count(f'data-annotation-id="{annotation["id"]}"') == 1
    assert ">in<" in first
    assert ">cm<" in first
    assert "1/8”" in first
    assert "1”" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
