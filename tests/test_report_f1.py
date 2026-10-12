from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.report_batch import REQUIRED_PAGE_FILES
from carpinova_knowledge.report_f1 import (
    build_f1_report,
    classify_source_gaps,
    find_qr_findings,
    find_security_candidates,
    find_visual_findings,
)

ROOT = Path(__file__).resolve().parents[1]


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


def test_qr_visual_without_explicit_status_is_reported(tmp_path: Path) -> None:
    page_dir = _complete_page(tmp_path, 4)
    inventory = {
        "page_id": "PAGE-CPNC-2025-P0004",
        "pdf_page": 4,
        "visuals": [
            {
                "inventory_id": "REF-P0004-001",
                "kind": "qr_store",
                "meaningful": False,
            }
        ],
    }
    (page_dir / "visual-inventory.json").write_text(
        json.dumps(inventory) + "\n", encoding="utf-8"
    )

    findings = find_qr_findings(tmp_path, "cpnc-2025")

    assert findings == [
        {
            "code": "unclassified_qr",
            "file": str(page_dir / "visual-inventory.json"),
            "qr_id": "REF-P0004-001",
        }
    ]


def test_decoded_qr_visual_requires_payload(tmp_path: Path) -> None:
    page_dir = _complete_page(tmp_path, 5)
    inventory = {
        "page_id": "PAGE-CPNC-2025-P0005",
        "pdf_page": 5,
        "visuals": [
            {
                "inventory_id": "REF-P0005-001",
                "kind": "qr_store",
                "meaningful": False,
                "qr_status": "DECODED",
            }
        ],
    }
    (page_dir / "visual-inventory.json").write_text(
        json.dumps(inventory) + "\n", encoding="utf-8"
    )

    findings = find_qr_findings(tmp_path, "cpnc-2025")

    assert findings[0]["code"] == "decoded_qr_without_payload"


def test_unresolved_qr_entity_is_classified_without_invented_payload(tmp_path: Path) -> None:
    page_dir = _complete_page(tmp_path, 6)
    figures_dir = page_dir / "figures"
    figures_dir.mkdir()
    figure = {
        "figure_id": "FIG-CPNC-2025-P0006-001",
        "entities": [
            {
                "id": "qr-reference",
                "type": "qr_code",
                "geometry": {"precision": "unknown"},
                "qr_status": "UNRESOLVED",
            }
        ],
    }
    (figures_dir / "fig-001.json").write_text(json.dumps(figure) + "\n", encoding="utf-8")

    assert find_qr_findings(tmp_path, "cpnc-2025") == []


def test_security_candidate_is_reported_when_safety_meaning_disappears(tmp_path: Path) -> None:
    page_dir = _complete_page(tmp_path, 7)
    content = [
        {
            "content_id": "CONTENT-CPNC-2025-P0007-001",
            "source_transcription": "Advertencia: desconectar la herramienta antes de ajustar.",
            "normalized_text": "Ajuste la herramienta antes del trabajo.",
            "learning_text": "Prepare la herramienta para el trabajo.",
        }
    ]
    (page_dir / "content.json").write_text(json.dumps(content) + "\n", encoding="utf-8")

    findings = find_security_candidates(tmp_path, "cpnc-2025")

    assert findings == [
        {
            "code": "security_meaning_review",
            "file": str(page_dir / "content.json"),
            "content_id": "CONTENT-CPNC-2025-P0007-001",
            "source_terms": ["advertencia", "desconectar"],
        }
    ]


def test_security_candidate_is_not_reported_when_safety_term_is_preserved(tmp_path: Path) -> None:
    page_dir = _complete_page(tmp_path, 8)
    content = [
        {
            "content_id": "CONTENT-CPNC-2025-P0008-001",
            "source_transcription": "Advertencia: desconectar la herramienta antes de ajustar.",
            "normalized_text": "Advertencia: desconectar la herramienta antes de ajustarla.",
            "learning_text": "Prepare el ajuste de forma segura.",
        }
    ]
    (page_dir / "content.json").write_text(json.dumps(content) + "\n", encoding="utf-8")

    assert find_security_candidates(tmp_path, "cpnc-2025") == []


def test_current_f1_has_no_automatic_audit_blockers() -> None:
    report = build_f1_report(ROOT, "cpnc-2025")

    assert report["coverage"]["total_pages"] == 295
    assert report["coverage"]["complete"] is True
    assert report["validation"]["valid"] is True
    assert report["automatic_blockers"] == []
