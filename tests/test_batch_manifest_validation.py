from __future__ import annotations

import json
from pathlib import Path

from carpinova_knowledge.validate_repo import validate_repository


def test_invalid_batch_status_is_reported_as_schema_error(tmp_path: Path) -> None:
    batch_path = tmp_path / "books" / "cpnc-2025" / "batches" / "batch-test.json"
    batch_path.parent.mkdir(parents=True, exist_ok=True)
    batch_path.write_text(
        json.dumps(
            {
                "batch_id": "BATCH-TEST",
                "book_id": "cpnc-2025",
                "purpose": "validator-contract-test",
                "pdf_pages": [1],
                "status": "NOT_A_REAL_STATUS",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    report = validate_repository(tmp_path)

    assert any(
        error["code"] == "schema_error" and error["file"] == str(batch_path)
        for error in report["errors"]
    )
