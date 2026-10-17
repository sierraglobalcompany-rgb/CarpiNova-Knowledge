from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0212" / "figures" / "fig-001.json"

EXPECTED_PURPOSE = "Recrear los pasos finales de instalación de una chapa de puerta mostrados por la fuente."
EXPECTED_ENTITY_TYPES = {
    "interior-knob": "interior_knob",
    "tapaluz": "lock_tapaluz",
    "latch": "door_latch",
    "security-screws": "security_screws",
    "door": "door_leaf",
}
EXPECTED_RELATIONSHIPS = [
    {"from": "tapaluz", "to": "interior-knob", "type": "removed_after_knob"},
    {"from": "latch", "to": "door", "type": "inserted_into"},
    {"from": "security-screws", "to": "interior-knob", "type": "secure"},
    {"from": "tapaluz", "to": "interior-knob", "type": "reinstalled_before_knob"},
]
EXPECTED_LABELS = [
    ("interior-knob", "Paso 4: sacar el pomo y retirar el tapaluz"),
    ("latch", "Insertar el pestillo en la puerta"),
    ("security-screws", "Paso 5: instalar tornillos de seguridad"),
    ("tapaluz", "Volver a poner el tapaluz y finalmente el pomo"),
]
EXPECTED_ANNOTATION_IDS = {
    "ann-interior-knob",
    "ann-latch",
    "ann-security-screws",
    "ann-tapaluz",
}
EXPECTED_SEQUENCE = [
    {"step": 4, "action": "Retirar el tapaluz e insertar el pestillo"},
    {"step": 5, "action": "Fijar tornillos de seguridad, reponer tapaluz y pomo"},
]


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0212_fig001_preserves_frozen_source_semantics() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0212-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0212"
    assert figure["type"] == "process_diagram"
    assert figure["purpose"] == EXPECTED_PURPOSE
    assert figure["source"]["pdf_page"] == 212
    assert figure["source"]["printed_page"] == 190
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["measurements"] == []
    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["educational_sequence"] == EXPECTED_SEQUENCE

    entities = {entity["id"]: entity for entity in figure["entities"]}
    assert set(entities) == set(EXPECTED_ENTITY_TYPES)
    assert {entity_id: entity["type"] for entity_id, entity in entities.items()} == EXPECTED_ENTITY_TYPES

    assert [(annotation["target_entity_id"], annotation["text"]) for annotation in figure["annotations"]] == EXPECTED_LABELS

    serialized = json.dumps(figure, ensure_ascii=False).lower()
    for forbidden_neighbor_claim in (
        "95 cm",
        "90 cm",
        "54 mm",
        "7/8",
        "torque",
        "tolerancia",
    ):
        assert forbidden_neighbor_claim not in serialized


def test_p0212_fig001_declares_frozen_normalized_render_contract() -> None:
    figure = _figure()

    reconstruction = figure["reconstruction"]
    assert reconstruction.get("render_contract") == "normalized-2d-v1"
    assert reconstruction["preferred_renderer"] == "svg"
    assert reconstruction["deterministic_required"] is True
    assert reconstruction["generative_image_allowed"] is False

    assert figure.get("camera") == {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
    }

    annotations = figure["annotations"]
    assert {annotation.get("id") for annotation in annotations} == EXPECTED_ANNOTATION_IDS
    assert len(annotations) == len(EXPECTED_ANNOTATION_IDS)
    for annotation in annotations:
        placement = annotation.get("placement")
        assert placement is not None
        assert placement["precision"] == "approximate"
        _assert_normalized(placement["x"])
        _assert_normalized(placement["y"])

    layers = figure.get("layers")
    assert isinstance(layers, list)
    assert len(layers) == 2
    assert [(layer["id"], layer["order"]) for layer in layers] == [
        ("geometry", 10),
        ("labels", 20),
    ]

    geometry_ids = layers[0].get("entity_ids")
    label_ids = layers[1].get("annotation_ids")
    assert geometry_ids is not None
    assert label_ids is not None
    assert len(geometry_ids) == len(set(geometry_ids)) == len(EXPECTED_ENTITY_TYPES)
    assert set(geometry_ids) == set(EXPECTED_ENTITY_TYPES)
    assert len(label_ids) == len(set(label_ids)) == len(EXPECTED_ANNOTATION_IDS)
    assert set(label_ids) == EXPECTED_ANNOTATION_IDS

    semantic_text = " ".join(
        [
            figure["accessibility"]["summary"],
            figure["review"]["notes"],
        ]
    ).lower()
    assert "pedag" in semantic_text or "simplific" in semantic_text
    assert "métric" in semantic_text or "escala" in semantic_text
    assert "fabricación" in semantic_text
    assert "certific" in semantic_text


def test_p0212_fig001_uses_only_normalized_approximate_rect_semantic_zones() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}

    assert set(entities) == set(EXPECTED_ENTITY_TYPES)
    for entity_id, expected_type in EXPECTED_ENTITY_TYPES.items():
        entity = entities[entity_id]
        assert entity["type"] == expected_type

        geometry = entity["geometry"]
        assert geometry["precision"] == "approximate"
        assert geometry.get("primitive") == "rect"
        assert "dimensions" not in geometry
        assert "bbox" not in geometry
        assert "scale" not in geometry

        bounds = geometry.get("bounds")
        assert bounds is not None
        _assert_normalized(bounds["x"])
        _assert_normalized(bounds["y"])
        assert bounds["width"] > 0
        assert bounds["height"] > 0
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1


def test_p0212_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-layer-id="labels"' in svg_first
    for entity_id in EXPECTED_ENTITY_TYPES:
        assert f'data-entity-id="{entity_id}"' in svg_first
    for annotation_id in EXPECTED_ANNOTATION_IDS:
        assert f'data-annotation-id="{annotation_id}"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
