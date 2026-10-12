from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .report_batch import REQUIRED_PAGE_FILES
from .report_coverage import build_coverage_report
from .validate_repo import validate_repository

_SOURCE_GAP_RE = re.compile(r"source-gap-p(\d{4})\.md$")
_URL_RE = re.compile(r"https?://[^\s<>()\[\]{}\"']+")
_QR_RE = re.compile(r"\bqr\b", re.IGNORECASE)
_SECURITY_TERMS = (
    "advertencia",
    "cuidado",
    "condición",
    "desconectar",
    "distancia",
    "epp",
    "peligro",
    "protección",
)
_NEGATIVE_DECODE_PHRASES = (
    "no se decodific",
    "no fueron decodific",
    "no fue decodific",
    "no se han decodific",
    "sin decodific",
    "no se considera conocido",
    "no se consideran conocidos",
)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _content_text(item: dict[str, Any]) -> str:
    return " ".join(
        str(item.get(field, ""))
        for field in ("source_transcription", "normalized_text", "learning_text")
    )


def _extract_urls(text: str) -> list[str]:
    return list(dict.fromkeys(match.rstrip(".,;:)") for match in _URL_RE.findall(text)))


def _claims_decoded_without_negation(text: str) -> bool:
    folded = text.casefold()
    if "decodific" not in folded:
        return False
    return not any(phrase in folded for phrase in _NEGATIVE_DECODE_PHRASES)


def classify_source_gaps(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    result: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for path in sorted((root / "audits" / "f1").glob("source-gap-p*.md")):
        match = _SOURCE_GAP_RE.fullmatch(path.name)
        if match is None:
            continue
        pdf_page = int(match.group(1))
        page_dir = pages_dir / f"p{pdf_page:04d}"
        complete = page_dir.is_dir() and all(
            (page_dir / filename).exists() for filename in REQUIRED_PAGE_FILES
        )
        result.append(
            {
                "file": str(path),
                "pdf_page": pdf_page,
                "status": "RESOLVED_HISTORICAL" if complete else "OPEN",
            }
        )
    return result


def find_visual_findings(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    findings: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for page_dir in sorted(pages_dir.glob("p*")):
        if not page_dir.is_dir():
            continue
        figure_ids: set[str] = set()
        figures_dir = page_dir / "figures"
        if figures_dir.exists():
            for figure_path in sorted(figures_dir.glob("*.json")):
                figure = _load(figure_path)
                if figure.get("figure_id"):
                    figure_ids.add(str(figure["figure_id"]))

        inventory_path = page_dir / "visual-inventory.json"
        if not inventory_path.exists():
            continue
        inventory = _load(inventory_path)
        for visual in inventory.get("visuals", []):
            if visual.get("meaningful") is not True:
                continue
            figure_id = visual.get("figure_id")
            if visual.get("exclusion_reason"):
                continue
            if figure_id and str(figure_id) in figure_ids:
                continue
            findings.append(
                {
                    "code": "meaningful_visual_without_figure",
                    "file": str(inventory_path),
                    "inventory_id": visual.get("inventory_id"),
                }
            )
    return findings


def build_qr_inventory(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    records: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for page_dir in sorted(pages_dir.glob("p*")):
        if not page_dir.is_dir():
            continue
        page_has_qr_content = False
        content_path = page_dir / "content.json"
        if content_path.exists():
            for item in _load(content_path):
                text = _content_text(item)
                if not _QR_RE.search(text):
                    continue
                page_has_qr_content = True
                destinations = _extract_urls(text)
                records.append(
                    {
                        "file": str(content_path),
                        "qr_id": item.get("content_id"),
                        "status": "DECODED" if destinations else "UNRESOLVED",
                        "destinations": destinations,
                        "provenance": item.get("source"),
                    }
                )
        if page_has_qr_content:
            continue

        inventory_path = page_dir / "visual-inventory.json"
        if inventory_path.exists():
            qr_visuals = [
                visual
                for visual in _load(inventory_path).get("visuals", [])
                if "qr" in str(visual.get("kind", "")).casefold()
            ]
            if qr_visuals:
                for visual in qr_visuals:
                    records.append(
                        {
                            "file": str(inventory_path),
                            "qr_id": visual.get("inventory_id"),
                            "status": "UNRESOLVED",
                            "destinations": [],
                            "provenance": visual.get("source_region"),
                        }
                    )
                continue

        figures_dir = page_dir / "figures"
        if not figures_dir.exists():
            continue
        for figure_path in sorted(figures_dir.glob("*.json")):
            figure = _load(figure_path)
            for entity in figure.get("entities", []):
                if str(entity.get("type", "")).casefold() != "qr_code":
                    continue
                records.append(
                    {
                        "file": str(figure_path),
                        "qr_id": entity.get("id"),
                        "status": "UNRESOLVED",
                        "destinations": [],
                        "provenance": figure.get("source"),
                    }
                )

    return records


def find_qr_findings(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    findings: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for content_path in sorted(pages_dir.glob("p*/content.json")):
        for item in _load(content_path):
            text = _content_text(item)
            if not _QR_RE.search(text):
                continue
            if _claims_decoded_without_negation(text) and not _extract_urls(text):
                findings.append(
                    {
                        "code": "decoded_qr_without_destination",
                        "file": str(content_path),
                        "qr_id": item.get("content_id"),
                    }
                )

    return findings


def find_security_candidates(root: Path, book_id: str) -> list[dict[str, Any]]:
    root = Path(root)
    findings: list[dict[str, Any]] = []
    pages_dir = root / "books" / book_id / "pages"

    for content_path in sorted(pages_dir.glob("p*/content.json")):
        for item in _load(content_path):
            source_text = str(item.get("source_transcription", "")).casefold()
            source_terms = [term for term in _SECURITY_TERMS if term in source_text]
            if not source_terms:
                continue
            derived_text = " ".join(
                (
                    str(item.get("normalized_text", "")),
                    str(item.get("learning_text", "")),
                )
            ).casefold()
            if any(term in derived_text for term in source_terms):
                continue
            findings.append(
                {
                    "code": "security_meaning_review",
                    "file": str(content_path),
                    "content_id": item.get("content_id"),
                    "source_terms": source_terms,
                }
            )

    return findings


def build_f1_report(root: Path, book_id: str) -> dict[str, Any]:
    root = Path(root)
    coverage = build_coverage_report(root, book_id)
    validation = validate_repository(root)
    source_gaps = classify_source_gaps(root, book_id)
    visual_findings = find_visual_findings(root, book_id)
    qr_inventory = build_qr_inventory(root, book_id)
    qr_findings = find_qr_findings(root, book_id)
    security_candidates = find_security_candidates(root, book_id)

    automatic_blockers: list[dict[str, Any]] = []
    if not coverage["complete"]:
        automatic_blockers.append(
            {
                "code": "coverage_incomplete",
                "pending_pdf_pages": coverage["pending_pdf_pages"],
                "duplicate_batch_pages": coverage["duplicate_batch_pages"],
            }
        )
    if not validation["valid"]:
        automatic_blockers.append(
            {
                "code": "repository_validation_failed",
                "error_count": validation["error_count"],
            }
        )
    automatic_blockers.extend(
        {"code": "open_source_gap", **gap}
        for gap in source_gaps
        if gap["status"] == "OPEN"
    )
    automatic_blockers.extend(visual_findings)
    automatic_blockers.extend(qr_findings)

    return {
        "book_id": book_id,
        "coverage": coverage,
        "validation": validation,
        "source_gaps": source_gaps,
        "visual_findings": visual_findings,
        "qr_inventory": qr_inventory,
        "qr_findings": qr_findings,
        "security_candidates": security_candidates,
        "automatic_blockers": automatic_blockers,
        "automatic_gate": "GO" if not automatic_blockers else "NO_GO",
    }
