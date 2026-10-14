from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0124" / "figures" / "fig-001.json"


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0124_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0124-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0124"
    assert figure["source"]["pdf_page"] == 124
    assert figure["source"]["printed_page"] == 102
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


def test_p0124_keeps_source_backed_lock_geometry_renderable_without_changing_measurements() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    expected_entities = {
        "door-face",
        "door-edge",
        "face-hole",
        "edge-hole",
        "height-reference",
        "backset-reference",
    }
    assert set(entities) == expected_entities
    assert figure["measurements"] == [
        f"MEAS-CPNC-2025-P0124-{index:03d}" for index in range(1, 11)
    ]

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
            assert all(
                0 <= point["x"] <= 1 and 0 <= point["y"] <= 1
                for point in geometry["points"]
            )


def test_p0124_source_labels_are_visible_and_layer_references_resolve() -> None:
    figure = _figure()
    expected_labels = {
        "Diámetro 25mm (1 Pulgada). También 7/8.",
        "Diámetro 54mm (2 ⅛ pulgadas)",
        "Del piso hacia arriba 90cm",
        'Medida de entrada "Backset" 60mm o 70mm (2 ⅜ o 2 ¾)',
    }

    annotations = {annotation["id"]: annotation for annotation in figure["annotations"]}
    assert {annotation["text"] for annotation in annotations.values()} == expected_labels
    assert all(
        annotation["placement"]["precision"] == "approximate"
        for annotation in annotations.values()
    )

    entity_ids = {entity["id"] for entity in figure["entities"]}
    referenced_entities: set[str] = set()
    referenced_annotations: set[str] = set()
    for layer in figure["layers"]:
        referenced_entities.update(layer.get("entity_ids", []))
        referenced_annotations.update(layer.get("annotation_ids", []))

    assert referenced_entities == entity_ids
    assert referenced_annotations == set(annotations)


def test_p0124_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    assert 'data-entity-id="door-face"' in first
    assert 'data-entity-id="door-edge"' in first
    assert 'data-entity-id="face-hole"' in first
    assert 'data-entity-id="edge-hole"' in first
    assert 'data-entity-id="height-reference"' in first
    assert 'data-entity-id="backset-reference"' in first
    assert "Diámetro 25mm" in first
    assert "Diámetro 54mm" in first
    assert "90cm" in first
    assert "60mm o 70mm" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
