from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0177" / "figures" / "fig-001.json"

EXPECTED_BOUNDS = {
    "board-piece": {"x": 0.15, "y": 0.16, "width": 0.55, "height": 0.46},
    "long-edge-1": {"x": 0.15, "y": 0.16, "width": 0.55, "height": 0.03},
    "long-edge-2": {"x": 0.15, "y": 0.59, "width": 0.55, "height": 0.03},
    "short-edge-1": {"x": 0.15, "y": 0.16, "width": 0.03, "height": 0.46},
    "short-edge-2": {"x": 0.67, "y": 0.16, "width": 0.03, "height": 0.46},
    "edge-band-types": {"x": 0.05, "y": 0.70, "width": 0.90, "height": 0.24},
}

EXPECTED_MEASUREMENTS = [
    "MEAS-CPNC-2025-P0177-001",
    "MEAS-CPNC-2025-P0177-002",
    "MEAS-CPNC-2025-P0177-003",
    "MEAS-CPNC-2025-P0177-004",
    "MEAS-CPNC-2025-P0177-005",
    "MEAS-CPNC-2025-P0177-006",
]

EXPECTED_ANNOTATIONS = {
    "long-edge-1": ("ann-long-edge-1", "LARGO"),
    "short-edge-1": ("ann-short-edge-1", "ANCHO"),
    "edge-band-types": (
        "ann-edge-band-types",
        "0.45 mm · 1 mm · 1.5 mm · 2 mm",
    ),
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def test_p0177_fig001_declares_existing_normalized_render_contract() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0177-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0177"
    assert figure["type"] == "technical_diagram"
    assert figure["source"]["pdf_page"] == 177
    assert figure["source"]["printed_page"] == 155
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


def test_p0177_fig001_keeps_only_source_backed_regions_renderable() -> None:
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
        {"from": "long-edge-1", "to": "board-piece", "type": "edge_of"},
        {"from": "long-edge-2", "to": "board-piece", "type": "edge_of"},
        {"from": "short-edge-1", "to": "board-piece", "type": "edge_of"},
        {"from": "short-edge-2", "to": "board-piece", "type": "edge_of"},
        {
            "from": "edge-band-types",
            "to": "board-piece",
            "type": "can_be_applied_to_edges_of",
        },
    ]


def test_p0177_fig001_preserves_measurements_labels_and_complete_layers() -> None:
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
            "id": "piece",
            "order": 10,
            "entity_ids": ["board-piece"],
        },
        {
            "id": "edge-labels",
            "order": 20,
            "entity_ids": [
                "long-edge-1",
                "long-edge-2",
                "short-edge-1",
                "short-edge-2",
            ],
            "annotation_ids": ["ann-long-edge-1", "ann-short-edge-1"],
        },
        {
            "id": "band-types",
            "order": 30,
            "entity_ids": ["edge-band-types"],
            "annotation_ids": ["ann-edge-band-types"],
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


def test_p0177_fig001_renders_byte_deterministically_and_repository_stays_valid() -> None:
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
