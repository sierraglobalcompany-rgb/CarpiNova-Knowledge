from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .ids import page_id
from .render_docs import _render
from .schema_loader import validate_instance


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def _err(errors: list[dict], code: str, path: Path, object_id: str | None = None, field: str | None = None, message: str = '') -> None:
    errors.append({'code':code,'file':str(path),'object_id':object_id,'field':field,'message':message})


def validate_repository(root: Path) -> dict[str, Any]:
    root=Path(root)
    errors: list[dict[str, Any]]=[]
    ids: dict[str, Path]={}
    refs: list[tuple[str,Path,str]]=[]

    page_map_path=root/'books/cpnc-2025/page-map.json'
    if page_map_path.exists():
        pm=_load(page_map_path)
        seen_pdf=set()
        for e in pm.get('pages',[]):
            p=e.get('pdf_page')
            if p in seen_pdf:
                _err(errors,'DUPLICATE_PAGE_MAP',page_map_path,message=f'duplicate pdf_page {p}')
            seen_pdf.add(p)

    for page_dir in sorted(root.glob('books/*/pages/p[0-9][0-9][0-9][0-9]')):
        page_path=page_dir/'page.json'
        if not page_path.exists():
            _err(errors,'MISSING_PAGE_JSON',page_dir)
            continue
        page=_load(page_path)
        for msg in validate_instance('page',page):
            _err(errors,'SCHEMA_ERROR',page_path,page.get('id'),message=msg)
        expected=page_id(str(page.get('book_id','')).upper(),int(page.get('pdf_page',0) or 0)) if page.get('pdf_page') else None
        if expected and page.get('id') != expected:
            _err(errors,'PAGE_ID_MISMATCH',page_path,page.get('id'),message=f'expected {expected}')
        if page.get('id'):
            if page['id'] in ids:
                _err(errors,'DUPLICATE_ID',page_path,page['id'])
            ids[page['id']]=page_path

        content_path=page_dir/'content.json'
        content=_load(content_path) if content_path.exists() else []
        for obj in content:
            for msg in validate_instance('content',obj):
                _err(errors,'SCHEMA_ERROR',content_path,obj.get('id'),message=msg)
            oid=obj.get('id')
            if oid:
                if oid in ids: _err(errors,'DUPLICATE_ID',content_path,oid)
                ids[oid]=content_path
            for ref in obj.get('derived_from_content_ids',[]):
                refs.append((ref,content_path,oid or ''))
        for name,field in [('source.md','source_transcription'),('normalized.md','normalized_text'),('learning.md','learning_text')]:
            path=page_dir/name
            expected_text=_render(content,field)
            if not path.exists() or path.read_text(encoding='utf-8') != expected_text:
                _err(errors,'STALE_MARKDOWN',path,message='generated review view differs from canonical content.json')

        for filename,schema_name in [('measurements.json','measurement'),('rules.json','rule')]:
            path=page_dir/filename
            arr=_load(path) if path.exists() else []
            for obj in arr:
                for msg in validate_instance(schema_name,obj):
                    _err(errors,'SCHEMA_ERROR',path,obj.get('id'),message=msg)
                oid=obj.get('id')
                if oid:
                    if oid in ids: _err(errors,'DUPLICATE_ID',path,oid)
                    ids[oid]=path

        for path in sorted((page_dir/'figures').glob('*.json')) if (page_dir/'figures').exists() else []:
            fig=_load(path)
            for msg in validate_instance('figure',fig):
                _err(errors,'SCHEMA_ERROR',path,fig.get('id'),message=msg)
            oid=fig.get('id')
            if oid:
                if oid in ids: _err(errors,'DUPLICATE_ID',path,oid)
                ids[oid]=path
            src=fig.get('source',{})
            reg=src.get('region',{})
            for k in ('x','y','width','height'):
                v=reg.get(k)
                if not isinstance(v,(int,float)) or not 0 <= v <= 1:
                    _err(errors,'FIGURE_REGION_INVALID',path,oid,k)
            if fig.get('deterministic_required') and (fig.get('preferred_renderer')=='image' or fig.get('generative_image_allowed')):
                _err(errors,'DETERMINISTIC_FIGURE_GENERATIVE_ONLY',path,oid,message='deterministic technical figure cannot depend on generative image rendering')

    for path in sorted(root.glob('lessons/**/*.json')):
        obj=_load(path)
        for msg in validate_instance('lesson',obj):
            _err(errors,'SCHEMA_ERROR',path,obj.get('id'),message=msg)
        oid=obj.get('id')
        if oid:
            if oid in ids: _err(errors,'DUPLICATE_ID',path,oid)
            ids[oid]=path
        for ref in obj.get('content_refs',[])+obj.get('figure_refs',[]):
            refs.append((ref,path,oid or ''))
        for step in obj.get('steps',[]):
            ref=step.get('ref')
            if ref: refs.append((ref,path,oid or ''))

    for ref,path,oid in refs:
        if ref not in ids:
            _err(errors,'UNRESOLVED_REF',path,oid,message=ref)

    return {'errors':errors,'error_count':len(errors),'object_count':len(ids)}
