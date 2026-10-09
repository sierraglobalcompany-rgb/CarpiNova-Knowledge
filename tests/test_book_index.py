import json
from pathlib import Path


def test_index_ranges_and_taxonomy_are_consistent():
    root = Path('.')
    index = json.loads((root/'books/cpnc-2025/index.json').read_text(encoding='utf-8'))
    page_map = json.loads((root/'books/cpnc-2025/page-map.json').read_text(encoding='utf-8'))
    max_pdf = max(p['pdf_page'] for p in page_map['pages'])
    sections = index['sections']
    for section in sections:
        pr = section['physical_range']
        assert 1 <= pr['start'] <= pr['end'] <= max_pdf
    hits = [s for s in sections if s['printed_range']['start'] <= 91 <= s['printed_range']['end']]
    assert len(hits) == 1
    assert hits[0]['section_id'] == 'step-2-hardware'

    canonical = set()
    aliases = []
    for name in ['materials','hardware','furniture','construction-systems','procedures','glossary']:
        data = json.loads((root/f'taxonomy/{name}.json').read_text(encoding='utf-8'))
        for item in data['items']:
            assert item['id'] not in canonical
            canonical.add(item['id'])
            aliases.extend(item.get('aliases', []))
    assert len(canonical) >= 10
    assert all(isinstance(a, str) and a.strip() for a in aliases)
