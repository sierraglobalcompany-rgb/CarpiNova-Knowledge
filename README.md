# CarpiNova Knowledge

Canonical structured knowledge base and validation toolchain for CarpiNova.

The source book PDF is intentionally kept outside Git. The repository stores traceable structured knowledge, schemas, derived review views, validation tooling, and deterministic consumer bundles.

## Full-book version

Current full-book Knowledge candidate version: `1.1.0` on the release branch. The published `main` release remains `1.0.0` until the candidate is explicitly merged.

Canonical source: `cpnc-2025`, `295` physical pages, SHA-256:

`318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`

The canonical extraction remains preserved page by page for provenance. The consumer bundle intentionally excludes `43` confirmed non-technical pages (front matter, non-operational narrative, pure advertising/branding, separators, blank pages and administrative/promotional material) and distributes `252` useful carpentry pages.

The exclusions are explicit in `books/cpnc-2025/distribution.json`; they do not delete or rewrite the canonical page records.

Known source conflicts and safe `UNRESOLVED` items remain explicit instead of being reconciled by inference. No distributed RuleSpec is `EXECUTABLE` fabrication authority.

Knowledge `1.1.0` adds the opt-in `normalized-2d-v1` render contract only to `FIG-CPNC-2025-P0113-001`. Legacy FigureSpec records remain valid and do not require migration.

## Reproduce the full-book bundle

From the repository root:

```bash
uv sync --all-groups
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge build-book-dist --root . --book-id cpnc-2025 --out work/knowledge-1.1.0
```

The build produces four deterministic consumer artifacts:

- `knowledge.bundle.json`
- `figures.bundle.json`
- `lessons.bundle.json`
- `manifest.json`

For this candidate, `manifest.json` identifies `scope=BOOK`, `book_id=cpnc-2025`, `knowledge_version=1.1.0`, the canonical source SHA-256, `source_page_count=295`, the explicit exclusion count, record counts and hashes of the generated bundle files.

`work/` is local scratch space and is not committed. The source PDF is also excluded from Git. Generated bundles are reproducible artifacts, not source-of-truth inputs.

## Release evidence

- Knowledge 1.1 candidate review: `docs/releases/1.1.0-review.md`
- Knowledge 1.1 stable release record: `docs/releases/1.1.0.md`
- Knowledge 1.0 final review: `docs/releases/1.0.0-review.md`
- Knowledge 1.0 release record: `docs/releases/1.0.0.md`
- Historical RC record: `docs/releases/1.0.0-rc.1.md`

## Governance

- Editorial transformations: `docs/editorial-policy.md`
- Technical validation: `docs/validation-policy.md`
- Visual reconstruction: `docs/visual-spec-policy.md`
