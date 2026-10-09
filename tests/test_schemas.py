from copy import deepcopy
from jsonschema import Draft202012Validator
import pytest

from carpinova_knowledge.schema_loader import SCHEMA_NAMES, load_schema, validate_instance


VALID = {
    'source': {'book_id':'CPNC-2025','pdf_page':110,'printed_page':88,'region':{'x':0.1,'y':0.1,'width':0.8,'height':0.4}},
    'page': {'id':'PAGE-CPNC-2025-P0110','book_id':'CPNC-2025','pdf_page':110,'printed_page':88,'topics':['hardware'],'contains':{'text':True,'figures':True}},
    'content': {'id':'CONTENT-CPNC-2025-P0110-001','kind':'source','source':{'book_id':'CPNC-2025','pdf_page':110,'printed_page':88,'region':{'x':0.1,'y':0.1,'width':0.8,'height':0.4}},'source_transcription':'Texto','normalized_text':'Texto','learning_text':'Texto simple','derived_from_content_ids':['CONTENT-CPNC-2025-P0110-001']},
    'figure': {'id':'FIG-CPNC-2025-P0110-001','source':{'book_id':'CPNC-2025','pdf_page':110,'printed_page':88,'region':{'x':0.05,'y':0.1,'width':0.9,'height':0.45}},'type':'illustration','purpose':'Explicar herrajes','entities':[],'labels':[],'relationships':[],'geometry':{'precision':'unknown'},'preferred_renderer':'image','deterministic_required':False,'generative_image_allowed':True,'educational_sequence':[],'accessibility_summary':'Ilustración de herrajes.'},
    'measurement': {'id':'MEAS-CPNC-2025-P0113-001','source':{'book_id':'CPNC-2025','pdf_page':113,'printed_page':91,'region':{'x':0,'y':0,'width':1,'height':1}},'value':35,'unit':'mm','meaning':'diámetro de perforación','status':'VISUALLY_VERIFIED','visual_verification':{'method':'page_image','verified':True}},
    'rule': {'id':'RULE-CPNC-2025-P0113-001','source':{'book_id':'CPNC-2025','pdf_page':113,'printed_page':91,'region':{'x':0,'y':0,'width':1,'height':1}},'statement':'Usar perforación de 35 mm','status':'CANDIDATE','applies_to':['cup_hinge']},
    'concept': {'id':'CONCEPT-CUP-HINGE','canonical_term':'bisagra de cazoleta','aliases':['bisagra parche'],'source_refs':['CONTENT-CPNC-2025-P0111-001']},
    'lesson': {'id':'LESSON-HINGES-001','title':'Bisagras de cazoleta','content_refs':['CONTENT-CPNC-2025-P0111-001'],'figure_refs':['FIG-CPNC-2025-P0112-001'],'steps':[{'type':'explain','ref':'CONTENT-CPNC-2025-P0111-001'}]},
    'batch': {'batch_id':'BATCH-000-PILOT','book_id':'CPNC-2025','printed_pages':[88,89,90,91,92,93,94,95],'status':'ACCEPTED'},
}


def test_all_schemas_are_valid_and_accept_fixture():
    assert set(SCHEMA_NAMES) == set(VALID)
    for name in SCHEMA_NAMES:
        schema = load_schema(name)
        Draft202012Validator.check_schema(schema)
        assert validate_instance(name, VALID[name]) == []

@pytest.mark.parametrize('name,mutator', [
    ('source', lambda d: d.update(pdf_page=0)),
    ('source', lambda d: d['region'].update(x=1.2)),
    ('measurement', lambda d: (d.update(status='VALIDATED'), d.pop('visual_verification', None))),
    ('rule', lambda d: d.update(status='EXECUTABLE')),
    ('content', lambda d: d.pop('derived_from_content_ids', None)),
    ('figure', lambda d: (d['geometry'].update(precision='unknown', dimensions=[{'name':'width','value':10,'unit':'mm'}]))),
])
def test_required_failure_modes(name, mutator):
    obj = deepcopy(VALID[name])
    mutator(obj)
    errors = validate_instance(name, obj)
    assert errors, (name, obj)
