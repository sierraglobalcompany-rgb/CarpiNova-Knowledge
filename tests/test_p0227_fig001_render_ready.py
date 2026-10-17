from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0227" / "figures" / "fig-001.json"
MEASUREMENTS_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0227" / "measurements.json"

EXPECTED_PURPOSE = "Recrear las fijaciones del soporte de T.V. al tablón y el sistema de chaflán mostrado por la fuente."
EXPECTED_ENTITY_TYPES = {
    "particleboard": "particleboard_panel",
    "tv-bracket": "tv_wall_mount_bracket",
    "direct-screw": "direct_fastener",
    "through-bolt": "through_fastener_with_washer",
    "wall-cleat": "wall_chamfer_piece",
    "board-cleat": "board_chamfer_piece",
}
EXPECTED_RELATIONSHIPS = [
    {"from": "tv-bracket", "to": "particleboard", "type": "fastened_to"},
    {"from": "direct-screw", "to": "particleboard", "type": "fastens"},
    {"from": "through-bolt", "to": "particleboard", "type": "passes_through"},
    {"from": "wall-cleat", "to": "board-cleat", "type": "interlocks_with"},
]
EXPECTED_MEASUREMENT_IDS = [
    "MEAS-CPNC-2025-P0227-001",
    "MEAS-CPNC-2025-P0227-002",
    "MEAS-CPNC-2025-P0227-003",
]
EXPECTED_LABELS = [
    ("direct-screw", "1 pulgada x8 según la fuente"),
    ("through-bolt", "Pasante, asegurado atrás con arandela"),
    ("wall-cleat", "Sistema de chaflán: dos piezas con corte de 45°"),
]
EXPECTED_ANNOTATION_IDS = {
    "ann-direct-screw",
    "ann-through-bolt",
    "ann-wall-cleat",
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _measurements() -> list[dict]:
    return json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0227_fig001_preserves_repaired_frozen_source_semantics() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0227-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0227"
    assert figure["type"] == "mixed"
    assert figure["purpose"] == EXPECTED_PURPOSE
    assert figure["source"]["pdf_page"] == 227
    assert figure["source"]["printed_page"] == 205
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == EXPECTED_MEASUREMENT_IDS
    assert "educational_sequence" not in figure

    entities = {entity["id"]: entity for entity in figure["entities"]}
    assert set(entities) == set(EXPECTED_ENTITY_TYPES)
    assert {entity_id: entity["type"] for entity_id, entity in entities.items()} == EXPECTED_ENTITY_TYPES

    assert [(annotation["target_entity_id"], annotation["text"]) for annotation in figure["annotations"]] == EXPECTED_LABELS

    measurements = {measurement["measurement_id"]: measurement for measurement in _measurements()}
    assert set(measurements) == set(EXPECTED_MEASUREMENT_IDS)

    pullout = measurements["MEAS-CPNC-2025-P0227-001"]
    assert pullout["kind"] == "single_screw_pullout_force_stated_by_source"
    assert pullout["value"] == 120
    assert pullout["unit"] == "kgf"
    assert pullout["applies_to"] == "un solo tornillo en aglomerado según la lámina"

    screw_length = measurements["MEAS-CPNC-2025-P0227-002"]
    assert screw_length["kind"] == "tv_support_screw_length_stated_by_source"
    assert screw_length["value"] == 1
    assert screw_length["unit"] == "in"
    assert screw_length["applies_to"] == "tornillo indicado como 1 pulgada x8 por la fuente"

    chamfer = measurements["MEAS-CPNC-2025-P0227-003"]
    assert chamfer["kind"] == "chamfer_cleat_cut_angle"
    assert chamfer["value"] == 45
    assert chamfer["unit"] == "deg"
    assert chamfer["applies_to"] == "corte de las dos piezas del sistema de chaflán"

    review_notes = figure["review"]["notes"].lower()
    assert "120 kgf" in review_notes
    assert "afirmación de la fuente" in review_notes
    assert "no se extrapola" in review_notes

    serialized = json.dumps({"figure": figure, "measurements": _measurements()}, ensure_ascii=False).lower()
    for forbidden_superseded_claim in (
        "floating-shelf",
        "floating_shelf",
        "hidden-support",
        "hidden_shelf_support",
        "toggle-anchor",
        "drywall",
        "5/16",
        "3/8",
    ):
        assert forbidden_superseded_claim not in serialized


def test_p0227_fig001_declares_repaired_frozen_normalized_render_contract() -> None:
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
    assert "120 kgf" in semantic_text
    assert "fuente" in semantic_text
    assert "tornillo" in semantic_text
    assert "45" in semantic_text
    assert "certific" in semantic_text or "verific" in semantic_text
    assert "carga segura" in semantic_text or "capacidad" in semantic_text
    assert "estruct" in semantic_text
    assert "fabric" in semantic_text or "plano" in semantic_text


def test_p0227_fig001_uses_only_normalized_approximate_rect_semantic_zones() -> None:
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


def test_p0227_fig001_renders_deterministically_and_repository_stays_valid() -> None:
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
