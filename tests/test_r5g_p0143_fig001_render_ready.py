from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0143" / "figures" / "fig-001.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0143" / "measurements.json"


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized_geometry(entity: dict) -> None:
    geometry = entity["geometry"]
    assert geometry["precision"] == "approximate"
    assert "dimensions" not in geometry

    primitive = geometry.get("primitive")
    assert primitive in {"rect", "line", "polyline"}

    if primitive == "rect":
        bounds = geometry.get("bounds")
        assert isinstance(bounds, dict)
        assert 0 <= bounds["x"] <= 1
        assert 0 <= bounds["y"] <= 1
        assert 0 < bounds["width"] <= 1
        assert 0 < bounds["height"] <= 1
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1
        return

    points = geometry.get("points")
    assert isinstance(points, list)
    assert len(points) == 2 if primitive == "line" else len(points) >= 2
    assert all(0 <= point["x"] <= 1 and 0 <= point["y"] <= 1 for point in points)


def test_p0143_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0143-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0143"
    assert figure["type"] == "process_diagram"
    assert figure["source"]["pdf_page"] == 143
    assert figure["source"]["printed_page"] == 121
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


def test_p0143_fig001_keeps_only_source_backed_hollow_shelf_and_multiuse_support_renderable() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == {
        "hollow-shelf",
        "internal-rear-box",
        "multiuse-shelf-piece",
        "multiuse-wall-piece",
    }
    assert figure["measurements"] == [
        "MEAS-CPNC-2025-P0143-004",
        "MEAS-CPNC-2025-P0143-005",
        "MEAS-CPNC-2025-P0143-006",
    ]

    for entity in entities.values():
        _assert_normalized_geometry(entity)

    assert entities["hollow-shelf"]["geometry"]["primitive"] in {"rect", "polyline"}
    assert entities["internal-rear-box"]["geometry"]["primitive"] in {"rect", "polyline"}
    assert entities["multiuse-shelf-piece"]["geometry"]["primitive"] in {"rect", "polyline"}
    assert entities["multiuse-wall-piece"]["geometry"]["primitive"] in {"rect", "polyline"}

    assert figure["relationships"] == [
        {"from": "multiuse-shelf-piece", "to": "multiuse-wall-piece", "type": "interlocks_with"},
        {"from": "multiuse-shelf-piece", "to": "internal-rear-box", "type": "mounted_inside"},
    ]


def test_p0143_fig001_preserves_exact_measurements_and_resolved_layer_references() -> None:
    figure = _figure()
    measurements = {
        item["measurement_id"]: item
        for item in _measurements()
        if item["measurement_id"] in set(figure["measurements"])
    }

    assert measurements["MEAS-CPNC-2025-P0143-004"]["kind"] == "board_thickness"
    assert measurements["MEAS-CPNC-2025-P0143-004"]["value"] == 15
    assert measurements["MEAS-CPNC-2025-P0143-004"]["unit"] == "mm"
    assert measurements["MEAS-CPNC-2025-P0143-005"]["kind"] == "board_thickness"
    assert measurements["MEAS-CPNC-2025-P0143-005"]["value"] == 18
    assert measurements["MEAS-CPNC-2025-P0143-005"]["unit"] == "mm"
    assert measurements["MEAS-CPNC-2025-P0143-006"]["kind"] == "perimeter_strip_approx_width"
    assert measurements["MEAS-CPNC-2025-P0143-006"]["value"] == 5
    assert measurements["MEAS-CPNC-2025-P0143-006"]["unit"] == "cm"
    assert all(item["status"] == "VISUALLY_VERIFIED" for item in measurements.values())

    assert len(figure["annotations"]) == 1
    annotation = figure["annotations"][0]
    assert annotation["target_entity_id"] == "internal-rear-box"
    assert annotation["text"] == "Caja posterior interna para ocultar el soporte multiusos."
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


def test_p0143_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    assert 'data-entity-id="hollow-shelf"' in first
    assert 'data-entity-id="internal-rear-box"' in first
    assert 'data-entity-id="multiuse-shelf-piece"' in first
    assert 'data-entity-id="multiuse-wall-piece"' in first
    assert "Caja posterior interna para ocultar el soporte multiusos." in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
