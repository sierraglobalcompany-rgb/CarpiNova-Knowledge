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
