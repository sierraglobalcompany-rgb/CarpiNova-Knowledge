from __future__ import annotations

import json
from pathlib import Path

import pytest

from carpinova_knowledge.render_figure import render_normalized_2d_svg
from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {
    "p0253": ROOT / "books/cpnc-2025/pages/p0253/figures/fig-001.json",
    "p0256": ROOT / "books/cpnc-2025/pages/p0256/figures/fig-001.json",
}
EXPECTED = {
    "p0253": {
        "figure_id": "FIG-CPNC-2025-P0253-001",
        "page_id": "PAGE-CPNC-2025-P0253",
        "pdf_page": 253,
        "printed_page": 231,
        "type": "mixed",
        "visual_id": "VIS-P0253-001",
        "entities": [
            ("title", "title_block", "Título ¿PARA QUÉ SIRVE LA ORDEN DE PRODUCCIÓN?."),
            (
                "environment-design",
                "before_after_design_block",
                "Bloque DISEÑO DEL AMBIENTE con representación ANTES y DESPUÉS de un centro de entretenimiento.",
            ),
            (
                "materials-list",
                "materials_block",
                "Bloque LISTA DE MATERIALES con tablero, tornillería y adhesivo.",
            ),
            (
                "installation-left",
                "installation_observations_block",
                "Primer bloque visible OBSERVACIONES Y CARACTERÍSTICAS DE INSTALACIÓN con módulo, adhesivo y elementos de fijación.",
            ),
            (
                "installation-right",
                "installation_observations_block",
                "Segundo bloque visible OBSERVACIONES Y CARACTERÍSTICAS DE INSTALACIÓN con MURO y distintos anclajes.",
            ),
            (
                "delivery-checklist",
                "delivery_checklist_block",
                "Bloque LISTA DE CHEQUEO DE ENTREGA con carpeta ANTICIPO, documento AVANCES, lista de chequeo e identificación.",
            ),
            (
                "satisfaction",
                "satisfaction_survey_block",
                "Bloque ENCUESTA DE SATISFACCIÓN con PUNTUALIDAD, LIMPIEZA e INSTALACIÓN.",
            ),
            ("operators", "operators_data_block", "Rótulo DATOS DE LOS OPERARIOS."),
            (
                "conclusion",
                "conclusion_text",
                "Texto final: La orden de producción evita confusiones y garantiza una experiencia profesional.",
            ),
        ],
        "relationships": [
            {"from": "title", "to": "environment-design", "type": "introduces"},
            {"from": "title", "to": "materials-list", "type": "introduces"},
            {
                "from": "environment-design",
                "to": "installation-left",
                "type": "visually_followed_by",
            },
            {
                "from": "materials-list",
                "to": "installation-right",
                "type": "visually_followed_by",
            },
            {
                "from": "installation-left",
                "to": "delivery-checklist",
                "type": "visually_followed_by",
            },
            {
                "from": "installation-right",
                "to": "satisfaction",
                "type": "visually_followed_by",
            },
            {"from": "satisfaction", "to": "operators", "type": "visually_followed_by"},
            {"from": "operators", "to": "conclusion", "type": "visually_followed_by"},
        ],
        "annotations": [
            ("ann-title", "title", "¿PARA QUÉ SIRVE LA ORDEN DE PRODUCCIÓN?"),
            (
                "ann-environment-design",
                "environment-design",
                "DISEÑO DEL AMBIENTE / ANTES / DESPUÉS",
            ),
            ("ann-materials-list", "materials-list", "LISTA DE MATERIALES"),
            (
                "ann-installation-left",
                "installation-left",
                "OBSERVACIONES Y CARACTERÍSTICAS DE INSTALACIÓN",
            ),
            (
                "ann-installation-right",
                "installation-right",
                "OBSERVACIONES Y CARACTERÍSTICAS DE INSTALACIÓN / MURO",
            ),
            (
                "ann-delivery-checklist",
                "delivery-checklist",
                "LISTA DE CHEQUEO DE ENTREGA / ANTICIPO / AVANCES",
            ),
            (
                "ann-satisfaction",
                "satisfaction",
                "ENCUESTA DE SATISFACCIÓN / PUNTUALIDAD / LIMPIEZA / INSTALACIÓN",
            ),
            ("ann-operators", "operators", "DATOS DE LOS OPERARIOS"),
            (
                "ann-conclusion",
                "conclusion",
                "La orden de producción evita confusiones y garantiza una experiencia profesional.",
            ),
        ],
        "sequence": [
            {
                "step": 1,
                "show_entity_ids": ["title", "environment-design", "materials-list"],
                "instruction": "Presentar el propósito de la orden de producción y sus bloques de diseño y materiales.",
            },
            {
                "step": 2,
                "show_entity_ids": ["installation-left", "installation-right"],
                "instruction": "Mostrar las observaciones de instalación conservando los dos encabezados visibles en la fuente.",
            },
            {
                "step": 3,
                "show_entity_ids": ["delivery-checklist", "satisfaction"],
                "instruction": "Mostrar controles de entrega, avances y satisfacción del cliente.",
            },
            {
                "step": 4,
                "show_entity_ids": ["operators", "conclusion"],
                "instruction": "Cerrar con los datos de operarios y el mensaje de reducción de confusiones y profesionalismo.",
            },
        ],
    },
    "p0256": {
        "figure_id": "FIG-CPNC-2025-P0256-001",
        "page_id": "PAGE-CPNC-2025-P0256",
        "pdf_page": 256,
        "printed_page": 234,
        "type": "process_diagram",
        "visual_id": "VIS-P0256-001",
        "entities": [
            ("title", "title_block", "Título ¿Cómo se entrega un proyecto de carpintería?"),
            (
                "manual",
                "manual_use_block",
                "1 Entrega con manual de uso; ilustración de manual con texto MANUAL DE USO y Limpiar con producto adecuado.",
            ),
            (
                "photo",
                "photo_social_block",
                "2 Registro fotográfico y para redes sociales; persona fotografiando el proyecto junto al cliente.",
            ),
            (
                "warranty",
                "warranty_after_sales_block",
                "3 Carta de garantía y servicio posventa; carta con GARANTÍA 1 AÑO y calendario JUN.",
            ),
            (
                "alerts",
                "follow_up_alerts_block",
                "4 Programa alertas para seguimiento; calendario y tabla con Fecha y Tipo...",
            ),
            (
                "summary",
                "summary_block",
                "Entrega un manual, registro visual, carta de garantía y ofrece servicio posventa.",
            ),
        ],
        "relationships": [
            {"from": "title", "to": "manual", "type": "introduces"},
            {"from": "manual", "to": "photo", "type": "sequence"},
            {"from": "photo", "to": "warranty", "type": "sequence"},
            {"from": "warranty", "to": "alerts", "type": "sequence"},
            {"from": "alerts", "to": "summary", "type": "summarized_by"},
        ],
        "annotations": [
            ("ann-title", "title", "¿Cómo se entrega un proyecto de carpintería?"),
            ("ann-manual", "manual", "1 Entrega con manual de uso"),
            ("ann-photo", "photo", "2 Registro fotográfico y para redes sociales"),
            ("ann-warranty", "warranty", "3 Carta de garantía y servicio posventa"),
            ("ann-alerts", "alerts", "4 Programa alertas para seguimiento"),
            (
                "ann-summary",
                "summary",
                "Entrega un manual, registro visual, carta de garantía y ofrece servicio posventa",
            ),
        ],
        "sequence": [
            {
                "step": 1,
                "show_entity_ids": ["title", "manual"],
                "instruction": "Presentar la entrega con manual de uso.",
            },
            {
                "step": 2,
                "show_entity_ids": ["photo"],
                "instruction": "Registrar visualmente el proyecto y su entrega.",
            },
            {
                "step": 3,
                "show_entity_ids": ["warranty"],
                "instruction": "Formalizar garantía y servicio posventa.",
            },
            {
                "step": 4,
                "show_entity_ids": ["alerts", "summary"],
                "instruction": "Programar seguimiento y cerrar con el resumen visual.",
            },
        ],
    },
}


def _figure(page: str) -> dict:
    return json.loads(FIGURES[page].read_text(encoding="utf-8"))


@pytest.mark.parametrize("page", FIGURES)
def test_batch_preserves_source_identity_and_distribution(page: str) -> None:
    figure = _figure(page)
    expected = EXPECTED[page]
    inventory_path = FIGURES[page].parents[1] / "visual-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    distribution = json.loads(
        (ROOT / "books/cpnc-2025/distribution.json").read_text(encoding="utf-8")
    )

    assert figure["figure_id"] == expected["figure_id"]
    assert figure["page_id"] == expected["page_id"]
    assert figure["type"] == expected["type"]
    assert figure["source"]["book_id"] == "cpnc-2025"
    assert figure["source"]["pdf_page"] == expected["pdf_page"]
    assert figure["source"]["printed_page"] == expected["printed_page"]
    assert figure["source"]["extraction"]["review_status"] == "VISUALLY_VERIFIED"
    assert figure["review"]["status"] == "VISUALLY_VERIFIED"
    assert inventory["inspection_status"] == "VISUALLY_VERIFIED"
    assert inventory["visuals"][0]["inventory_id"] == expected["visual_id"]
    assert inventory["visuals"][0]["figure_id"] == expected["figure_id"]
    assert expected["pdf_page"] not in distribution["exclude_pdf_pages"]
    assert figure["measurements"] == []


@pytest.mark.parametrize("page", FIGURES)
def test_batch_preserves_semantics_sequence_and_source_text(page: str) -> None:
    figure = _figure(page)
    expected = EXPECTED[page]
    source = FIGURES[page].parents[1] / "source.md"
    source_text = source.read_text(encoding="utf-8")

    assert [
        (entity["id"], entity["type"], entity["description"])
        for entity in figure["entities"]
    ] == expected["entities"]
    assert figure["relationships"] == expected["relationships"]
    assert figure["educational_sequence"] == expected["sequence"]
    original_annotations = expected["annotations"]
    if page == "p0256":
        original_annotations = [
            annotation for annotation in original_annotations if annotation[1] != "title"
        ]
        source_annotations = [
            annotation
            for annotation in figure["annotations"]
            if annotation["target_entity_id"] != "title"
        ]
    else:
        source_annotations = figure["annotations"]
    assert [
        (annotation["target_entity_id"], annotation["text"])
        for annotation in source_annotations
    ] == [(target, text) for _annotation_id, target, text in original_annotations]

    for _annotation_id, _target, text in expected["annotations"]:
        for source_fragment in text.split(" / "):
            assert source_fragment in source_text

    if page == "p0253":
        heading = "OBSERVACIONES Y CARACTERÍSTICAS DE INSTALACIÓN"
        assert source_text.count(heading) == 2
        assert sum(heading in annotation["text"] for annotation in figure["annotations"]) == 2
        assert "La orden de producción evita confusiones y garantiza una experiencia profesional." in source_text
    else:
        for visible_text in (
            "MANUAL DE USO",
            "Limpiar con producto adecuado",
            "GARANTÍA 1 AÑO",
            "JUN",
            "Fecha",
            "Tipo...",
        ):
            assert visible_text in source_text
            assert visible_text in json.dumps(figure, ensure_ascii=False)
        action_targets = {"manual", "photo", "warranty", "alerts"}
        actions = [
            text
            for _annotation_id, target, text in expected["annotations"]
            if target in action_targets
        ]
        assert actions == [
            "1 Entrega con manual de uso",
            "2 Registro fotográfico y para redes sociales",
            "3 Carta de garantía y servicio posventa",
            "4 Programa alertas para seguimiento",
        ]


@pytest.mark.parametrize("page", FIGURES)
def test_batch_declares_normalized_contract_and_camera(page: str) -> None:
    figure = _figure(page)
    reconstruction = figure["reconstruction"]

    assert reconstruction.get("render_contract") == "normalized-2d-v1"
    assert reconstruction["preferred_renderer"] == "svg"
    assert reconstruction["deterministic_required"] is True
    assert reconstruction["generative_image_allowed"] is False
    assert figure["camera"] == {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
    }
    if page == "p0256":
        assert "no implica una obligación legal vigente" in figure["review"]["notes"]


@pytest.mark.parametrize("page", FIGURES)
def test_batch_uses_complete_normalized_geometry_and_layers(page: str) -> None:
    figure = _figure(page)
    expected = EXPECTED[page]

    entity_ids = [entity["id"] for entity in figure["entities"]]
    assert len(entity_ids) == len(set(entity_ids))

    for entity in figure["entities"]:
        geometry = entity["geometry"]
        assert geometry["primitive"] == "rect"
        assert geometry["precision"] == "approximate"
        assert "bounding_box" not in geometry
        bounds = geometry["bounds"]
        assert 0 <= bounds["x"] <= 1
        assert 0 <= bounds["y"] <= 1
        assert bounds["width"] > 0
        assert bounds["height"] > 0
        assert bounds["x"] + bounds["width"] <= 1
        assert bounds["y"] + bounds["height"] <= 1

    annotation_ids = [annotation["id"] for annotation in figure["annotations"]]
    assert len(annotation_ids) == len(set(annotation_ids))
    assert len(set(entity_ids + annotation_ids)) == len(entity_ids + annotation_ids)
    entity_id_set = set(entity_ids)
    assert [
        (annotation["id"], annotation["target_entity_id"], annotation["text"])
        for annotation in figure["annotations"]
    ] == expected["annotations"]
    for annotation in figure["annotations"]:
        assert annotation["target_entity_id"] in entity_id_set
        placement = annotation["placement"]
        assert placement["precision"] == "approximate"
        assert 0 <= placement["x"] <= 1
        assert 0 <= placement["y"] <= 1

    assert figure["layers"] == [
        {"id": "geometry", "order": 10, "entity_ids": entity_ids},
        {"id": "labels", "order": 20, "annotation_ids": annotation_ids},
    ]
    guardrail = " ".join(
        [figure["accessibility"]["summary"], figure["review"]["notes"]]
    ).lower()
    assert "zonas normalizadas son semánticas" in guardrail
    assert "no métricas" in guardrail
    assert "no están a escala" in guardrail


@pytest.mark.parametrize("page", FIGURES)
def test_batch_renders_all_semantics_deterministically(page: str) -> None:
    figure = _figure(page)
    assert figure["reconstruction"].get("render_contract") == "normalized-2d-v1"

    first = render_normalized_2d_svg(figure)
    second = render_normalized_2d_svg(figure)

    assert first == second
    assert first.startswith("<svg")
    assert 'data-layer-id="geometry"' in first
    assert 'data-layer-id="labels"' in first
    for entity in figure["entities"]:
        assert f'data-entity-id="{entity["id"]}"' in first
    for annotation in figure["annotations"]:
        assert f'data-annotation-id="{annotation["id"]}"' in first
        assert annotation["text"] in first


def test_batch_repository_stays_valid() -> None:
    validation = validate_repository(ROOT)
    assert validation["valid"] is True
    assert validation["error_count"] == 0
    assert validation["errors"] == []
