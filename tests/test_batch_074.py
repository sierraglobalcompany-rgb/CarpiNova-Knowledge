from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_074_qr_resource_index_and_hagalo_en_casa_separator_pages_are_accepted() -> None:
    report = build_batch_report(ROOT, "batch-074")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2
