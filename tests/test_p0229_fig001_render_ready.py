from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0229" / "figures" / "fig-001.json"
SOURCE_PATH = ROOT / "books" / "cpnc-2025" / "pages" / "p0229" / "source.md"

EXPECTED_PURPOSE = (
    "Recrear la estructura visual del índice de recursos QR de cocina y closet sin fabricar "
    "códigos QR funcionales ni destinos no verificados."
)
EXPECTED_ENTITIES = [
    ("qr-01", "qr_resource_placeholder", "¿Cómo estructurar una cocina?"),
    ("qr-02", "qr_resource_placeholder", "¿Cómo hacer una cocina?"),
    ("qr-03", "qr_resource_placeholder", "Cocina y bisagras"),
    ("qr-04", "qr_resource_placeholder", "Sistema T en frontal de cocina"),
    ("qr-05", "qr_resource_placeholder", "Medidas estándar de cocina"),
    ("qr-06", "qr_resource_placeholder", "Sistema chaflan cocinas"),
    ("qr-07", "qr_resource_placeholder", "Elementos fundamentales para realizar tu cocina"),
    ("qr-08", "qr_resource_placeholder", "¿Cómo cotizar una cocina?"),
    ("qr-09", "qr_resource_placeholder", "¿Cómo va estructurado un closet?"),
    ("qr-10", "qr_resource_placeholder", "¿Cómo hacer un closet?"),
    ("qr-11", "qr_resource_placeholder", "Sistema corredizo SD Simple y doble"),
    ("qr-12", "qr_resource_placeholder", "Sistema corredizo SD 50"),
]
EXPECTED_ANNOTATIONS = [
    (f"ann-{entity_id}-title", entity_id, label)
    for entity_id, _entity_type, label in EXPECTED_ENTITIES
]


def _figure() -> dict:
    return json.loads(FIGURE_PATH.read_text(encoding="utf-8"))


def _assert_normalized(value: float) -> None:
    assert 0 <= value <= 1


def test_p0229_fig001_preserves_frozen_source_semantics_and_unresolved_qr_destinations() -> None:
    figure = _figure()

    assert figure["figure_id"] == "FIG-CPNC-2025-P0229-001"
    assert figure["page_id"] == "PAGE-CPNC-2025-P0229"
    assert figure["type"] == "mixed"
    assert figure["purpose"] == EXPECTED_PURPOSE
    assert figure["source"]["pdf_page"] == 229
    assert figure["source"]["printed_page"] == 207
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert figure["relationships"] == []
    assert figure["measurements"] == []
    assert "educational_sequence" not in figure

    assert [
        (entity["id"], entity["type"], entity["label"])
        for entity in figure["entities"]
    ] == EXPECTED_ENTITIES

    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    for _entity_id, _entity_type, label in EXPECTED_ENTITIES:
        assert label in source_text

    guardrail_text = " ".join(
        [figure["review"]["notes"]]
        + [annotation["text"] for annotation in figure["annotations"]]
    ).lower()
    assert "payload" in guardrail_text
    assert "decodific" in guardrail_text
    assert "verific" in guardrail_text
    assert (
        "no funcional" in guardrail_text
        or "no se debe generar ningún qr funcional" in guardrail_text
    )

    serialized = json.dumps(figure, ensure_ascii=False).lower()
    for forbidden_destination_claim in (
        "http://",
        "https://",
        "www.",
        "whatsapp",
        "youtube",
        "vimeo",
    ):
        assert forbidden_destination_claim not in serialized
    assert '"camas"' not in serialized
    assert "separador" not in serialized


def test_p0229_fig001_declares_frozen_normalized_render_contract_and_title_annotations() -> None:
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
    assert [
        (annotation.get("id"), annotation["target_entity_id"], annotation["text"])
        for annotation in annotations
    ] == EXPECTED_ANNOTATIONS
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
    assert layers[0].get("entity_ids") == [
        entity_id for entity_id, _entity_type, _label in EXPECTED_ENTITIES
    ]
    assert layers[1].get("annotation_ids") == [
        annotation_id for annotation_id, _target, _text in EXPECTED_ANNOTATIONS
    ]

    semantic_text = " ".join(
        [
            figure["accessibility"]["summary"],
            figure["review"]["notes"],
        ]
    ).lower()
    assert "simplific" in semantic_text or "pedag" in semantic_text
    assert "no funcional" in semantic_text or "no son códigos qr" in semantic_text
    assert "métric" in semantic_text or "escala" in semantic_text
    assert "payload" in semantic_text or "destino" in semantic_text
    assert "decodific" in semantic_text
    assert "verific" in semantic_text


def test_p0229_fig001_uses_only_normalized_approximate_rect_zones_in_source_grid_order() -> None:
    figure = _figure()
    entities = {entity["id"]: entity for entity in figure["entities"]}
    expected_ids = [entity_id for entity_id, _entity_type, _label in EXPECTED_ENTITIES]

    assert list(entities) == expected_ids
    for entity_id, expected_type, expected_label in EXPECTED_ENTITIES:
        entity = entities[entity_id]
        assert entity["type"] == expected_type
        assert entity["label"] == expected_label

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

    rows = [expected_ids[index : index + 3] for index in range(0, len(expected_ids), 3)]
    for row in rows:
        x_positions = [
            entities[entity_id]["geometry"]["bounds"]["x"] for entity_id in row
        ]
        assert x_positions == sorted(x_positions)
        assert len(set(x_positions)) == 3

    for upper_row, lower_row in zip(rows, rows[1:], strict=True):
        upper_y = [
            entities[entity_id]["geometry"]["bounds"]["y"] for entity_id in upper_row
        ]
        lower_y = [
            entities[entity_id]["geometry"]["bounds"]["y"] for entity_id in lower_row
        ]
        assert max(upper_y) < min(lower_y)


def test_p0229_fig001_renders_deterministically_and_repository_stays_valid() -> None:
    figure = _figure()

    svg_first = render_normalized_2d_svg(figure)
    svg_second = render_normalized_2d_svg(figure)

    assert svg_first == svg_second
    assert svg_first.startswith("<svg")
    assert 'data-layer-id="geometry"' in svg_first
    assert 'data-layer-id="labels"' in svg_first
    for entity_id, _entity_type, _label in EXPECTED_ENTITIES:
        assert f'data-entity-id="{entity_id}"' in svg_first
    for annotation_id, _target, _text in EXPECTED_ANNOTATIONS:
        assert f'data-annotation-id="{annotation_id}"' in svg_first

    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
