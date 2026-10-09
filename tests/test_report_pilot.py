import json
import shutil
from pathlib import Path
from carpinova_knowledge.report_pilot import build_pilot_report


def test_real_pilot_reports_go():
    report=build_pilot_report(Path('.'),'BATCH-000-PILOT')
    assert report['result']=='GO'
    assert report['counts']['pages']==8
    assert report['counts']['figures']==6
    assert report['counts']['measurements']==48
    assert report['counts']['rules']==36
    assert report['counts']['lessons']>=1
    assert report['validation_errors']==0


def test_missing_figure_for_declared_visual_is_no_go(tmp_path: Path):
    src=Path('.')
    for name in ['books','lessons','taxonomy','schemas','docs']:
        if (src/name).exists(): shutil.copytree(src/name,tmp_path/name)
    page=tmp_path/'books/cpnc-2025/pages/p0112'
    for f in (page/'figures').glob('*.json'): f.unlink()
    report=build_pilot_report(tmp_path,'BATCH-000-PILOT')
    assert report['result']=='NO_GO'
    assert any('meaningful visual' in x.lower() for x in report['findings'])
