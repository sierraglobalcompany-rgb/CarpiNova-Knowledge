import json
from pathlib import Path
from carpinova_knowledge.scaffold_batch import scaffold_batch


def test_scaffold_resolves_printed_pages_and_is_idempotent(tmp_path: Path):
    page_map={'pages':[{'pdf_page':p+22,'printed_page':p,'mapping_status':'verified'} for p in range(88,96)]}
    batch={'batch_id':'BATCH-000-PILOT','book_id':'CPNC-2025','printed_pages':list(range(88,96)),'status':'PLANNED'}
    paths=scaffold_batch(batch,page_map,tmp_path)
    assert len(paths)==8
    for p in paths:
        for name in ['page.json','content.json','measurements.json','rules.json','source.md','normalized.md','learning.md']:
            assert (p/name).exists()
        assert (p/'figures').is_dir()
    target=paths[0]/'content.json'
    target.write_text('[{"id":"KEEP"}]',encoding='utf-8')
    scaffold_batch(batch,page_map,tmp_path)
    assert json.loads(target.read_text()) == [{'id':'KEEP'}]


def test_scaffold_fails_on_ambiguous_mapping(tmp_path: Path):
    page_map={'pages':[{'pdf_page':110,'printed_page':88,'mapping_status':'candidate'}]}
    batch={'batch_id':'BATCH-000-PILOT','book_id':'CPNC-2025','printed_pages':[88],'status':'PLANNED'}
    import pytest
    with pytest.raises(ValueError):
        scaffold_batch(batch,page_map,tmp_path)
