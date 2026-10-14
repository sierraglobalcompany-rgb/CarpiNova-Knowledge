from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0138" / "figures" / "fig-001.json"


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0138_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0138-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0138"
    assert figure["type"] == "illustration"
    assert figure["source"]["pdf_page"] == 138
    assert figure["source"]["printed_page"] == 116
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
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


def test_p0138_keeps_four_source_backed_anchors_renderable_without_inventing_measurements() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == {"anchor-1", "anchor-2", "anchor-3", "anchor-4"}
    assert figure["measurements"] == []

    for entity in entities.values():
        geometry = entity["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry.get("primitive") == "polyline"
        points = geometry.get("points")
        assert isinstance(points, list) and len(points) >= 4
        assert points[0] == points[-1]
        assert all(
            0 <= point["x"] <= 1 and 0 <= point["y"] <= 1
            for point in points
        )
        assert "dimensions" not in geometry


def test_p0138_keeps_only_the_source_title_and_layer_references_resolve() -> None:
    figure = _figure()

    assert len(figure["annotations"]) == 1
    annotation = figure["annotations"][0]
    assert annotation["text"] == "CHAZOS PLÁSTICOS PARA MURO TRADICIONAL"
    assert isinstance(annotation.get("id"), str) and annotation["id"]
    assert annotation.get("placement", {}).get("precision") == "approximate"

    entity_ids = {entity["id"] for entity in figure["entities"]}
    referenced_entities: set[str] = set()
    referenced_annotations: set[str] = set()
    orders: list[int] = []
    for layer in figure["layers"]:
        assert "description" not in layer
        orders.append(layer["order"])
        referenced_entities.update(layer.get("entity_ids", []))
        referenced_annotations.update(layer.get("annotation_ids", []))

    assert orders == sorted(orders)
    assert referenced_entities == entity_ids
    assert referenced_annotations == {annotation["id"]}


def test_p0138_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in ("anchor-1", "anchor-2", "anchor-3", "anchor-4"):
        assert f'data-entity-id="{entity_id}"' in first
    assert "CHAZOS PLÁSTICOS PARA MURO TRADICIONAL" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
