from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_072_entertainment_center_continuation_and_tv_board_support_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-072")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
