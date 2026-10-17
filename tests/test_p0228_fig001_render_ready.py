from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0228" / "figures" / "fig-001.json"
SOURCE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0228" / "source.md"

EXPECTED_PURPOSE = (
    "Recrear la infografía de referencias estándar para escaleras conservando literalmente "
    "las cifras y etiquetas visibles sin inferir unidades ausentes."
)
EXPECTED_ENTITY_TYPES = {
    "stair-profile": "stair_side_profile",
    "formula-box": "stair_formula_reference",
    "low-traffic-pair": "tread_riser_reference_low_traffic",
    "comfort-pair": "tread_riser_reference_maximum_comfort",
    "exterior-pair": "tread_riser_reference_exterior",
    "horizontal-step": "horizontal_step_length_reference",
}
EXPECTED_RELATIONSHIPS = [
    {"from": "low-traffic-pair", "to": "stair-profile", "type": "annotates"},
    {"from": "comfort-pair", "to": "stair-profile", "type": "annotates"},
    {"from": "exterior-pair", "to": "stair-profile", "type": "annotates"},
    {"from": "horizontal-step", "to": "stair-profile", "type": "annotates"},
]
EXPECTED_LABELS = [
    (
        "formula-box",
        (
            "La fuente imprime literalmente: 2 contrahuellas + 1 huella = 0.63cm; "
            "puede variar de 0.61 a 0.65"
        ),
    ),
    ("low-traffic-pair", "Huella 0.21; contrahuella 0.21; lugares poco transitados"),
    ("comfort-pair", "Huella 0.29; contrahuella 0.17; máxima comodidad"),
    (
        "exterior-pair",
        (
            "Escaleras exteriores: huella 0.39; contrahuella 0.12; "
            "anotación superior pequeña no normalizada"
        ),
    ),
    ("horizontal-step", ".63 Longitud Horizontal de un paso"),
]
EXPECTED_ANNOTATION_IDS = {
    "ann-formula-box",
    "ann-low-traffic-pair",
    "ann-comfort-pair",
    "ann-exterior-pair",
    "ann-horizontal-step",
}


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0228_fig001_preserves_frozen_source_semantics_and_unresolved_units() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0228-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0228"
    assert figure["type"] == "mixed"
    assert figure["purpose"] == EXPECTED_PURPOSE
    assert figure["source"]["pdf_page"] == 228
    assert figure["source"]["printed_page"] == 206
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["relationships"] == EXPECTED_RELATIONSHIPS
    assert figure["measurements"] == []
    assert "educational_sequence" not in figure

    entities = {entity["id"]: entity for entity in figure["entities"]}
    assert set(entities) == set(EXPECTED_ENTITY_TYPES)
    assert {entity_id: entity["type"] for entity_id, entity in entities.items()} == EXPECTED_ENTITY_TYPES

    assert [(annotation["target_entity_id"], annotation["text"]) for annotation in figure["annotations"]] == EXPECTED_LABELS

    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    assert "2 contrahuellas + 1 huella = 0.63cm" in source_text
    assert "Puede variar de 0.61 a 0.65" in source_text
    assert ".63 Longitud Horizontal de un paso" in source_text

    serialized = json.dumps(figure, ensure_ascii=False).lower()
    for forbidden_normalization in (
        "0.63 m",
        "63 cm",
        "0.61 m",
        "0.65 m",
        "0.21 m",
        "0.29 m",
        "0.17 m",
        "0.39 m",
        "0.12 m",
    ):
        assert forbidden_normalization not in serialized


def test_p0228_fig001_declares_frozen_normalized_render_contract() -> None:
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
    assert "0.63cm" in semantic_text
    assert "fuente" in semantic_text
    assert "unidad" in semantic_text or "unidades" in semantic_text
    assert "código" in semantic_text or "norma" in semantic_text
    assert "estruct" in semantic_text
    assert "seguridad" in semantic_text or "certific" in semantic_text
    assert "calcul" in semantic_text
    assert "fabric" in semantic_text or "constru" in semantic_text or "plantilla" in semantic_text


def test_p0228_fig001_uses_only_normalized_approximate_rect_semantic_zones() -> None:
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


def test_p0228_fig001_renders_deterministically_and_repository_stays_valid() -> None:
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
