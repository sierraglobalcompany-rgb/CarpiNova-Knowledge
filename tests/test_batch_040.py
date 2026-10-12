from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_040_tools_profile_and_basics_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-040")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
