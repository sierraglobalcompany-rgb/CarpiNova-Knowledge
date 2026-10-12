from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_069_murphy_bed_mattress_frame_steps_and_lateral_b_hardware_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-069")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
