from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0158" / "figures" / "fig-001.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0158" / "measurements.json"

EXPECTED_BOUNDS = {
    "table-saw": {"x": 0.02, "y": 0.02, "width": 0.48, "height": 0.96},
    "workpiece": {"x": 0.02, "y": 0.18, "width": 0.46, "height": 0.64},
    "push-stick": {"x": 0.22, "y": 0.10, "width": 0.20, "height": 0.30},
    "blade-guard": {"x": 0.17, "y": 0.57, "width": 0.18, "height": 0.20},
    "splitter": {"x": 0.27, "y": 0.58, "width": 0.10, "height": 0.20},
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def test_p0158_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0158-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0158"
    assert figure["type"] == "process_diagram"
    assert figure["source"]["pdf_page"] == 158
    assert figure["source"]["printed_page"] == 136
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


def test_p0158_fig001_keeps_only_source_backed_safety_entities_renderable() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == set(EXPECTED_BOUNDS)
    assert figure["measurements"] == ["MEAS-CPNC-2025-P0158-001"]

    for entity_id, expected_bounds in EXPECTED_BOUNDS.items():
        geometry = entities[entity_id]["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry["primitive"] == "rect"
        assert geometry["bounds"] == expected_bounds
        assert "dimensions" not in geometry

    assert figure["relationships"] == [
        {"from": "push-stick", "to": "workpiece", "type": "pushes"},
        {"from": "blade-guard", "to": "table-saw", "type": "installed_on"},
        {"from": "splitter", "to": "table-saw", "type": "installed_behind_blade"},
    ]


def test_p0158_fig001_preserves_safety_measurement_annotations_and_layers() -> None:
    figure = _figure()
    measurement = next(
        item
        for item in _measurements()
        if item["measurement_id"] == "MEAS-CPNC-2025-P0158-001"
    )

    assert measurement["kind"] == "minimum_hand_distance_from_table_saw_blade_stated_by_source"
    assert measurement["value"] == 5
    assert measurement["unit"] == "cm"
    assert measurement["status"] == "VISUALLY_VERIFIED"

    expected_annotations = {
        ("push-stick", "Se usa el empujador"),
        ("blade-guard", "No se retira la guarda, ni el separador de corte"),
    }
    assert {
        (annotation["target_entity_id"], annotation["text"])
        for annotation in figure["annotations"]
    } == expected_annotations

    annotation_ids: set[str] = set()
    for annotation in figure["annotations"]:
        assert isinstance(annotation.get("id"), str) and annotation["id"]
        annotation_ids.add(annotation["id"])
        placement = annotation.get("placement")
        assert isinstance(placement, dict)
        assert placement["precision"] == "approximate"
        assert 0 <= placement["x"] <= 1
        assert 0 <= placement["y"] <= 1
    assert len(annotation_ids) == 2

    entity_ids = set(EXPECTED_BOUNDS)
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
    assert referenced_annotations == annotation_ids


def test_p0158_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
    for entity_id in EXPECTED_BOUNDS:
        assert f'data-entity-id="{entity_id}"' in first
    assert "Se usa el empujador" in first
    assert "No se retira la guarda, ni el separador de corte" in first

    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
