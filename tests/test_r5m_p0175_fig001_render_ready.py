from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0175" / "figures" / "fig-001.json"

EXPECTED_BOUNDS = {
    "general-board": {"x": 0.05, "y": 0.12, "width": 0.35, "height": 0.34},
    "piece-layout": {"x": 0.42, "y": 0.12, "width": 0.52, "height": 0.34},
    "example-module": {"x": 0.15, "y": 0.53, "width": 0.37, "height": 0.37},
    "field-list": {"x": 0.56, "y": 0.53, "width": 0.39, "height": 0.38},
}

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0175-001",
    "MEAS-CPNC-2025-P0175-002",
    "MEAS-CPNC-2025-P0175-003",
    "MEAS-CPNC-2025-P0175-004",
    "MEAS-CPNC-2025-P0175-005",
]

EXPECTED_ANNOTATIONS = {
    "example-module": ("ann-example-module", "alto, ancho y profundidad"),
    "field-list": (
        "ann-field-list",
        "cantidad · descripción · largo · ancho · beta · tapacantos",
    ),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0175_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0175-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0175"
    assert figure["type"] == "process_diagram"
    assert figure["source"]["pdf_page"] == 175
    assert figure["source"]["printed_page"] == 153
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == EXPECTED_MEASUREMENTS
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


def test_p0175_fig001_keeps_only_source_backed_regions_renderable() -> None:
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
            "from": "general-board",
            "to": "piece-layout",
            "type": "is_decomposed_into",
        },
        {
            "from": "example-module",
            "to": "field-list",
            "type": "documented_with",
        },
    ]


def test_p0175_fig001_preserves_measurements_labels_and_complete_layers() -> None:
    figure = _figure()

    assert figure["measurements"] == EXPECTED_MEASUREMENTS
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
            "id": "board-pieces",
            "order": 10,
            "entity_ids": ["general-board", "piece-layout"],
        },
        {
            "id": "module-example",
            "order": 20,
            "entity_ids": ["example-module"],
            "annotation_ids": ["ann-example-module"],
        },
        {
            "id": "fields",
            "order": 30,
            "entity_ids": ["field-list"],
            "annotation_ids": ["ann-field-list"],
        },
    ]

    entity_refs = [
        entity_id
        for layer in figure["layers"]
        for entity_id in layer.get("entity_ids", [])
    ]
    annotation_refs = [
        annotation_id
        for layer in figure["layers"]
        for annotation_id in layer.get("annotation_ids", [])
    ]
    assert sorted(entity_refs) == sorted(EXPECTED_BOUNDS)
    assert len(entity_refs) == len(set(entity_refs))
    assert sorted(annotation_refs) == sorted(
        annotation_id for annotation_id, _ in EXPECTED_ANNOTATIONS.values()
    )
    assert len(annotation_refs) == len(set(annotation_refs))


def test_p0175_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
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
