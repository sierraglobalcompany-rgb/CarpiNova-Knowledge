from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_101_glossary_e_f_g_h_definitions_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-101")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
    assert report["counts"]["content"] == 57
    assert report["counts"]["figures"] == 0
