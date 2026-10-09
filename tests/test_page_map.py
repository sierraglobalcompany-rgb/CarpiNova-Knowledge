from __future__ import annotations

from carpinova_knowledge.page_map import build_page_map


def _page(pdf_page: int, blocks: list[tuple[str, list[float]]], height: float = 800.0) -> dict:
    return {
        "pdf_page": pdf_page,
        "height_pt": height,
        "width_pt": 600.0,
        "text_blocks": [
            {"text": text, "bbox": bbox, "block_no": i, "block_type": 0}
            for i, (text, bbox) in enumerate(blocks)
        ],
    }


def test_page_map_preserves_all_physical_pages_and_candidates() -> None:
    audit = {
        "book_id": "book",
        "pages": [
            _page(1, [("front matter", [10, 20, 200, 40])]),
            _page(2, [("1", [570, 755, 580, 772])]),
            _page(3, [("2", [10, 755, 20, 772])]),
        ],
    }
    result = build_page_map(audit, {})
    assert [entry["pdf_page"] for entry in result["pages"]] == [1, 2, 3]
    assert result["pages"][0]["printed_page"] is None
    assert result["pages"][0]["mapping_status"] == "unresolved"
    assert result["pages"][1]["printed_page"] == 1
    assert result["pages"][1]["mapping_status"] == "candidate"
    assert result["pages"][2]["printed_page"] == 2


def test_duplicate_candidates_become_unresolved_until_overridden() -> None:
    audit = {
        "book_id": "book",
        "pages": [
            _page(1, [("5", [10, 755, 20, 772])]),
            _page(2, [("5", [570, 755, 580, 772])]),
        ],
    }
    result = build_page_map(audit, {})
    assert [p["mapping_status"] for p in result["pages"]] == ["unresolved", "unresolved"]
    assert [p["printed_page"] for p in result["pages"]] == [5, 5]


def test_explicit_overrides_verify_or_mark_not_printed() -> None:
    audit = {
        "book_id": "book",
        "pages": [
            _page(1, [("99", [10, 755, 20, 772])]),
            _page(2, []),
            _page(3, [("3", [570, 755, 580, 772])]),
        ],
    }
    result = build_page_map(audit, {1: 1, 2: None, 3: 3})
    assert result["pages"][0]["printed_page"] == 1
    assert result["pages"][0]["mapping_status"] == "verified"
    assert result["pages"][1]["printed_page"] is None
    assert result["pages"][1]["mapping_status"] == "not_printed"
    assert result["pages"][2]["mapping_status"] == "verified"


def test_margin_detection_ignores_numbers_in_body() -> None:
    audit = {
        "book_id": "book",
        "pages": [
            _page(1, [("35", [100, 300, 120, 320])]),
            _page(2, [("7", [570, 760, 580, 775])]),
        ],
    }
    result = build_page_map(audit, {})
    assert result["pages"][0]["printed_page"] is None
    assert result["pages"][1]["printed_page"] == 7
