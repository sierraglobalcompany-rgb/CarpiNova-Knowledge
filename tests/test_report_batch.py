import json
import shutil
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_generic_batch_report_accepts_f0_pilot() -> None:
    report = build_batch_report(ROOT, "batch-000-pilot")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 8


def test_batch_001_front_matter_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-001")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 8


def test_batch_002_onboarding_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-002")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2


def test_batch_003_duratex_reference_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-003")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 4


def test_batch_004_virtual_course_index_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-004")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2


def test_batch_005_final_front_matter_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-005")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 6


def test_batch_006_index_and_support_group_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-006")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 4


def test_batch_007_carpintero_digital_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-007")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 3


def test_batch_008_teaching_furniture_origin_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-008")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 3


def test_batch_009_learning_and_teaching_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-009")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 3


def test_batch_010_new_carpenter_community_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-010")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 6


def test_batch_011_new_beginning_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-011")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 4


def test_batch_012_company_origin_story_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-012")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 6


def test_generic_batch_report_accepts_physical_page_batch(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        root,
        ignore=shutil.ignore_patterns(
            ".git", ".worktrees", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv"
        ),
    )
    batch = {
        "batch_id": "BATCH-TEST-PHYSICAL",
        "book_id": "cpnc-2025",
        "purpose": "f1-extraction-test",
        "pdf_pages": [110],
        "status": "EXTRACTED",
    }
    path = root / "books" / "cpnc-2025" / "batches" / "batch-test-physical.json"
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = build_batch_report(root, "batch-test-physical")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 1
