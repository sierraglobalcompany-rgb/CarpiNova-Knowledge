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
        "report-pilot",
        "report-batch",
    ):
        assert command in result.stdout


def test_ci_pushes_validate_main_and_f1() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "knowledge-qa.yml").read_text(
        encoding="utf-8"
    )

    assert "      - main\n" in workflow
    assert "      - 'feat/knowledge-f1*'\n" in workflow
    assert "      - 'knowledge/f1-*'\n" in workflow
    assert "  pull_request:\n    branches:\n      - main\n" in workflow
