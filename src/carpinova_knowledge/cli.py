from __future__ import annotations

import argparse
from pathlib import Path
from collections.abc import Sequence


COMMANDS = (
    "audit-book",
    "build-page-map",
    "scaffold-batch",
    "render-docs",
    "validate",
    "build-dist",
    "report-pilot",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="carpinova-knowledge")
    subparsers = parser.add_subparsers(dest="command")
    for command in COMMANDS:
        sub = subparsers.add_parser(command)
        if command == "audit-book":
            sub.add_argument("--pdf", type=Path, required=True)
            sub.add_argument("--book-id", required=True)
            sub.add_argument("--out", type=Path, required=True)
        elif command == "build-page-map":
            sub.add_argument("--audit", type=Path, required=True)
            sub.add_argument("--overrides", type=Path, required=True)
            sub.add_argument("--out", type=Path, required=True)
        elif command == "scaffold-batch":
            sub.add_argument("--batch", type=Path, required=True)
            sub.add_argument("--page-map", type=Path, required=True)
            sub.add_argument("--root", type=Path, default=Path("."))
        elif command == "render-docs":
            sub.add_argument("--page-dir", type=Path, required=True)
        elif command == "validate":
            sub.add_argument("--root", type=Path, default=Path("."))
        elif command == "build-dist":
            sub.add_argument("--root", type=Path, default=Path("."))
            sub.add_argument("--batch", required=True)
            sub.add_argument("--out", type=Path, required=True)
        elif command == "report-pilot":
            sub.add_argument("--root", type=Path, default=Path("."))
            sub.add_argument("--batch", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "audit-book":
        from .audit_book import audit_book

        audit_book(args.pdf, args.book_id, args.out)
    elif args.command == "build-page-map":
        import json

        from .page_map import build_page_map

        audit = json.loads(args.audit.read_text(encoding="utf-8"))
        overrides = json.loads(args.overrides.read_text(encoding="utf-8"))
        result = build_page_map(audit, overrides)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif args.command == "scaffold-batch":
        import json

        from .scaffold_batch import scaffold_batch

        batch = json.loads(args.batch.read_text(encoding="utf-8"))
        page_map = json.loads(args.page_map.read_text(encoding="utf-8"))
        scaffold_batch(batch, page_map, args.root)
    elif args.command == "render-docs":
        from .render_docs import render_page_docs

        render_page_docs(args.page_dir)
    elif args.command == "validate":
        import json

        from .validate_repo import validate_repository

        report = validate_repository(args.root)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["valid"] else 1
    elif args.command == "build-dist":
        import json

        from .build_dist import build_distribution

        manifest = build_distribution(args.root, args.batch, args.out)
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    elif args.command == "report-pilot":
        from .report_pilot import build_pilot_report, render_pilot_report

        report = build_pilot_report(args.root, args.batch)
        out = args.root / "audits" / "f0-pilot-acceptance.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_pilot_report(report), encoding="utf-8")
        print(report["result"])
        return 0 if report["result"] == "GO" else 1
    return 0
