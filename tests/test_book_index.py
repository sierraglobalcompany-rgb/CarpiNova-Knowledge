from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "cpnc-2025"
TAXONOMY = ROOT / "taxonomy"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_index_ranges_exist_and_pilot_page_91_has_exactly_one_section() -> None:
    page_map = _load(BOOK / "page-map.json")["pages"]
    index = _load(BOOK / "index.json")
    existing = {p["pdf_page"] for p in page_map}

    for section in index["sections"]:
        start = section["physical_range"]["start"]
        end = section["physical_range"]["end"]
        assert start <= end
        assert start in existing and end in existing

    matches = [
        s
        for s in index["sections"]
        if s["printed_range"]["start"] <= 91 <= s["printed_range"]["end"]
    ]
    assert len(matches) == 1
    assert matches[0]["section_id"] == "step-2-hardware"


def test_index_printed_ranges_map_to_expected_physical_offset() -> None:
    page_map = _load(BOOK / "page-map.json")["pages"]
    by_printed = {p["printed_page"]: p["pdf_page"] for p in page_map if p["printed_page"]}
    index = _load(BOOK / "index.json")
    for section in index["sections"]:
        ps = section["printed_range"]["start"]
        pe = section["printed_range"]["end"]
        assert section["physical_range"] == {"start": by_printed[ps], "end": by_printed[pe]}


def test_taxonomy_ids_are_unique_and_alias_targets_exist() -> None:
    canonical_ids: set[str] = set()
    alias_targets: list[str] = []
    for name in [
        "materials.json",
        "hardware.json",
        "furniture.json",
        "construction-systems.json",
        "procedures.json",
    ]:
        data = _load(TAXONOMY / name)
        for item in data["items"]:
            assert item["id"] not in canonical_ids
            canonical_ids.add(item["id"])
    glossary = _load(TAXONOMY / "glossary.json")
    for alias in glossary["aliases"]:
        alias_targets.append(alias["target_id"])
    assert alias_targets
    assert set(alias_targets) <= canonical_ids
