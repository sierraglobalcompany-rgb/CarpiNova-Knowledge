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


def test_lesson_step_accepts_figure_references_for_visual_reuse() -> None:
    lesson = _fixture("lesson")
    lesson["steps"][0]["figure_ids"] = ["FIG-CPNC-2025-P0091-001"]
    lesson["steps"][0]["interaction"] = {"type": "highlight", "target_entity_ids": ["panel-1"]}
    assert validate_instance("lesson", lesson) == []
