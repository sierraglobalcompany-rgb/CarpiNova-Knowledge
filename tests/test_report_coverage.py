import json
import shutil
from pathlib import Path

from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_current_coverage_is_derived_from_canonical_files() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["total_pages"] == 295
    assert report["complete_pages"] == 139
    assert report["pending_pages"] == 156
    assert report["duplicate_batch_pages"] == []
    assert report["complete"] is False


def test_coverage_detects_duplicate_batch_assignment(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        root,
        ignore=shutil.ignore_patterns(
            ".git", ".worktrees", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv"
        ),
    )
    batch = {
        "batch_id": "BATCH-DUPLICATE",
        "book_id": "cpnc-2025",
        "purpose": "coverage-test",
        "pdf_pages": [110],
        "status": "PLANNED",
    }
    path = root / "books" / "cpnc-2025" / "batches" / "batch-duplicate.json"
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = build_coverage_report(root, "cpnc-2025")
    assert report["duplicate_batch_pages"] == [110]
