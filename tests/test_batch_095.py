from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_095_sena_certification_continuation_and_infographic_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-095")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
