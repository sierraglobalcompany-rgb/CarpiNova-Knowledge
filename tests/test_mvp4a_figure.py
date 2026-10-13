from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0113" / "figures" / "fig-001.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0113" / "measurements.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p0113_identity_and_render_contract_are_preserved() -> None:
    figure = _read_json(FIGURE_PATH)

    assert figure["figure_id"] == "FIG-CPNC-2025-P0113-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0113"
    assert figure["type"] == "technical_diagram"
    assert figure["source"]["pdf_page"] == 113
    assert figure["source"]["printed_page"] == 91

    reconstruction = figure["reconstruction"]
    assert reconstruction["preferred_renderer"] == "hybrid"
    assert reconstruction["deterministic_required"] is True
    assert reconstruction["generative_image_allowed"] is False
    assert reconstruction["render_contract"] == "normalized-2d-v1"

    assert figure["camera"] == {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
    }
    assert figure["layers"]


def test_p0113_measurement_annotations_and_statuses_are_preserved() -> None:
    figure = _read_json(FIGURE_PATH)
    measurements = _read_json(MEASUREMENTS_PATH)

    expected = {
        "MEAS-CPNC-2025-P0113-009": 13,
        "MEAS-CPNC-2025-P0113-010": 14,
        "MEAS-CPNC-2025-P0113-011": 15,
    }
    annotations_by_measurement = {
        annotation.get("measurement_id"): annotation
        for annotation in figure["annotations"]
        if annotation.get("measurement_id")
    }
    measurements_by_id = {record["measurement_id"]: record for record in measurements}

    for measurement_id, value in expected.items():
        annotation = annotations_by_measurement[measurement_id]
        assert annotation["id"]
        assert annotation["placement"]["precision"] == "approximate"
        assert measurements_by_id[measurement_id]["value"] == value
        assert measurements_by_id[measurement_id]["unit"] == "mm"
        assert measurements_by_id[measurement_id]["status"] == "VISUALLY_VERIFIED"


def test_p0113_layers_resolve_locally_and_visible_annotations_have_placement() -> None:
    figure = _read_json(FIGURE_PATH)

    entity_ids = {entity["id"] for entity in figure["entities"]}
    annotations_by_id = {annotation["id"]: annotation for annotation in figure["annotations"]}
    assert len(annotations_by_id) == len(figure["annotations"])

    for layer in figure["layers"]:
        for entity_id in layer.get("entity_ids", []):
            assert entity_id in entity_ids
        for annotation_id in layer.get("annotation_ids", []):
            assert annotation_id in annotations_by_id
            assert "placement" in annotations_by_id[annotation_id]

    cross_section = next(entity for entity in figure["entities"] if entity["id"] == "cross-section")
    assert cross_section["geometry"]["precision"] == "unknown"


def test_p0113_renderable_figure_keeps_repository_valid() -> None:
    report = validate_repository(ROOT)
    assert report["valid"] is True, report["errors"]
    assert report["errors"] == []
