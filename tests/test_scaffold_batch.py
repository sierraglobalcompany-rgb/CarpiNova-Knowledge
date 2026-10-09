from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.scaffold_batch import scaffold_batch


def _page_map() -> dict:
    return {
        "book_id": "cpnc-2025",
        "pages": [
            {
                "page_id": f"PAGE-CPNC-2025-P{printed+22:04d}",
                "book_id": "cpnc-2025",
                "pdf_page": printed + 22,
                "printed_page": printed,
                "mapping_status": "verified",
            }
            for printed in range(88, 96)
        ],
    }


def test_scaffold_resolves_pilot_to_eight_physical_page_folders(tmp_path: Path) -> None:
    batch = {
        "batch_id": "BATCH-000-PILOT",
        "book_id": "cpnc-2025",
        "purpose": "schema-and-reconstruction-pilot",
        "printed_pages": list(range(88, 96)),
        "status": "PLANNED",
    }
    paths = scaffold_batch(batch, _page_map(), tmp_path)
    assert [p.name for p in paths] == [f"p{i:04d}" for i in range(110, 118)]
    for page_dir in paths:
        assert (page_dir / "page.json").exists()
        assert json.loads((page_dir / "content.json").read_text()) == []
        assert json.loads((page_dir / "measurements.json").read_text()) == []
        assert json.loads((page_dir / "rules.json").read_text()) == []
        assert (page_dir / "figures").is_dir()
        for name in ["source.md", "normalized.md", "learning.md"]:
            assert (page_dir / name).exists()


def test_scaffold_is_idempotent_and_does_not_overwrite_canonical_content(tmp_path: Path) -> None:
    batch = {
        "batch_id": "BATCH-000-PILOT",
        "book_id": "cpnc-2025",
        "purpose": "schema-and-reconstruction-pilot",
        "printed_pages": [88],
        "status": "PLANNED",
    }
    [page_dir] = scaffold_batch(batch, _page_map(), tmp_path)
    sentinel = [{"keep": "me"}]
    (page_dir / "content.json").write_text(json.dumps(sentinel), encoding="utf-8")
    scaffold_batch(batch, _page_map(), tmp_path)
    assert json.loads((page_dir / "content.json").read_text()) == sentinel


def test_scaffold_fails_on_ambiguous_mapping(tmp_path: Path) -> None:
    batch = {
        "batch_id": "BATCH-000-PILOT",
        "book_id": "cpnc-2025",
        "purpose": "schema-and-reconstruction-pilot",
        "printed_pages": [88],
        "status": "PLANNED",
    }
    page_map = _page_map()
    page_map["pages"][0]["mapping_status"] = "candidate"
    try:
        scaffold_batch(batch, page_map, tmp_path)
    except ValueError as exc:
        assert "unambiguous verified mapping" in str(exc)
    else:
        raise AssertionError("Expected ambiguous mapping to fail")
