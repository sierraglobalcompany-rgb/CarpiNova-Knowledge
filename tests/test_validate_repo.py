from __future__ import annotations

import copy
import json
from pathlib import Path

from carpinova_knowledge.render_docs import render_page_docs
from carpinova_knowledge.validate_repo import validate_repository

FIX = Path(__file__).parent / "fixtures" / "schemas" / "valid"


def _fixture(name: str) -> dict:
    return json.loads((FIX / f"{name}.json").read_text(encoding="utf-8"))


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _valid_repo(root: Path) -> Path:
    page = _fixture("page")
    content = _fixture("content")
    figure = _fixture("figure")
    measurement = _fixture("measurement")
    rule = _fixture("rule")
    lesson = _fixture("lesson")
    page_dir = root / "books" / "cpnc-2025" / "pages" / "p0091"
    _write(page_dir / "page.json", page)
    _write(page_dir / "content.json", [content])
    _write(page_dir / "measurements.json", [measurement])
    _write(page_dir / "rules.json", [rule])
    _write(page_dir / "figures" / "fig-001.json", figure)
    render_page_docs(page_dir)
    _write(root / "lessons" / "pilot" / "lesson.json", lesson)
    _write(
        root / "books" / "cpnc-2025" / "page-map.json",
        {"book_id": "cpnc-2025", "pages": [page]},
    )
    _write(
        root / "books" / "cpnc-2025" / "index.json",
        {
            "book_id": "cpnc-2025",
            "sections": [
                {
                    "section_id": "pilot",
                    "title": "Pilot",
                    "printed_range": {"start": 88, "end": 88},
                    "physical_range": {"start": 91, "end": 91},
                }
            ],
        },
    )
    return page_dir


def _codes(report: dict) -> set[str]:
    return {e["code"] for e in report["errors"]}


def test_valid_repository_has_zero_errors(tmp_path: Path) -> None:
    _valid_repo(tmp_path)
    report = validate_repository(tmp_path)
    assert report["valid"] is True
    assert report["errors"] == []


def test_unresolved_cross_reference_is_reported(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    content = json.loads((page_dir / "content.json").read_text())
    content[0]["derived_from_content_ids"] = ["CONTENT-CPNC-2025-P0091-999"]
    _write(page_dir / "content.json", content)
    render_page_docs(page_dir)
    assert "unresolved_reference" in _codes(validate_repository(tmp_path))


def test_duplicate_ids_are_reported(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    records = json.loads((page_dir / "content.json").read_text())
    records.append(copy.deepcopy(records[0]))
    _write(page_dir / "content.json", records)
    render_page_docs(page_dir)
    assert "duplicate_id" in _codes(validate_repository(tmp_path))


def test_validated_measurement_without_visual_evidence_is_reported(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    records = json.loads((page_dir / "measurements.json").read_text())
    records[0]["status"] = "VALIDATED"
    records[0].pop("visual_verification", None)
    _write(page_dir / "measurements.json", records)
    codes = _codes(validate_repository(tmp_path))
    assert "schema_error" in codes or "measurement_visual_verification_required" in codes


def test_deterministic_figure_cannot_be_generative_image_only(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path = page_dir / "figures" / "fig-001.json"
    figure = json.loads(path.read_text())
    figure["reconstruction"] = {
        "preferred_renderer": "image",
        "deterministic_required": True,
        "generative_image_allowed": True,
    }
    _write(path, figure)
    assert "deterministic_figure_generative_only" in _codes(validate_repository(tmp_path))


def test_page_id_must_match_pdf_page(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    page = json.loads((page_dir / "page.json").read_text())
    page["pdf_page"] = 92
    _write(page_dir / "page.json", page)
    assert "page_identity_mismatch" in _codes(validate_repository(tmp_path))


def test_generated_markdown_must_be_fresh(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    (page_dir / "learning.md").write_text("stale", encoding="utf-8")
    assert "stale_generated_markdown" in _codes(validate_repository(tmp_path))


def test_source_region_cannot_leave_page(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path = page_dir / "figures" / "fig-001.json"
    figure = json.loads(path.read_text())
    figure["source"]["region"]["x"] = 0.8
    figure["source"]["region"]["width"] = 0.4
    _write(path, figure)
    assert "source_region_out_of_bounds" in _codes(validate_repository(tmp_path))


def test_external_enrichment_requires_external_source(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    content = json.loads((page_dir / "content.json").read_text())
    content[0]["content_type"] = "external_enrichment"
    content[0].pop("external_source", None)
    _write(page_dir / "content.json", content)
    render_page_docs(page_dir)
    assert "schema_error" in _codes(validate_repository(tmp_path))


def test_lesson_figure_reference_must_resolve(tmp_path: Path) -> None:
    _valid_repo(tmp_path)
    lesson_path = tmp_path / "lessons" / "pilot" / "lesson.json"
    lesson = json.loads(lesson_path.read_text())
    lesson["steps"][0]["figure_ids"] = ["FIG-CPNC-2025-P0091-999"]
    _write(lesson_path, lesson)
    report = validate_repository(tmp_path)
    assert "unresolved_reference" in _codes(report)


def test_page_map_rejects_duplicate_verified_printed_page(tmp_path: Path) -> None:
    _valid_repo(tmp_path)
    path = tmp_path / "books" / "cpnc-2025" / "page-map.json"
    page_map = json.loads(path.read_text())
    duplicate = copy.deepcopy(page_map["pages"][0])
    duplicate["page_id"] = "PAGE-CPNC-2025-P0092"
    duplicate["pdf_page"] = 92
    page_map["pages"].append(duplicate)
    _write(path, page_map)
    assert "duplicate_verified_printed_page" in _codes(validate_repository(tmp_path))


def _render_ready_figure(page_dir: Path) -> tuple[Path, dict]:
    path = page_dir / "figures" / "fig-001.json"
    figure = json.loads(path.read_text(encoding="utf-8"))
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
            "measurement_id": "MEAS-CPNC-2025-P0091-001",
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
    _write(path, figure)
    return path, figure


def test_valid_render_contract_repository_has_zero_errors(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    _render_ready_figure(page_dir)
    report = validate_repository(tmp_path)
    assert report["valid"] is True
    assert report["errors"] == []


def test_render_contract_unknown_layer_entity_is_reported(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["layers"][0]["entity_ids"] = ["missing-panel"]
    _write(path, figure)
    assert "render_contract_unknown_layer_entity" in _codes(validate_repository(tmp_path))


def test_render_contract_unknown_layer_annotation_is_reported(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["layers"][0]["annotation_ids"] = ["missing-annotation"]
    _write(path, figure)
    assert "render_contract_unknown_layer_annotation" in _codes(validate_repository(tmp_path))


def test_render_contract_duplicate_annotation_id_is_reported(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["annotations"].append(copy.deepcopy(figure["annotations"][0]))
    _write(path, figure)
    assert "render_contract_duplicate_annotation_id" in _codes(validate_repository(tmp_path))


def test_render_contract_visible_annotation_requires_placement(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["annotations"][0].pop("placement")
    _write(path, figure)
    assert "render_contract_visible_annotation_missing_placement" in _codes(validate_repository(tmp_path))


def test_render_contract_layer_member_cannot_repeat_across_layers(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["layers"].append({"id": "duplicate", "order": 1, "entity_ids": ["panel-1"]})
    _write(path, figure)
    assert "render_contract_duplicate_layer_member" in _codes(validate_repository(tmp_path))


def test_render_contract_annotation_measurement_reference_must_resolve(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["annotations"][0]["measurement_id"] = "MEAS-CPNC-2025-P0091-999"
    _write(path, figure)
    assert "unresolved_reference" in _codes(validate_repository(tmp_path))


def test_render_contract_annotation_entity_reference_must_resolve(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["annotations"][0]["entity_id"] = "missing-panel"
    _write(path, figure)
    assert "unresolved_reference" in _codes(validate_repository(tmp_path))


def test_render_contract_rect_bounds_must_fit_viewport(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    path, figure = _render_ready_figure(page_dir)
    figure["entities"][0]["geometry"]["bounds"] = {
        "x": 0.8,
        "y": 0.2,
        "width": 0.4,
        "height": 0.2,
    }
    _write(path, figure)
    assert "render_contract_bounds_out_of_view" in _codes(validate_repository(tmp_path))


def _lesson_path(root: Path) -> Path:
    return root / "lessons" / "pilot" / "lesson.json"


def test_highlight_interaction_target_must_exist_in_step_figure(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    _render_ready_figure(page_dir)
    path = _lesson_path(tmp_path)
    lesson = json.loads(path.read_text(encoding="utf-8"))
    lesson["steps"][0]["figure_ids"] = ["FIG-CPNC-2025-P0091-001"]
    lesson["steps"][0]["interaction"] = {
        "type": "highlight",
        "target_entity_ids": ["missing-panel"],
    }
    _write(path, lesson)
    assert "interaction_unresolved_entity_target" in _codes(validate_repository(tmp_path))


def test_measurement_highlight_must_belong_to_step_figure(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    _render_ready_figure(page_dir)
    measurements_path = page_dir / "measurements.json"
    measurements = json.loads(measurements_path.read_text(encoding="utf-8"))
    second = copy.deepcopy(measurements[0])
    second["measurement_id"] = "MEAS-CPNC-2025-P0091-002"
    measurements.append(second)
    _write(measurements_path, measurements)

    path = _lesson_path(tmp_path)
    lesson = json.loads(path.read_text(encoding="utf-8"))
    lesson["steps"][0]["figure_ids"] = ["FIG-CPNC-2025-P0091-001"]
    lesson["steps"][0]["interaction"] = {
        "type": "highlight_measurements",
        "measurement_ids": ["MEAS-CPNC-2025-P0091-002"],
    }
    _write(path, lesson)
    assert "interaction_unresolved_measurement_target" in _codes(validate_repository(tmp_path))


def test_identify_parts_source_content_must_belong_to_step(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    content_path = page_dir / "content.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    second = copy.deepcopy(content[0])
    second["content_id"] = "CONTENT-CPNC-2025-P0091-002"
    second["derived_from_content_ids"] = [second["content_id"]]
    content.append(second)
    _write(content_path, content)
    render_page_docs(page_dir)

    path = _lesson_path(tmp_path)
    lesson = json.loads(path.read_text(encoding="utf-8"))
    lesson["source_content_ids"].append(second["content_id"])
    lesson["steps"][0]["interaction"] = {
        "type": "identify_parts",
        "source_content_id": second["content_id"],
        "parts": [{"label": "Parte", "installation_location": "Ubicación"}],
    }
    _write(path, lesson)
    assert "interaction_source_content_not_in_step" in _codes(validate_repository(tmp_path))


def test_guided_sequence_content_must_belong_to_step(tmp_path: Path) -> None:
    page_dir = _valid_repo(tmp_path)
    content_path = page_dir / "content.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    second = copy.deepcopy(content[0])
    second["content_id"] = "CONTENT-CPNC-2025-P0091-002"
    second["derived_from_content_ids"] = [second["content_id"]]
    content.append(second)
    _write(content_path, content)
    render_page_docs(page_dir)

    path = _lesson_path(tmp_path)
    lesson = json.loads(path.read_text(encoding="utf-8"))
    lesson["source_content_ids"].append(second["content_id"])
    lesson["steps"][0]["interaction"] = {
        "type": "guided_sequence",
        "sequence": [
            {
                "order": 1,
                "content_id": second["content_id"],
                "measurement_ids": ["MEAS-CPNC-2025-P0091-001"],
            }
        ],
    }
    _write(path, lesson)
    assert "interaction_sequence_content_not_in_step" in _codes(validate_repository(tmp_path))


def test_guided_sequence_measurement_reference_must_resolve(tmp_path: Path) -> None:
    _valid_repo(tmp_path)
    path = _lesson_path(tmp_path)
    lesson = json.loads(path.read_text(encoding="utf-8"))
    lesson["steps"][0]["interaction"] = {
        "type": "guided_sequence",
        "sequence": [
            {
                "order": 1,
                "content_id": "CONTENT-CPNC-2025-P0091-001",
                "measurement_ids": ["MEAS-CPNC-2025-P0091-999"],
            }
        ],
    }
    _write(path, lesson)
    assert "unresolved_reference" in _codes(validate_repository(tmp_path))


def test_guided_sequence_order_must_be_unique(tmp_path: Path) -> None:
    _valid_repo(tmp_path)
    path = _lesson_path(tmp_path)
    lesson = json.loads(path.read_text(encoding="utf-8"))
    lesson["steps"][0]["interaction"] = {
        "type": "guided_sequence",
        "sequence": [
            {
                "order": 1,
                "content_id": "CONTENT-CPNC-2025-P0091-001",
                "measurement_ids": ["MEAS-CPNC-2025-P0091-001"],
            },
            {
                "order": 1,
                "content_id": "CONTENT-CPNC-2025-P0091-001",
                "measurement_ids": ["MEAS-CPNC-2025-P0091-001"],
            },
        ],
    }
    _write(path, lesson)
    assert "interaction_duplicate_sequence_order" in _codes(validate_repository(tmp_path))
