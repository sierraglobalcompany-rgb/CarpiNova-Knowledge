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
    assert manifest["source_page_count"] == 295
    assert manifest["excluded_page_count"] == 43
    assert manifest["counts"]["pages"] == 252
    assert manifest["knowledge_version"] == "1.0.0"


def test_ci_post_1_0_contract_uses_current_actions_and_no_stale_f1_pushes() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "knowledge-qa.yml").read_text(
        encoding="utf-8"
    )

    assert "      - main\n" in workflow
    assert "feat/knowledge-f1" not in workflow
    assert "knowledge/f1-" not in workflow
    assert "  pull_request:\n    branches:\n      - main\n" in workflow
    assert "uses: actions/checkout@v7" in workflow
    assert "uses: actions/setup-python@v7" in workflow
    assert "uses: astral-sh/setup-uv@v10" in workflow
