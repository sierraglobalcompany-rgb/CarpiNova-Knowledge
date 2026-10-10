import json
from pathlib import Path

from carpinova_knowledge.report_batch import build_batch_report

ROOT = Path(__file__).resolve().parents[1]


def test_batch_025_telescopic_slides_and_omega_hinges_is_accepted() -> None:
    report = build_batch_report(ROOT, "batch-025")
    assert report["result"] == "GO"
    assert report["counts"]["pages"] == 2


def test_batch_025_does_not_invent_units_for_system_32_37_label() -> None:
    measurements = json.loads(
        (
            ROOT
            / "books"
            / "cpnc-2025"
            / "pages"
            / "p0118"
            / "measurements.json"
        ).read_text(encoding="utf-8")
    )
    by_id = {item["measurement_id"]: item for item in measurements}
    assert by_id["MEAS-CPNC-2025-P0118-015"]["unit"] is None
    assert by_id["MEAS-CPNC-2025-P0118-016"]["unit"] is None
