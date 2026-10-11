from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_100_glossary_d_e_definitions_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-100")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
    assert report["counts"]["content"] == 64
    assert report["counts"]["figures"] == 0
