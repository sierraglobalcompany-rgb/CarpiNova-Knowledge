from carpinova_knowledge.page_map import build_page_map


def _audit(texts):
    return {'pages':[{'pdf_page':i+1,'height':1000,'text_blocks':[{'bbox':[0,950,100,990],'text':t,'block_no':0,'block_type':0}]} for i,t in enumerate(texts)]}


def test_page_map_preserves_every_physical_page_and_candidates():
    result = build_page_map(_audit(['','1','2']), {})
    assert [x['pdf_page'] for x in result['pages']] == [1,2,3]
    assert result['pages'][0]['mapping_status'] in {'unresolved','not_printed'}
    assert result['pages'][1]['printed_page'] == 1
    assert result['pages'][1]['mapping_status'] == 'candidate'


def test_explicit_overrides_are_verified_and_null_is_not_printed():
    result = build_page_map(_audit(['9','9','9']), {1:None,2:88,3:89})
    assert result['pages'][0]['printed_page'] is None
    assert result['pages'][0]['mapping_status'] == 'not_printed'
    assert result['pages'][1]['printed_page'] == 88
    assert result['pages'][1]['mapping_status'] == 'verified'
    assert result['pages'][2]['printed_page'] == 89


def test_duplicate_candidates_are_marked_unresolved():
    result = build_page_map(_audit(['7','7']), {})
    assert all(x['mapping_status'] == 'unresolved' for x in result['pages'])


def test_write_page_map_reads_gzip_audit(tmp_path):
    import gzip, json
    from carpinova_knowledge.page_map import write_page_map
    audit={"pages":[{"pdf_page":1,"height":100,"text_blocks":[]}]}
    audit_path=tmp_path/"raw-page-audit.json.gz"
    with gzip.open(audit_path,"wt",encoding="utf-8") as fh:
        json.dump(audit,fh)
    overrides=tmp_path/"overrides.json"
    overrides.write_text('{"1":null}',encoding='utf-8')
    out=tmp_path/"page-map.json"
    result=write_page_map(audit_path,overrides,out)
    assert result["pages"][0]["mapping_status"]=="not_printed"
