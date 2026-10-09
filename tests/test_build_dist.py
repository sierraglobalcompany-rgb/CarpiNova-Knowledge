import hashlib
import json
from pathlib import Path
from carpinova_knowledge.build_dist import build_distribution


def _hashes(path: Path):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.glob('*.json'))}


def test_distribution_is_deterministic_and_safe(tmp_path: Path):
    root=Path('.')
    out1=tmp_path/'a'; out2=tmp_path/'b'
    m1=build_distribution(root,'BATCH-000-PILOT',out1)
    m2=build_distribution(root,'BATCH-000-PILOT',out2)
    assert _hashes(out1)==_hashes(out2)
    assert m1==m2
    knowledge=json.loads((out1/'knowledge.bundle.json').read_text(encoding='utf-8'))
    figures=json.loads((out1/'figures.bundle.json').read_text(encoding='utf-8'))
    lessons=json.loads((out1/'lessons.bundle.json').read_text(encoding='utf-8'))
    assert len(knowledge['pages'])==8
    assert len(figures)==6
    assert len(lessons)>=1
    assert all(r['status']!='EXECUTABLE' for p in knowledge['pages'] for r in p['rules'])
    combined=''.join(p.read_text(encoding='utf-8') for p in out1.glob('*.json'))
    assert '.pdf' not in combined.lower()
    assert '/mnt/data/' not in combined
    assert 'source' in knowledge['pages'][0]['content'][0]
