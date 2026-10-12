import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_116_recovers_exact_source_page_202() -> None:
    report = build_batch_report(ROOT, "batch-116")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 1,
        "content": 3,
        "figures": 0,
        "measurements": 10,
        "rules": 5,
    }

    p202 = ROOT / "books" / "cpnc-2025" / "pages" / "p0202"
    source = (p202 / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "Clósets",
        "La modulación de clósets también se basa en ergonomía.",
        "incluyendo dos gavetas con correderas por cada metro lineal.",
        "Doble colgadero, con una separación vertical de 90 cm entre cada uno.",
        "el maletero, que empieza a los 190 cm y tiene una altura de 40 cm",
        "el clóset ideal tendría 230 cm de altura: 190 cm de estructura útil más 40 cm de maletero.",
        "Profundidad interna: 50 cm",
        "Profundidad externa: 60 cm",
        "los 10 cm extra son para permitir el uso de sistemas corredizos",
    ):
        assert fragment in source

    measurements = json.loads((p202 / "measurements.json").read_text(encoding="utf-8"))
    values = {(item["value"], item["unit"]) for item in measurements}
    for expected in (
        (2, "count"),
        (1, "m"),
        (90, "cm"),
        (190, "cm"),
        (40, "cm"),
        (230, "cm"),
        (50, "cm"),
        (60, "cm"),
        (10, "cm"),
    ):
        assert expected in values

    visual = json.loads((p202 / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual["visuals"])

    audit = (ROOT / "audits" / "f1" / "source-gap-p0202.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit


def test_batch_116_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] == 292
    assert report["pending_pages"] == 3
    assert report["pending_pdf_pages"] == [207, 213, 223]
    assert report["duplicate_batch_pages"] == []
