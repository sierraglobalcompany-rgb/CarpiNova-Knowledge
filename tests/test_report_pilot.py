from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from carpinova_knowledge.report_pilot import build_pilot_report

ROOT = Path(__file__).resolve().parents[1]


def _copy_project(tmp_path: Path) -> Path:
    dst = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        dst,
        ignore=shutil.ignore_patterns(".git", ".superpowers", ".worktrees", "__pycache__", ".pytest_cache", ".ruff_cache"),
    )
    return dst


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_actual_pilot_reports_go_with_expected_coverage() -> None:
    report = build_pilot_report(ROOT, "batch-000-pilot")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 8
    assert report["counts"]["figures_total"] == 6
    assert report["counts"]["measurements_by_status"]["VISUALLY_VERIFIED"] == 48
    assert report["counts"]["rule_candidates"] == 36
    # This is a global inventory count, not a fixed F0-only lesson count.
    lesson_files = sorted(ROOT.glob("lessons/**/*.json"))
    assert any(path.stem == "slides-x-2x" for path in lesson_files)
    assert report["counts"]["lessons"] == len(lesson_files)
    assert report["reconstruction_audit"]["all_pass"] is True


@pytest.mark.parametrize(
    "mutation,expected_code",
    [
        ("missing_required_page_file", "missing_required_page_file"),
        ("meaningful_visual_without_figure", "meaningful_visual_without_figure"),
        ("measurement_without_source", "validation_error"),
        ("broken_cross_reference", "validation_error"),
        ("pedagogical_provenance_missing", "validation_error"),
        ("ambiguous_page_mapping", "ambiguous_page_mapping"),
        ("stale_markdown", "validation_error"),
    ],
)
def test_acceptance_is_no_go_for_required_failure_modes(tmp_path: Path, mutation: str, expected_code: str) -> None:
    root = _copy_project(tmp_path)
    p110 = root / "books" / "cpnc-2025" / "pages" / "p0110"

    if mutation == "missing_required_page_file":
        (p110 / "content.json").unlink()
    elif mutation == "meaningful_visual_without_figure":
        (p110 / "figures" / "fig-001.json").unlink()
    elif mutation == "measurement_without_source":
        records = _load(p110 / "measurements.json")
        records[0].pop("source", None)
        _write(p110 / "measurements.json", records)
    elif mutation == "broken_cross_reference":
        path = root / "lessons" / "pilot" / "slides-x-2x.json"
        lesson = _load(path)
        lesson["steps"][0]["content_ids"] = ["CONTENT-CPNC-2025-P0110-999"]
        _write(path, lesson)
    elif mutation == "pedagogical_provenance_missing":
        records = _load(p110 / "content.json")
        records[0]["derived_from_content_ids"] = []
        _write(p110 / "content.json", records)
    elif mutation == "ambiguous_page_mapping":
        path = root / "books" / "cpnc-2025" / "page-map.json"
        page_map = _load(path)
        for page in page_map["pages"]:
            if page.get("printed_page") == 88:
                page["mapping_status"] = "candidate"
                break
        _write(path, page_map)
    elif mutation == "stale_markdown":
        (p110 / "learning.md").write_text("stale\n", encoding="utf-8")
    else:  # pragma: no cover
        raise AssertionError(mutation)

    report = build_pilot_report(root, "batch-000-pilot")
    assert report["result"] == "NO_GO"
    assert expected_code in {finding["code"] for finding in report["findings"]}
