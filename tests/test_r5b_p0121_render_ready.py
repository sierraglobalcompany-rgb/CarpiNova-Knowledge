from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0121" / "figures" / "fig-001.json"


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0121_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0121-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0121"
    assert figure["source"]["pdf_page"] == 121
    assert figure["source"]["printed_page"] == 99
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


def test_p0121_renders_only_source_backed_structure_and_keeps_dimensions_unresolved() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    expected_entities = {
        "installation-title",
        "large-arm-series",
        "large-arm-label",
        "large-arm-reference",
        "mini-arm-label",
        "mini-plan",
        "mini-plan-label",
        "instruction-label",
        "mini-installation-series",
        "unresolved-dimension-labels",
    }
    assert set(entities) == expected_entities

    unresolved = entities["unresolved-dimension-labels"]
    assert unresolved["geometry"] == {"precision": "unknown"}
    assert figure["measurements"] == []
    assert figure["review"]["small_dimension_labels_resolved"] is False
    assert figure["review"]["resolved_dimensions"] == []

    for entity_id, entity in entities.items():
        if entity_id == "unresolved-dimension-labels":
            continue
        geometry = entity["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry["primitive"] in {"rect", "line", "polyline"}


def test_p0121_annotations_and_layers_are_stable_without_rendering_unresolved_dimension_entity() -> None:
    figure = _figure()
    annotations = {annotation["id"]: annotation for annotation in figure["annotations"]}

    expected_annotation_ids = {
        "ann-installation-title",
        "ann-large-arm-label",
        "ann-mini-arm-label",
        "ann-mini-plan-label",
        "ann-instruction-label",
        "ann-unresolved-dimensions",
    }
    assert set(annotations) == expected_annotation_ids
    assert all(annotation["placement"]["precision"] == "approximate" for annotation in annotations.values())
    assert annotations["ann-unresolved-dimensions"]["status"] == "UNRESOLVED_DIMENSIONS"

    rendered_entity_ids: set[str] = set()
    rendered_annotation_ids: set[str] = set()
    for layer in figure["layers"]:
        rendered_entity_ids.update(layer.get("entity_ids", []))
        rendered_annotation_ids.update(layer.get("annotation_ids", []))

    assert "unresolved-dimension-labels" not in rendered_entity_ids
    assert rendered_entity_ids == {
        entity["id"]
        for entity in figure["entities"]
        if entity["id"] != "unresolved-dimension-labels"
    }
    assert rendered_annotation_ids == expected_annotation_ids


def test_p0121_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    assert 'data-entity-id="large-arm-series"' in first
    assert 'data-entity-id="mini-plan"' in first
    assert 'data-entity-id="mini-installation-series"' in first
    assert 'data-entity-id="unresolved-dimension-labels"' not in first
    assert "Medidas para Instalación" in first
    assert "Brazo Grande" in first
    assert "Brazo mini" in first
    assert "Cotas presentes en la fuente exacta" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
