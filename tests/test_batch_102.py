from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_102_glossary_i_j_k_l_m_n_o_p_definitions_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-102")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
    assert report["counts"]["content"] == 54
    assert report["counts"]["figures"] == 0
