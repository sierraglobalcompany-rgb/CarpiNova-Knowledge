import pytest
from carpinova_knowledge.ids import content_id, figure_id, measurement_id, page_id, rule_id


def test_canonical_ids_use_physical_page():
    assert page_id('CPNC-2025', 110) == 'PAGE-CPNC-2025-P0110'
    assert content_id('CPNC-2025', 110, 1) == 'CONTENT-CPNC-2025-P0110-001'
    assert figure_id('CPNC-2025', 110, 2) == 'FIG-CPNC-2025-P0110-002'
    assert measurement_id('CPNC-2025', 110, 3) == 'MEAS-CPNC-2025-P0110-003'
    assert rule_id('CPNC-2025', 110, 4) == 'RULE-CPNC-2025-P0110-004'


def test_ids_reject_invalid_values():
    with pytest.raises(ValueError):
        page_id('CPNC-2025', 0)
    with pytest.raises(ValueError):
        figure_id('bad id', 1, 1)
