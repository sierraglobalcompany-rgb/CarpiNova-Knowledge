import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report
from carpinova_knowledge.report_coverage import build_coverage_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_111_recovers_exact_source_page_178() -> None:
    report = build_batch_report(ROOT, "batch-111")
    assert report["result"] == "GO"
    assert report["counts"] == {
        "pages": 1,
        "content": 6,
        "figures": 0,
        "measurements": 7,
        "rules": 5,
    }

    page_dir = ROOT / "books" / "cpnc-2025" / "pages" / "p0178"
    source = (page_dir / "source.md").read_text(encoding="utf-8")
    for fragment in (
        "Servicios especiales",
        "1. Engruese",
        "40 x 50 cm",
        "15 mm",
        "5 a 7 cm",
        "45°",
        "2. Ensanduchado",
        "súper pega infinita",
        "3. Ranuras",
        "usualmente de 4 mm",
        "4. Curvas",
        "5. Perforaciones para herrajes",
        "Corte Cloud",
        "minifix o tarugos",
    ):
        assert fragment in source

    measurements = json.loads((page_dir / "measurements.json").read_text(encoding="utf-8"))
    assert [(item["value"], item["unit"]) for item in measurements] == [
        (40, "cm"),
        (50, "cm"),
        (15, "mm"),
        (5, "cm"),
        (7, "cm"),
        (45, "deg"),
        (4, "mm"),
    ]

    visual = json.loads((page_dir / "visual-inventory.json").read_text(encoding="utf-8"))
    assert visual["inspection_status"] == "VISUALLY_VERIFIED"
    assert all(item["meaningful"] is False for item in visual["visuals"])

    audit = (ROOT / "audits" / "f1" / "source-gap-p0178.md").read_text(encoding="utf-8")
    assert "RESOLVED" in audit
    assert "PENDING — SOURCE_IMAGE_UNAVAILABLE" not in audit


def test_batch_111_advances_coverage_without_duplicates() -> None:
    report = build_coverage_report(ROOT, "cpnc-2025")
    assert report["complete_pages"] >= 285
    assert report["pending_pages"] <= 10
    assert 178 not in report["pending_pdf_pages"]
    assert report["duplicate_batch_pages"] == []
