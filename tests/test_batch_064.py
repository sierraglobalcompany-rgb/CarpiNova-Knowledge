from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_064_door_opening_frame_and_lock_installation_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-064")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
