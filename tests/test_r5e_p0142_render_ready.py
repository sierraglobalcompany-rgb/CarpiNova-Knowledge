from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0142" / "figures" / "fig-001.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0142" / "measurements.json"


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def test_p0142_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0142-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0142"
    assert figure["type"] == "illustration"
    assert figure["source"]["pdf_page"] == 142
    assert figure["source"]["printed_page"] == 120
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


def test_p0142_keeps_two_source_backed_bracket_pieces_renderable_without_invented_capacity() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == {"furniture-side-bracket", "wall-side-bracket"}
    assert figure["measurements"] == ["MEAS-CPNC-2025-P0142-001"]

    for entity in entities.values():
        geometry = entity["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry.get("primitive") == "polyline"
        points = geometry.get("points")
        assert isinstance(points, list) and len(points) >= 3
        assert all(
            0 <= point["x"] <= 1 and 0 <= point["y"] <= 1
            for point in points
        )
        assert "dimensions" not in geometry

    assert figure["relationships"] == [
        {
            "from": "furniture-side-bracket",
            "to": "wall-side-bracket",
            "type": "joined_by_bolt_and_nut",
        }
    ]
    assert "capacidad" not in json.dumps(figure, ensure_ascii=False).lower()


def test_p0142_preserves_source_angle_and_annotation_layer_references_resolve() -> None:
    figure = _figure()
    measurement = next(
        item
        for item in _measurements()
        if item["measurement_id"] == "MEAS-CPNC-2025-P0142-001"
    )

    assert measurement["kind"] == "bracket_angle"
    assert measurement["value"] == 90
    assert measurement["unit"] == "deg"
    assert measurement["status"] == "VISUALLY_VERIFIED"

    assert len(figure["annotations"]) == 1
    annotation = figure["annotations"][0]
    assert annotation["text"] == "GRAPA MUEBLE DE INDUMA"
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


def test_p0142_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    assert 'data-entity-id="furniture-side-bracket"' in first
    assert 'data-entity-id="wall-side-bracket"' in first
    assert "GRAPA MUEBLE DE INDUMA" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
