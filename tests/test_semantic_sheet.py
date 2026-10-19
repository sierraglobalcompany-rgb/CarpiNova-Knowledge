from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.schema_loader import validate_instance

ROOT = Path(__file__).resolve().parents[1]


def _sheet_fixture() -> dict:
    figure = json.loads((ROOT / "tests/fixtures/schemas/valid/figure.json").read_text(encoding="utf-8"))
    figure["type"] = "table"
    figure["reconstruction"].update(
        preferred_renderer="html",
        deterministic_required=True,
        generative_image_allowed=False,
        render_contract="semantic-sheet-v1",
    )
    figure["entities"] = [
        {
            "id": "title",
            "type": "sheet_title",
            "geometry": {"precision": "approximate"},
            "text": "PRESUPUESTO",
        },
        {
            "id": "grid",
            "type": "sheet_table",
            "geometry": {"precision": "approximate"},
            "caption": "PRESUPUESTO",
            "headers": ["", "INGRESOS", "EGRESOS"],
            "column_groups": [{"label": "SEMANA 1", "start_column": 1, "span": 2}],
            "sections": [
                {
                    "id": "week-1",
                    "heading": "",
                    "rows": [["TOTAL", "$ 1", ""]],
                    "merged_cells": [],
                }
            ],
        },
    ]
    return figure


def test_semantic_sheet_contract_accepts_grouped_headers_and_source_blanks() -> None:
    assert validate_instance("figure", _sheet_fixture()) == []


def test_legacy_figure_without_render_contract_remains_valid() -> None:
    figure = json.loads((ROOT / "tests/fixtures/schemas/valid/figure.json").read_text(encoding="utf-8"))
    assert validate_instance("figure", figure) == []


def test_semantic_sheet_schema_rejects_unknown_entity_fields() -> None:
    figure = _sheet_fixture()
    figure["entities"][1]["unexpected"] = True
    assert validate_instance("figure", figure)


def test_semantic_sheet_schema_rejects_fields_from_another_entity_kind() -> None:
    figure = _sheet_fixture()
    figure["entities"][0]["role"] = "subtitle"
    assert validate_instance("figure", figure)


def test_semantic_sheet_schema_rejects_non_string_cells() -> None:
    figure = _sheet_fixture()
    figure["entities"][1]["sections"][0]["rows"][0][1] = 1
    assert validate_instance("figure", figure)


def test_semantic_sheet_schema_rejects_invalid_color_tokens() -> None:
    figure = _sheet_fixture()
    figure["entities"].append(
        {
            "id": "legend",
            "type": "sheet_legend",
            "geometry": {"precision": "approximate"},
            "entries": [{"label": "DESPIECE", "code": "D", "color": "blue"}],
        }
    )
    assert validate_instance("figure", figure)


def test_semantic_sheet_schema_rejects_partial_column_groups() -> None:
    figure = _sheet_fixture()
    figure["entities"][1]["column_groups"][0]["span"] = 1
    from carpinova_knowledge.validate_repo import _validate_semantic_sheet

    errors = []
    _validate_semantic_sheet(figure, Path("figure.json"), errors)
    assert any(error["code"] == "semantic_sheet_column_groups_incomplete" for error in errors)


def test_semantic_sheet_rejects_row_width_mismatch() -> None:
    from carpinova_knowledge.validate_repo import _validate_semantic_sheet

    figure = _sheet_fixture()
    figure["entities"][1]["sections"][0]["rows"][0].pop()
    errors = []
    _validate_semantic_sheet(figure, Path("figure.json"), errors)
    assert any(error["code"] == "semantic_sheet_row_width_mismatch" for error in errors)


def test_semantic_sheet_rejects_merges_that_hide_nonblank_source_cells() -> None:
    from carpinova_knowledge.validate_repo import _validate_semantic_sheet

    figure = _sheet_fixture()
    section = figure["entities"][1]["sections"][0]
    section["merged_cells"] = [{"row": 0, "start_column": 0, "colspan": 2}]
    errors = []
    _validate_semantic_sheet(figure, Path("figure.json"), errors)
    assert any(error["code"] == "semantic_sheet_merge_discards_source_cell" for error in errors)


def test_source_sheets_preserve_required_shapes_and_literals() -> None:
    figures = {
        number: json.loads(
            (ROOT / f"books/cpnc-2025/pages/p{number:04d}/figures/fig-001.json").read_text(encoding="utf-8")
        )
        for number in (257, 269, 270)
    }
    for figure in figures.values():
        assert figure["reconstruction"]["render_contract"] == "semantic-sheet-v1"
        assert validate_instance("figure", figure) == []
        from carpinova_knowledge.validate_repo import _validate_semantic_sheet

        errors = []
        _validate_semantic_sheet(figure, Path("figure.json"), errors)
        assert errors == []

    calendar = figures[257]
    schedule = next(item for item in calendar["entities"] if item["type"] == "sheet_table")
    assert calendar["type"] == "form"
    assert schedule["headers"] == ["NOMBRE DE LA OBRA", *(["L", "M", "M", "J", "V", "S", "D"] * 4)]
    assert [len(section["rows"]) for section in schedule["sections"]] == [6]
    assert all(len(row) == 29 and row[1:] == [""] * 28 for row in schedule["sections"][0]["rows"])
    legend = next(item for item in calendar["entities"] if item["type"] == "sheet_legend")
    assert [entry["code"] for entry in legend["entries"]] == ["D", "C", "A", "I", "E"]
    assert next(item for item in calendar["entities"] if item["type"] == "sheet_field")["value"] == ""

    budget = figures[269]
    grids = [item for item in budget["entities"] if item["type"] == "sheet_table"]
    assert budget["type"] == "table"
    assert [len(section["rows"]) for section in grids[0]["sections"]] == [3, 19, 8, 2]
    assert all(len(row) == 9 for section in grids[0]["sections"] for row in section["rows"])
    assert [len(row) for row in grids[1]["sections"][0]["rows"]] == [3, 3, 3, 3]
    assert grids[0]["sections"][0]["rows"][0][1] == "$ 3.200.000"
    assert grids[1]["sections"][0]["rows"][-1] == ["UTILIDAD", "$ 1.250.000", "8%"]

    costing = figures[270]
    tables = [item for item in costing["entities"] if item["type"] == "sheet_table"]
    assert costing["type"] == "form"
    assert tables[0]["headers"] == ["", "UNID", "CANT", "VR. UNIT", "VR. TOTAL"]
    assert [len(section["rows"]) for section in tables[0]["sections"]] == [3, 7, 10, 2, 3]
    assert all(len(row) == 5 for section in tables[0]["sections"] for row in section["rows"])
    assert tables[0]["sections"][0]["merged_cells"] == [{"row": 2, "start_column": 0, "colspan": 4}]
    assert tables[1]["sections"][0]["rows"][-1] == ["TOTAL", "$ -"]
    assert tables[2]["sections"][0]["rows"] == [["ML", "1,8"], ["DIVIDO EL TOTAL POR LOS ML, EN ESTE EJEMPLO 1,8M", ""], ["VALOR/ML", "$ -"]]


def test_contract_change_does_not_mutate_content_source_or_distribution() -> None:
    for number in (257, 269, 270):
        page = ROOT / f"books/cpnc-2025/pages/p{number:04d}"
        assert (page / "content.json").exists()
        assert (page / "source.md").exists()
        assert (page / "visual-inventory.json").exists()
    distribution = json.loads((ROOT / "books/cpnc-2025/distribution.json").read_text(encoding="utf-8"))
    assert len(distribution["exclude_pdf_pages"]) == 43
