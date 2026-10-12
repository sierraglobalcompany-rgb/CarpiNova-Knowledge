import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_help_lists_all_commands() -> None:
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")
    result = subprocess.run(
        [sys.executable, "-m", "carpinova_knowledge", "--help"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    for command in (
        "audit-book",
        "build-page-map",
        "scaffold-batch",
        "render-docs",
        "validate",
        "build-dist",
        "build-book-dist",
        "report-pilot",
        "report-batch",
        "report-coverage",
    ):
        assert command in result.stdout


def test_cli_build_book_dist_builds_full_f1_bundle(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "dist"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "carpinova_knowledge",
            "build-book-dist",
            "--root",
            str(root),
            "--book-id",
            "cpnc-2025",
            "--out",
            str(out),
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["scope"] == "BOOK"
    assert manifest["counts"]["pages"] == 295
    assert manifest["knowledge_version"] == "1.0.0-rc.1"


def test_ci_pushes_validate_main_and_f1() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "knowledge-qa.yml").read_text(
        encoding="utf-8"
    )

    assert "      - main\n" in workflow
    assert "      - 'feat/knowledge-f1*'\n" in workflow
    assert "      - 'knowledge/f1-*'\n" in workflow
    assert "  pull_request:\n    branches:\n      - main\n" in workflow
