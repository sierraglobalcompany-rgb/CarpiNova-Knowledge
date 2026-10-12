from pathlib import Path

from carpinova_knowledge.report_f1 import find_security_candidates


ROOT = Path(__file__).resolve().parents[1]


def test_current_f1_has_no_unreviewed_security_candidates() -> None:
    assert find_security_candidates(ROOT, "cpnc-2025") == []
