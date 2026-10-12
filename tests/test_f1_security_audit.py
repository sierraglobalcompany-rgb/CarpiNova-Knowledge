import json
from pathlib import Path

from carpinova_knowledge.report_f1 import find_security_candidates

ROOT = Path(__file__).resolve().parents[1]


def test_current_f1_security_candidates_are_reviewed() -> None:
    review = json.loads((ROOT / "audits" / "f1" / "security-review.json").read_text(encoding="utf-8"))
    candidate_ids = {
        item["content_id"] for item in find_security_candidates(ROOT, "cpnc-2025")
    }
    reviewed_ids = {item["content_id"] for item in review["reviewed_candidates"]}
    fixed_ids = {item["content_id"] for item in review["fixed_findings"]}

    assert candidate_ids == reviewed_ids
    assert candidate_ids.isdisjoint(fixed_ids)
