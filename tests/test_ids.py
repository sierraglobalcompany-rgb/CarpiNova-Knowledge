import pytest

from carpinova_knowledge.ids import content_id, figure_id, measurement_id, page_id, rule_id


def test_canonical_ids_derive_from_physical_pdf_page() -> None:
    assert page_id("cpnc-2025", 91) == "PAGE-CPNC-2025-P0091"
    assert content_id("cpnc-2025", 91, 2) == "CONTENT-CPNC-2025-P0091-002"
    assert figure_id("cpnc-2025", 91, 3) == "FIG-CPNC-2025-P0091-003"
    assert measurement_id("cpnc-2025", 91, 4) == "MEAS-CPNC-2025-P0091-004"
    assert rule_id("cpnc-2025", 91, 5) == "RULE-CPNC-2025-P0091-005"


@pytest.mark.parametrize("pdf_page,sequence", [(0, 1), (-1, 1), (1, 0), (1, -1)])
def test_id_helpers_reject_non_positive_numbers(pdf_page: int, sequence: int) -> None:
    if pdf_page <= 0:
        with pytest.raises(ValueError):
            figure_id("cpnc-2025", pdf_page, max(sequence, 1))
    else:
        with pytest.raises(ValueError):
            figure_id("cpnc-2025", pdf_page, sequence)
