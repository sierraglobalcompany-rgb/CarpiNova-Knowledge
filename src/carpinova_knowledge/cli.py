from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

COMMANDS = (
    'audit-book',
    'build-page-map',
    'scaffold-batch',
    'render-docs',
    'validate',
    'build-dist',
    'report-pilot',
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='carpinova_knowledge')
    sub = parser.add_subparsers(dest='command')

    p = sub.add_parser('audit-book')
    p.add_argument('--pdf', required=True)
    p.add_argument('--book-id', required=True)
    p.add_argument('--out', required=True)

    p = sub.add_parser('build-page-map')
    p.add_argument('--audit', required=True)
    p.add_argument('--overrides', required=True)
    p.add_argument('--out', required=True)

    p = sub.add_parser('scaffold-batch')
    p.add_argument('--batch', required=True)
    p.add_argument('--page-map', required=True)
    p.add_argument('--root', default='.')

    p = sub.add_parser('render-docs')
    p.add_argument('--root', default='.')
    p.add_argument('--page-dir')

    p = sub.add_parser('validate')
    p.add_argument('--root', default='.')

    p = sub.add_parser('build-dist')
    p.add_argument('--root', default='.')
    p.add_argument('--batch', required=True)
    p.add_argument('--out', required=True)

    p = sub.add_parser('report-pilot')
    p.add_argument('--root', default='.')
    p.add_argument('--batch', required=True)
    p.add_argument('--out')

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    if args.command == 'audit-book':
        from .audit_book import audit_book
        audit_book(Path(args.pdf), args.book_id, Path(args.out))
        return 0
    if args.command == 'build-page-map':
        from .page_map import write_page_map
        write_page_map(Path(args.audit), Path(args.overrides), Path(args.out))
        return 0
    if args.command == 'scaffold-batch':
        from .scaffold_batch import scaffold_batch
        batch=json.loads(Path(args.batch).read_text(encoding='utf-8'))
        page_map=json.loads(Path(args.page_map).read_text(encoding='utf-8'))
        scaffold_batch(batch,page_map,Path(args.root))
        return 0
    if args.command == 'render-docs':
        from .render_docs import render_page_docs
        if args.page_dir:
            render_page_docs(Path(args.page_dir))
        else:
            for pd in sorted(Path(args.root).glob('books/*/pages/p[0-9][0-9][0-9][0-9]')):
                render_page_docs(pd)
        return 0
    if args.command == 'validate':
        from .validate_repo import validate_repository
        report=validate_repository(Path(args.root))
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 1 if report['errors'] else 0
    if args.command == 'build-dist':
        from .build_dist import build_distribution
        manifest=build_distribution(Path(args.root),args.batch,Path(args.out))
        print(json.dumps(manifest,ensure_ascii=False,indent=2))
        return 0
    if args.command == 'report-pilot':
        from .report_pilot import build_pilot_report, render_report
        report=build_pilot_report(Path(args.root),args.batch)
        text=render_report(report)
        if args.out:
            Path(args.out).parent.mkdir(parents=True,exist_ok=True)
            Path(args.out).write_text(text,encoding='utf-8')
        print(text,end='')
        return 0 if report['result']=='GO' else 1
    raise AssertionError(args.command)
