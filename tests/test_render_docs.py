import json
from pathlib import Path
from carpinova_knowledge.render_docs import render_page_docs


def test_render_docs_regenerates_from_canonical_json(tmp_path: Path):
    records=[
      {'id':'CONTENT-X-P0001-002','source_transcription':'B','normalized_text':'B n','learning_text':'B l'},
      {'id':'CONTENT-X-P0001-001','source_transcription':'A','normalized_text':'A n','learning_text':'A l'},
    ]
    (tmp_path/'content.json').write_text(json.dumps(records),encoding='utf-8')
    render_page_docs(tmp_path)
    source=(tmp_path/'source.md').read_text(encoding='utf-8')
    assert 'GENERATED' in source
    assert source.index('A') < source.index('B')
    (tmp_path/'source.md').write_text('tampered',encoding='utf-8')
    render_page_docs(tmp_path)
    assert 'tampered' not in (tmp_path/'source.md').read_text(encoding='utf-8')
