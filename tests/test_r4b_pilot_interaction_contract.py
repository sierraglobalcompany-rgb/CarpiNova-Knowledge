from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_PATH = ROOT / "lessons" / "pilot" / "slides-x-2x.json"


def _steps_by_order() -> dict[int, dict]:
    lesson = json.loads(LESSON_PATH.read_text(encoding="utf-8"))
    return {step["order"]: step for step in lesson["steps"]}


def test_identify_parts_contract_is_explicit_and_source_backed() -> None:
    interaction = _steps_by_order()[4]["interaction"]

    assert interaction == {
        "type": "identify_parts",
        "source_content_id": "CONTENT-CPNC-2025-P0115-003",
        "parts": [
            {
                "label": "Parte delgada",
                "installation_location": "lateral de la gaveta",
            },
            {
                "label": "Parte gruesa",
                "installation_location": "costado interno del mueble",
            },
        ],
    }


def test_guided_sequence_contract_uses_canonical_content_and_measurement_ids() -> None:
    interaction = _steps_by_order()[5]["interaction"]

    assert interaction == {
        "type": "guided_sequence",
        "sequence": [
            {
                "order": 1,
                "content_id": "CONTENT-CPNC-2025-P0115-004",
                "measurement_ids": [
                    "MEAS-CPNC-2025-P0115-007",
                    "MEAS-CPNC-2025-P0115-008",
                ],
            },
            {
                "order": 2,
                "content_id": "CONTENT-CPNC-2025-P0116-001",
                "measurement_ids": ["MEAS-CPNC-2025-P0116-001"],
            },
            {
                "order": 3,
                "content_id": "CONTENT-CPNC-2025-P0116-002",
                "measurement_ids": ["MEAS-CPNC-2025-P0116-002"],
            },
        ],
    }
