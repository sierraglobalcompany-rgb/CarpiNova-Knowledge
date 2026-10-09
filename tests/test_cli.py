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
    ):
        assert command in result.stdout
