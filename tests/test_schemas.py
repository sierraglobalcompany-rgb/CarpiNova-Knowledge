import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from carpinova_knowledge.schema_loader import load_schema, validate_instance

SCHEMAS = [
    "source",
    "page",
    "content",
    "figure",
    "measurement",
    "rule",
    "concept",
    "lesson",
    "batch",
]
FIXTURES = Path(__file__).parent / "fixtures" / "schemas" / "valid"


def test_all_schemas_are_valid_draft_2020_12_and_accept_known_good_fixture() -> None:
    for name in SCHEMAS:
        schema = load_schema(name)
        Draft202012Validator.check_schema(schema)
        instance = json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))
        assert validate_instance(name, instance) == []


def test_source_rejects_pdf_page_zero() -> None:
    source = _fixture("source")
    source["pdf_page"] = 0
    assert validate_instance("source", source)


@pytest.mark.parametrize("field,value", [("x", -0.01), ("y", 1.01), ("width", 1.1), ("height", -0.1)])
def test_source_rejects_region_coordinates_outside_unit_interval(field: str, value: float) -> None:
    source = _fixture("source")
    source["region"][field] = value
    assert validate_instance("source", source)


def test_measurement_validated_requires_visual_verification_evidence() -> None:
    measurement = _fixture("measurement")
    measurement["status"] = "VALIDATED"
    measurement.pop("visual_verification", None)
    assert validate_instance("measurement", measurement)


def test_rule_rejects_executable_status_in_f0() -> None:
    rule = _fixture("rule")
    rule["status"] = "EXECUTABLE"
    assert validate_instance("rule", rule)


def test_learning_text_requires_source_derivation_unless_external_enrichment() -> None:
    content = _fixture("content")
    content["derived_from_content_ids"] = []
    assert validate_instance("content", content)

    content["content_type"] = "external_enrichment"
    content["external_source"] = {"title": "Hardware manual", "locator": "section 2"}
    assert validate_instance("content", content) == []


def test_figure_unknown_geometry_cannot_claim_exact_dimensions() -> None:
    figure = _fixture("figure")
    figure["entities"][0]["geometry"]["precision"] = "unknown"
    figure["entities"][0]["geometry"]["dimensions"] = {"width_mm": 100}
    assert validate_instance("figure", figure)


def test_schema_rejects_malformed_canonical_id() -> None:
    page = _fixture("page")
    page["page_id"] = "page-91"
    assert validate_instance("page", page)


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


def _normalized_2d_figure_fixture() -> dict:
    figure = _fixture("figure")
    figure["reconstruction"]["render_contract"] = "normalized-2d-v1"
    figure["camera"] = {
        "coordinate_space": "normalized_figure",
        "viewport": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0},
    }
    figure["entities"][0]["geometry"] = {
        "primitive": "rect",
        "precision": "approximate",
        "bounds": {"x": 0.1, "y": 0.2, "width": 0.4, "height": 0.2},
    }
    figure["annotations"] = [
        {
            "id": "ann-panel-1",
            "entity_id": "panel-1",
            "text": "Panel",
            "placement": {"x": 0.2, "y": 0.15, "precision": "approximate"},
        }
    ]
    figure["layers"] = [
        {
            "id": "base",
            "order": 0,
            "entity_ids": ["panel-1"],
            "annotation_ids": ["ann-panel-1"],
        }
    ]
    return figure


def test_figure_legacy_without_render_contract_stays_valid() -> None:
    figure = _fixture("figure")
    assert "render_contract" not in figure["reconstruction"]
    assert validate_instance("figure", figure) == []


def test_figure_accepts_normalized_2d_v1_contract() -> None:
    figure = _normalized_2d_figure_fixture()
    assert validate_instance("figure", figure) == []


def _mutate_invalid_normalized_2d_case(figure: dict, case: str) -> None:
    geometry = figure["entities"][0]["geometry"]
    if case == "unknown-contract":
        figure["reconstruction"]["render_contract"] = "normalized-2d-v2"
    elif case == "wrong-coordinate-space":
        figure["camera"]["coordinate_space"] = "page"
    elif case == "wrong-viewport":
        figure["camera"]["viewport"]["x"] = 0.1
    elif case == "unknown-primitive":
        geometry["primitive"] = "circle"
    elif case == "rect-missing-bounds":
        geometry.pop("bounds")
    elif case == "rect-zero-width":
        geometry["bounds"]["width"] = 0
    elif case == "rect-zero-height":
        geometry["bounds"]["height"] = 0
    elif case == "line-wrong-point-count":
        geometry.clear()
        geometry.update(
            {
                "primitive": "line",
                "precision": "approximate",
                "points": [{"x": 0.1, "y": 0.2}],
            }
        )
    elif case == "polyline-too-short":
        geometry.clear()
        geometry.update(
            {
                "primitive": "polyline",
                "precision": "approximate",
                "points": [{"x": 0.1, "y": 0.2}],
            }
        )
    elif case == "point-x-out-of-range":
        geometry.clear()
        geometry.update(
            {
                "primitive": "line",
                "precision": "approximate",
                "points": [{"x": -0.01, "y": 0.2}, {"x": 0.4, "y": 0.2}],
            }
        )
    elif case == "point-y-out-of-range":
        geometry.clear()
        geometry.update(
            {
                "primitive": "line",
                "precision": "approximate",
                "points": [{"x": 0.1, "y": 1.01}, {"x": 0.4, "y": 0.2}],
            }
        )
    elif case == "annotation-x-out-of-range":
        figure["annotations"][0]["placement"]["x"] = -0.01
    elif case == "annotation-y-out-of-range":
        figure["annotations"][0]["placement"]["y"] = 1.01
    elif case == "empty-layers":
        figure["layers"] = []
    else:
        raise AssertionError(f"unknown invalid case: {case}")


@pytest.mark.parametrize(
    "case",
    [
        "unknown-contract",
        "wrong-coordinate-space",
        "wrong-viewport",
        "unknown-primitive",
        "rect-missing-bounds",
        "rect-zero-width",
        "rect-zero-height",
        "line-wrong-point-count",
        "polyline-too-short",
        "point-x-out-of-range",
        "point-y-out-of-range",
        "annotation-x-out-of-range",
        "annotation-y-out-of-range",
        "empty-layers",
    ],
)
def test_figure_normalized_2d_v1_rejects_invalid_shape(case: str) -> None:
    figure = _normalized_2d_figure_fixture()
    _mutate_invalid_normalized_2d_case(figure, case)
    assert validate_instance("figure", figure)


def test_lesson_step_accepts_figure_references_for_visual_reuse() -> None:
    lesson = _fixture("lesson")
    lesson["steps"][0]["figure_ids"] = ["FIG-CPNC-2025-P0091-001"]
    lesson["steps"][0]["interaction"] = {"type": "highlight", "target_entity_ids": ["panel-1"]}
    assert validate_instance("lesson", lesson) == []


def test_batch_accepts_physical_pages_without_printed_numbers() -> None:
    batch = _fixture("batch")
    batch.pop("printed_pages")
    batch["pdf_pages"] = [1, 2, 3, 4, 5]
    assert validate_instance("batch", batch) == []
