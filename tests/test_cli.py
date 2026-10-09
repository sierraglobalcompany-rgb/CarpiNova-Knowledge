import subprocess
import sys
import os


def test_cli_help_lists_commands():
    env = os.environ.copy()
    env['PYTHONPATH'] = 'src'
    result = subprocess.run(
        [sys.executable, '-m', 'carpinova_knowledge', '--help'],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    for command in [
        'audit-book', 'build-page-map', 'scaffold-batch', 'render-docs',
        'validate', 'build-dist', 'report-pilot'
    ]:
        assert command in result.stdout
