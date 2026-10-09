from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

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
