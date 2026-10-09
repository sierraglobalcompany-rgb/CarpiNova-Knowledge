from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from typing import Any
from .validate_repo import validate_repository


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def build_pilot_report(root: Path, batch_id: str) -> dict[str, Any]:
    root=Path(root)
    batch_path=None
    for p in root.glob('books/*/batches/*.json'):
        obj=_load(p)
        if obj.get('batch_id')==batch_id:
            batch_path=p; batch=obj; break
    if batch_path is None:
        raise ValueError(f'unknown batch {batch_id}')
    book_dir=batch_path.parent.parent
    page_map=_load(book_dir/'page-map.json')
    by_printed={p.get('printed_page'):p for p in page_map.get('pages',[]) if p.get('printed_page') is not None}
    findings=[]
    page_dirs=[]
    figures=[]; measurements=[]; rules=[]; contents=[]
    reconstruction=[]
    for printed in batch['printed_pages']:
        entry=by_printed.get(printed)
        if not entry or entry.get('mapping_status')!='verified':
            findings.append(f'Printed page {printed} mapping is ambiguous or unverified')
            continue
        pd=book_dir/'pages'/f"p{int(entry['pdf_page']):04d}"
        page_dirs.append(pd)
        required=['page.json','content.json','measurements.json','rules.json','source.md','normalized.md','learning.md']
        for name in required:
            if not (pd/name).exists(): findings.append(f'Missing required page file {pd/name}')
        if not (pd/'page.json').exists():
            continue
        page=_load(pd/'page.json')
        page_figs=[_load(f) for f in sorted((pd/'figures').glob('*.json'))] if (pd/'figures').exists() else []
        if page.get('contains',{}).get('figures') and not page_figs:
            findings.append(f'Meaningful visual declared on page {printed} but no FigureSpec exists')
        figures.extend(page_figs)
        if (pd/'content.json').exists(): contents.extend(_load(pd/'content.json'))
        if (pd/'measurements.json').exists(): measurements.extend(_load(pd/'measurements.json'))
        if (pd/'rules.json').exists(): rules.extend(_load(pd/'rules.json'))
        for fig in page_figs:
            ok=True
            if not fig.get('entities'): ok=False
            precision=(fig.get('geometry') or {}).get('precision')
            if precision not in {'exact','approximate','unknown'}: ok=False
            if not fig.get('preferred_renderer'): ok=False
            if fig.get('type') in {'technical_diagram','dimensioned_drawing','table','mixed'} and fig.get('deterministic_required') and fig.get('preferred_renderer')=='image': ok=False
            reconstruction.append({'figure_id':fig.get('id'),'result':'PASS' if ok else 'FAIL'})
            if not ok: findings.append(f'Figure reconstruction incomplete: {fig.get("id")}')

    validation=validate_repository(root)
    if validation['error_count']:
        findings.append(f"Repository validator reports {validation['error_count']} error(s)")
    for m in measurements:
        source=m.get('source',{})
        if not source.get('region'):
            findings.append(f"Technical measurement lacks source location: {m.get('id')}")
    lessons=[_load(p) for p in sorted((root/'lessons').rglob('*.json'))]
    figure_types=Counter(f.get('type','unknown') for f in figures)
    measurement_states=Counter(m.get('status','unknown') for m in measurements)
    result='GO' if not findings and all(x['result']=='PASS' for x in reconstruction) else 'NO_GO'
    return {
        'result':result,
        'batch_id':batch_id,
        'book_id':batch['book_id'],
        'counts':{'pages':len(page_dirs),'contents':len(contents),'figures':len(figures),'measurements':len(measurements),'rules':len(rules),'lessons':len(lessons)},
        'figure_types':dict(sorted(figure_types.items())),
        'measurement_states':dict(sorted(measurement_states.items())),
        'validation_errors':validation['error_count'],
        'reconstruction':reconstruction,
        'findings':findings,
    }


def render_report(report: dict[str, Any]) -> str:
    lines=['# CarpiNova Knowledge F0 — Auditoría de aceptación del piloto','',f"**Resultado: {report['result']}**",'',f"- Lote: `{report['batch_id']}`",f"- Libro: `{report['book_id']}`"]
    labels={'pages':'Páginas','contents':'Contenidos','figures':'Figuras','measurements':'Medidas','rules':'Reglas candidatas','lessons':'Lecciones'}
    for k in ['pages','contents','figures','measurements','rules','lessons']:
        lines.append(f"- {labels[k]}: {report['counts'][k]}")
    lines.append(f"- Errores del validador: {report['validation_errors']}")
    lines += ['', '## Figuras por tipo', '']
    for k,v in report['figure_types'].items(): lines.append(f'- {k}: {v}')
    lines += ['', '## Medidas por estado', '']
    for k,v in report['measurement_states'].items(): lines.append(f'- {k}: {v}')
    lines += ['', '## Auditoría de reconstrucción', '']
    for item in report['reconstruction']: lines.append(f"- `{item['figure_id']}`: {item['result']}")
    lines += ['', '## Hallazgos', '']
    if report['findings']:
        lines.extend(f'- {x}' for x in report['findings'])
    else:
        lines.append('- Sin hallazgos bloqueantes.')
    return '\n'.join(lines)+'\n'
