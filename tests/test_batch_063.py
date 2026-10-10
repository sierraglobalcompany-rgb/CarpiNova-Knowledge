from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_063_door_leaf_hardware_frame_and_trim_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-063")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
