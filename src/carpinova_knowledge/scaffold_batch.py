from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping
from .ids import page_id
from .render_docs import render_page_docs


def _write_if_missing(path: Path, obj: Any) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def scaffold_batch(batch: Mapping[str,Any], page_map: Mapping[str,Any], root: Path) -> list[Path]:
    root=Path(root)
    by_printed={
        p.get('printed_page'):p for p in page_map.get('pages',[])
        if p.get('printed_page') is not None and p.get('mapping_status')=='verified'
    }
    paths=[]
    book_id=str(batch['book_id']).upper()
    for printed in batch['printed_pages']:
        entry=by_printed.get(printed)
        if not entry:
            raise ValueError(f'printed page {printed} is missing or not verified')
        pdf_page=int(entry['pdf_page'])
        page_dir=root/'books'/str(batch['book_id']).lower()/'pages'/f'p{pdf_page:04d}'
        page_dir.mkdir(parents=True,exist_ok=True)
        (page_dir/'figures').mkdir(exist_ok=True)
        _write_if_missing(page_dir/'page.json',{
            'id':page_id(book_id,pdf_page),
            'book_id':book_id,
            'pdf_page':pdf_page,
            'printed_page':printed,
            'topics':[],
            'contains':{'text':False,'figures':False},
        })
        for name in ['content.json','measurements.json','rules.json']:
            _write_if_missing(page_dir/name,[])
        render_page_docs(page_dir)
        paths.append(page_dir)
    return paths
