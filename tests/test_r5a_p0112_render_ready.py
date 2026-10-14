from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0112" / "figures" / "fig-001.json"


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0112_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0112-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0112"
    assert figure["source"]["pdf_page"] == 112
    assert figure["source"]["printed_page"] == 90
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


def test_p0112_keeps_three_source_backed_hinge_configurations_renderable() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    expected_entities = {
        "straight-hinge",
        "half-overlay-hinge",
        "inset-hinge",
        "side-straight",
        "door-straight",
        "side-half",
        "door-half",
        "side-inset",
        "door-inset",
    }
    assert set(entities) == expected_entities

    for entity in entities.values():
        geometry = entity["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry["primitive"] in {"rect", "line", "polyline"}
        if geometry["primitive"] == "rect":
            bounds = geometry["bounds"]
            assert 0 <= bounds["x"] <= 1
            assert 0 <= bounds["y"] <= 1
            assert 0 < bounds["width"] <= 1
            assert 0 < bounds["height"] <= 1
        else:
            assert len(geometry["points"]) >= 2
            assert all(0 <= point["x"] <= 1 and 0 <= point["y"] <= 1 for point in geometry["points"])


def test_p0112_source_labels_are_visible_and_layer_references_resolve() -> None:
    figure = _figure()
    expected_labels = {
        "Recta",
        "Cobertura total",
        "Semi-recta",
        "Cobertura parcial",
        "Curva",
        "Embebida",
    }

    annotations = {annotation["id"]: annotation for annotation in figure["annotations"]}
    assert {annotation["text"] for annotation in annotations.values()} == expected_labels
    assert all(annotation["placement"]["precision"] == "approximate" for annotation in annotations.values())

    entity_ids = {entity["id"] for entity in figure["entities"]}
    referenced_entities: set[str] = set()
    referenced_annotations: set[str] = set()
    for layer in figure["layers"]:
        referenced_entities.update(layer.get("entity_ids", []))
        referenced_annotations.update(layer.get("annotation_ids", []))

    assert referenced_entities == entity_ids
    assert referenced_annotations == set(annotations)


def test_p0112_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    assert 'data-entity-id="door-straight"' in first
    assert 'data-entity-id="door-half"' in first
    assert 'data-entity-id="door-inset"' in first
    assert "Cobertura total" in first
    assert "Cobertura parcial" in first
    assert "Embebida" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
