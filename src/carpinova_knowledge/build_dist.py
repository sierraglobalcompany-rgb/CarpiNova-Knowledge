from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def _stable_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def _write(path: Path, obj: Any) -> None:
    path.write_bytes(_stable_bytes(obj))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_distribution(root: Path, batch_id: str, out_dir: Path) -> dict[str, Any]:
    root=Path(root); out_dir=Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    batch_files=list(root.glob('books/*/batches/*.json'))
    batch=None; book_dir=None
    for bf in batch_files:
        obj=_load(bf)
        if obj.get('batch_id')==batch_id:
            batch=obj; book_dir=bf.parent.parent; break
    if batch is None or book_dir is None:
        raise ValueError(f'unknown batch {batch_id}')
    if batch.get('status')!='ACCEPTED':
        raise ValueError('distribution requires ACCEPTED batch')

    page_map=_load(book_dir/'page-map.json')
    physical_by_printed={e['printed_page']:e['pdf_page'] for e in page_map['pages'] if e.get('mapping_status')=='verified'}
    pages=[]; figures=[]
    for printed in batch['printed_pages']:
        pdf=physical_by_printed[printed]
        pd=book_dir/'pages'/f'p{pdf:04d}'
        pages.append({
            'page':_load(pd/'page.json'),
            'content':sorted(_load(pd/'content.json'), key=lambda x:x['id']),
            'measurements':sorted(_load(pd/'measurements.json'), key=lambda x:x['id']),
            'rules':sorted(_load(pd/'rules.json'), key=lambda x:x['id']),
        })
        for f in sorted((pd/'figures').glob('*.json')):
            figures.append(_load(f))

    taxonomy={}
    for tf in sorted((root/'taxonomy').glob('*.json')):
        taxonomy[tf.stem]=_load(tf)
    lessons=[_load(p) for p in sorted((root/'lessons').rglob('*.json'))]
    knowledge={'batch_id':batch_id,'book_id':batch['book_id'],'pages':pages,'taxonomy':taxonomy}
    figures=sorted(figures,key=lambda x:x['id'])
    lessons=sorted(lessons,key=lambda x:x['id'])
    _write(out_dir/'knowledge.bundle.json',knowledge)
    _write(out_dir/'figures.bundle.json',figures)
    _write(out_dir/'lessons.bundle.json',lessons)

    source_manifest=_load(book_dir/'manifest.json')
    manifest={
        'schema_version':'1.0.0',
        'knowledge_version':'0.1.0',
        'book_id':batch['book_id'],
        'batch_id':batch_id,
        'source_manifest_sha256':source_manifest['source_sha256'],
        'files':{
            'knowledge.bundle.json':_sha(out_dir/'knowledge.bundle.json'),
            'figures.bundle.json':_sha(out_dir/'figures.bundle.json'),
            'lessons.bundle.json':_sha(out_dir/'lessons.bundle.json'),
        },
    }
    _write(out_dir/'manifest.json',manifest)
    return manifest
