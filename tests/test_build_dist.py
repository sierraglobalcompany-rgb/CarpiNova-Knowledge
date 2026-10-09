from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from carpinova_knowledge.build_dist import build_distribution

ROOT = Path(__file__).resolve().parents[1]


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
