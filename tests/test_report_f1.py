from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.report_batch import REQUIRED_PAGE_FILES
from carpinova_knowledge.report_f1 import classify_source_gaps, find_visual_findings


def _complete_page(root: Path, pdf_page: int) -> Path:
    page_dir = root / "books" / "cpnc-2025" / "pages" / f"p{pdf_page:04d}"
    page_dir.mkdir(parents=True)
    for filename in REQUIRED_PAGE_FILES:
        path = page_dir / filename
        if filename.endswith(".json"):
            payload = [] if filename in {"content.json", "measurements.json", "rules.json"} else {}
            path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        else:
            path.write_text("generated\n", encoding="utf-8")
    return page_dir


def test_source_gap_is_resolved_historical_when_page_is_complete(tmp_path: Path) -> None:
    gap = tmp_path / "audits" / "f1" / "source-gap-p0001.md"
    gap.parent.mkdir(parents=True)
    gap.write_text("historical source gap\n", encoding="utf-8")
    _complete_page(tmp_path, 1)

    gaps = classify_source_gaps(tmp_path, "cpnc-2025")

    assert gaps == [
        {
            "file": str(gap),
            "pdf_page": 1,
            "status": "RESOLVED_HISTORICAL",
        }
    ]


def test_source_gap_stays_open_when_page_is_missing(tmp_path: Path) -> None:
    gap = tmp_path / "audits" / "f1" / "source-gap-p0002.md"
    gap.parent.mkdir(parents=True)
    gap.write_text("historical source gap\n", encoding="utf-8")

    gaps = classify_source_gaps(tmp_path, "cpnc-2025")

    assert gaps[0]["status"] == "OPEN"


def test_meaningful_visual_without_figure_or_exclusion_is_reported(tmp_path: Path) -> None:
    page_dir = _complete_page(tmp_path, 3)
    inventory = {
        "page_id": "PAGE-CPNC-2025-P0003",
        "pdf_page": 3,
        "visuals": [
            {
                "inventory_id": "VIS-P0003-001",
                "kind": "technical_diagram",
                "meaningful": True,
            }
        ],
    }
    (page_dir / "visual-inventory.json").write_text(
        json.dumps(inventory) + "\n", encoding="utf-8"
    )

    findings = find_visual_findings(tmp_path, "cpnc-2025")

    assert findings == [
        {
            "code": "meaningful_visual_without_figure",
            "file": str(page_dir / "visual-inventory.json"),
            "inventory_id": "VIS-P0003-001",
        }
    ]
