import json
from pathlib import Path
from carpinova_knowledge.validate_repo import validate_repository
from carpinova_knowledge.render_docs import render_page_docs


def _write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def _source(page=1, printed=1):
    return {'book_id':'CPNC-2025','pdf_page':page,'printed_page':printed,'region':{'x':0,'y':0,'width':1,'height':1}}


def make_repo(root: Path):
    _write(root/'books/cpnc-2025/page-map.json', {'pages':[{'pdf_page':1,'printed_page':1,'mapping_status':'verified'}]})
    _write(root/'books/cpnc-2025/index.json', {'book_id':'CPNC-2025','sections':[{'section_id':'s','title':'S','printed_range':{'start':1,'end':1},'physical_range':{'start':1,'end':1}}]})
    p=root/'books/cpnc-2025/pages/p0001'; (p/'figures').mkdir(parents=True)
    _write(p/'page.json', {'id':'PAGE-CPNC-2025-P0001','book_id':'CPNC-2025','pdf_page':1,'printed_page':1,'topics':[],'contains':{'text':True,'figures':True}})
    _write(p/'content.json', [{'id':'CONTENT-CPNC-2025-P0001-001','kind':'source','source':_source(),'source_transcription':'A','normalized_text':'A','learning_text':'A simple','derived_from_content_ids':['CONTENT-CPNC-2025-P0001-001']}])
    _write(p/'measurements.json', [{'id':'MEAS-CPNC-2025-P0001-001','source':_source(),'value':35,'unit':'mm','meaning':'d','status':'VISUALLY_VERIFIED','visual_verification':{'verified':True,'method':'page_image'}}])
    _write(p/'rules.json', [{'id':'RULE-CPNC-2025-P0001-001','source':_source(),'statement':'rule','status':'CANDIDATE'}])
    _write(p/'figures/f1.json', {'id':'FIG-CPNC-2025-P0001-001','source':_source(),'type':'technical_diagram','purpose':'p','entities':[],'labels':[],'relationships':[],'geometry':{'precision':'approximate'},'preferred_renderer':'svg','deterministic_required':True,'generative_image_allowed':False,'educational_sequence':[],'accessibility_summary':'a'})
    _write(root/'lessons/pilot/l.json', {'id':'LESSON-PILOT-001','title':'L','content_refs':['CONTENT-CPNC-2025-P0001-001'],'figure_refs':['FIG-CPNC-2025-P0001-001'],'steps':[{'type':'explain','ref':'CONTENT-CPNC-2025-P0001-001'}]})
    render_page_docs(p)


def test_valid_repository_has_zero_errors(tmp_path: Path):
    make_repo(tmp_path)
    report=validate_repository(tmp_path)
    assert report['errors']==[]


def test_validator_catches_core_integrity_failures(tmp_path: Path):
    make_repo(tmp_path)
    p=tmp_path/'books/cpnc-2025/pages/p0001'
    page=json.loads((p/'page.json').read_text()); page['id']='PAGE-CPNC-2025-P9999'; _write(p/'page.json',page)
    fig=json.loads((p/'figures/f1.json').read_text()); fig['preferred_renderer']='image'; fig['generative_image_allowed']=True; _write(p/'figures/f1.json',fig)
    lesson=json.loads((tmp_path/'lessons/pilot/l.json').read_text()); lesson['content_refs']=['CONTENT-MISSING']; _write(tmp_path/'lessons/pilot/l.json',lesson)
    (p/'source.md').write_text('stale',encoding='utf-8')
    report=validate_repository(tmp_path)
    codes={e['code'] for e in report['errors']}
    assert {'PAGE_ID_MISMATCH','DETERMINISTIC_FIGURE_GENERATIVE_ONLY','UNRESOLVED_REF','STALE_MARKDOWN'} <= codes
