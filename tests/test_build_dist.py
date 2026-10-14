from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from carpinova_knowledge.build_dist import build_book_distribution, build_distribution

ROOT = Path(__file__).resolve().parents[1]

USEFUL_BOOK_EXCLUDED_PDF_PAGES = {
    *range(1, 15),
    16,
    17,
    18,
    20,
    21,
    22,
    57,
    58,
    59,
    97,
    102,
    103,
    144,
    167,
    168,
    169,
    170,
    171,
    172,
    173,
    181,
    182,
    183,
    193,
    231,
    273,
    274,
    275,
    295,
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_build_distribution_is_deterministic_and_scoped_to_pilot(tmp_path: Path) -> None:
    out_a = tmp_path / "a"
    out_b = tmp_path / "b"

    manifest_a = build_distribution(ROOT, "batch-000-pilot", out_a)
    manifest_b = build_distribution(ROOT, "batch-000-pilot", out_b)

    expected_files = ["knowledge.bundle.json", "figures.bundle.json", "lessons.bundle.json", "manifest.json"]
    assert sorted(p.name for p in out_a.iterdir()) == sorted(expected_files)
    assert sorted(p.name for p in out_b.iterdir()) == sorted(expected_files)
    for name in expected_files:
        assert _sha(out_a / name) == _sha(out_b / name)

    knowledge = json.loads((out_a / "knowledge.bundle.json").read_text(encoding="utf-8"))
    figures = json.loads((out_a / "figures.bundle.json").read_text(encoding="utf-8"))
    lessons = json.loads((out_a / "lessons.bundle.json").read_text(encoding="utf-8"))

    assert [p["printed_page"] for p in knowledge["pages"]] == list(range(88, 96))
    assert all(r["status"] != "EXECUTABLE" for r in knowledge["rules"])
    assert len(figures["figures"]) == 6
    assert len(lessons["lessons"]) == 1
    assert manifest_a["batch_id"] == "BATCH-000-PILOT"
    assert manifest_a["knowledge_version"] == "0.1.0"
    assert manifest_a["source_manifest_sha256"] == "318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c"
    assert manifest_a == manifest_b

    combined = b"".join((out_a / name).read_bytes() for name in expected_files)
    assert b"/mnt/" not in combined
    assert b"source-books" not in combined
    assert b".pdf" not in combined.lower()


def test_build_book_distribution_is_deterministic_and_covers_f1(tmp_path: Path) -> None:
    out_a = tmp_path / "book-a"
    out_b = tmp_path / "book-b"

    manifest_a = build_book_distribution(ROOT, "cpnc-2025", out_a)
    manifest_b = build_book_distribution(ROOT, "cpnc-2025", out_b)

    expected_files = ["knowledge.bundle.json", "figures.bundle.json", "lessons.bundle.json", "manifest.json"]
    assert sorted(p.name for p in out_a.iterdir()) == sorted(expected_files)
    assert sorted(p.name for p in out_b.iterdir()) == sorted(expected_files)
    for name in expected_files:
        assert _sha(out_a / name) == _sha(out_b / name)

    knowledge = json.loads((out_a / "knowledge.bundle.json").read_text(encoding="utf-8"))
    figures = json.loads((out_a / "figures.bundle.json").read_text(encoding="utf-8"))
    page_ids = {page["page_id"] for page in knowledge["pages"]}
    excluded_page_ids = {
        f"PAGE-CPNC-2025-P{page:04d}" for page in USEFUL_BOOK_EXCLUDED_PDF_PAGES
    }

    assert excluded_page_ids.isdisjoint(page_ids)
    assert "PAGE-CPNC-2025-P0015" in page_ids
    assert "PAGE-CPNC-2025-P0019" in page_ids
    assert "PAGE-CPNC-2025-P0093" in page_ids
    assert "PAGE-CPNC-2025-P0165" in page_ids
    assert "PAGE-CPNC-2025-P0175" in page_ids
    assert all(rule["status"] != "EXECUTABLE" for rule in knowledge["rules"])

    assert manifest_a["scope"] == "BOOK"
    assert manifest_a["book_id"] == "cpnc-2025"
    assert manifest_a["knowledge_version"] == "1.2.0"
    assert manifest_a["source_manifest_sha256"] == "318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c"
    assert manifest_a["source_page_count"] == 295
    assert manifest_a["excluded_page_count"] == len(USEFUL_BOOK_EXCLUDED_PDF_PAGES)
    assert manifest_a["counts"]["pages"] == 295 - len(USEFUL_BOOK_EXCLUDED_PDF_PAGES)
    assert manifest_a == manifest_b

    matches = [
        figure
        for figure in figures["figures"]
        if figure["figure_id"] == "FIG-CPNC-2025-P0113-001"
    ]
    assert len(matches) == 1
    figure = matches[0]
    assert figure["page_id"] == "PAGE-CPNC-2025-P0113"
    assert figure["source"]["pdf_page"] == 113
    assert figure["source"]["printed_page"] == 91
    assert figure["reconstruction"]["render_contract"] == "normalized-2d-v1"
    assert figure["camera"]["coordinate_space"] == "normalized_figure"
    assert figure["camera"]["viewport"] == {"x": 0, "y": 0, "width": 1, "height": 1}
    assert figure["layers"]

    entities = {entity["id"]: entity for entity in figure["entities"]}
    assert entities["telescopic-slide"]["geometry"]["primitive"] == "polyline"
    assert entities["slide-inner-profile"]["geometry"]["primitive"] == "polyline"
    assert entities["slide-middle-profile"]["geometry"]["primitive"] == "polyline"
    assert entities["slide-section-left"]["geometry"]["primitive"] == "rect"
    assert entities["slide-section-right"]["geometry"]["primitive"] == "rect"

    expected_measurements = {
        "MEAS-CPNC-2025-P0113-009",
        "MEAS-CPNC-2025-P0113-010",
        "MEAS-CPNC-2025-P0113-011",
    }
    assert set(figure["measurements"]) == expected_measurements
    annotations_by_measurement = {
        annotation["measurement_id"]: annotation
        for annotation in figure["annotations"]
        if annotation.get("measurement_id")
    }
    assert set(annotations_by_measurement) == expected_measurements
    for annotation in annotations_by_measurement.values():
        assert annotation["entity_id"] == "telescopic-slide"
        assert annotation["placement"]["precision"] == "approximate"
        assert 0 <= annotation["placement"]["x"] <= 1
        assert 0 <= annotation["placement"]["y"] <= 1

    combined = b"".join((out_a / name).read_bytes() for name in expected_files)
    assert b"/mnt/" not in combined
    assert b"source-books" not in combined
    assert b".pdf" not in combined.lower()


def test_build_distribution_rejects_unknown_batch(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="batch"):
        build_distribution(ROOT, "batch-does-not-exist", tmp_path / "out")


def test_build_distribution_rejects_duplicate_verified_printed_mapping(tmp_path: Path) -> None:
    import shutil

    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".superpowers", ".worktrees", "__pycache__", ".pytest_cache"))
    path = root / "books" / "cpnc-2025" / "page-map.json"
    page_map = json.loads(path.read_text(encoding="utf-8"))
    original = next(item for item in page_map["pages"] if item.get("printed_page") == 88)
    duplicate = dict(original)
    duplicate["page_id"] = "PAGE-CPNC-2025-P0296"
    duplicate["pdf_page"] = 296
    page_map["pages"].append(duplicate)
    path.write_text(json.dumps(page_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(ValueError):
        build_distribution(root, "batch-000-pilot", tmp_path / "out")
