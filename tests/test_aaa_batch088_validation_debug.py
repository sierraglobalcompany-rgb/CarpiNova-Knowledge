from pathlib import Path

from carpinova_knowledge.validate_repo import validate_repository

ROOT = Path(__file__).resolve().parents[1]


def test_batch088_candidate_repository_validation_debug() -> None:
    report = validate_repository(ROOT)
    assert report["valid"], report["errors"]
