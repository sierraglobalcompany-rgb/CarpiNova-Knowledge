# CarpiNova Knowledge

Canonical structured knowledge base and validation toolchain for CarpiNova.

The source book PDF is intentionally kept outside Git. This repository stores traceable structured knowledge, schemas, derived review views, validation tooling and deterministic consumer bundles.

## Operating model

CarpiNova follows four durable laws:

1. **KISS** — choose the smallest correct path; prefer `A -> B` over unnecessary architecture or process.
2. **Anti-noise** — delete/simplify/reuse before adding; do not duplicate truth, historical execution or temporary artifacts.
3. **Anti-patch** — isolate and fix root causes; do not stack special cases or compatibility hacks to force green.
4. **Design** — user-visible output must be clear, consistent, accessible and faithful to the approved product direction without inventing source truth.

The complete binding rules are in `AGENTS.md`.

Routine source-backed work that fits existing contracts is handled in cohesive batches rather than with a forensic gate chain per figure:

```text
SOURCE BATCH
-> CONTRACT / DISTRIBUTION CHECK
-> TDD IMPLEMENT
-> KNOWLEDGE QA
-> PC REAL-BUNDLE PROOF (when consumer-visible)
-> MERGE
-> POSTMERGE SMOKE
-> CHECKPOINT / CLOSE
```

The extended forensic flow is reserved for real architecture/source-risk changes such as a new schema, primitive, renderer, interaction, version/distribution behavior, destructive migration or unresolved source conflict.

### Continuity after a chat/session ends

Do not rely on a private conversation transcript. Recover the project from live GitHub in this order:

1. read this `README.md` and `AGENTS.md`;
2. read fresh `main` and its exact SHA;
3. inspect open issues and pull requests;
4. inspect the current PR diff and exact-head CI;
5. continue from the active issue/PR checkpoint.

Current execution state belongs in GitHub issues/PRs, not in a permanently stale README. Git history is the historical archive; routine checkpoints should not be copied into new Markdown files.

## Full-book version

Current full-book Knowledge version on `main`: `1.2.0`.

Canonical source: `cpnc-2025`, `295` physical pages, SHA-256:

`318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`

The canonical extraction remains preserved page by page for provenance. The consumer bundle intentionally excludes `43` confirmed non-technical pages (front matter, non-operational narrative, pure advertising/branding, separators, blank pages and administrative/promotional material) and distributes `252` useful carpentry pages.

The exclusions are explicit in `books/cpnc-2025/distribution.json`; they do not delete or rewrite the canonical page records.

Known source conflicts and safe `UNRESOLVED` items remain explicit instead of being reconciled by inference. No distributed RuleSpec is `EXECUTABLE` fabrication authority.

Knowledge `1.2.0` includes source-backed lesson interactions with strict schemas and fail-closed reference validation while preserving the opt-in `normalized-2d-v1` render contract.

A FigureSpec is render-ready only when its canonical record explicitly declares:

```text
reconstruction.render_contract = normalized-2d-v1
```

That capability is opt-in per figure. Legacy FigureSpec records remain valid and do not require forced migration. Discover render-ready figures from canonical FigureSpec records or the generated `figures.bundle.json`; do not maintain a second manual inventory.

Figures whose source semantics cannot be represented faithfully by the current contract remain deferred rather than having geometry or dimensions invented.

## Figure rendering boundary

The current normalized contract intentionally stays small:

- `rect`
- `line`
- `polyline`
- canonical annotations/layers
- normalized presentation coordinates

Do not add a primitive, renderer, schema field or contract version simply to make one figure fit. Such a change is an architecture decision and must demonstrate a real source-backed need.

Normalized coordinates and placements are presentation geometry, not physical dimensions.

## Reproduce the full-book bundle

From the repository root:

```bash
uv sync --all-groups
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge build-book-dist --root . --book-id cpnc-2025 --out work/knowledge-1.2.0
```

The build produces four deterministic consumer artifacts:

- `knowledge.bundle.json`
- `figures.bundle.json`
- `lessons.bundle.json`
- `manifest.json`

`manifest.json` identifies `scope=BOOK`, `book_id=cpnc-2025`, `knowledge_version=1.2.0`, the canonical source SHA-256, `source_page_count=295`, the explicit exclusion count, record counts and hashes of the generated bundle files.

`work/` is local scratch space and is not committed. The source PDF is also excluded from Git. Generated bundles are reproducible artifacts, not source-of-truth inputs.

## Required QA

Before a Knowledge change is declared ready:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
```

When the change is consumer-visible, verify the exact Knowledge SHA against the intended exact `CarpiNova-PC` SHA using PC's permanent real-bundle consumer-proof workflow. Do not create a new temporary workflow/PR for each routine figure.

## Design reference boundary

CarpiNova uses relevant principles from the public `nextlevelbuilder/ui-ux-pro-max-skill` project as an advisory UX/design reference. CarpiNova does **not** vendor or depend on that project's CLI, search databases or architecture. The product's approved mockup and design rules live on the consumer side (`CarpiNova-PC`); Knowledge remains the source-faithful data/contract layer.

## Documentation policy

Keep durable information in the smallest correct place:

- `AGENTS.md` — permanent agent/governance rules.
- `README.md` — stable architecture, commands and recovery path.
- GitHub issues/PRs — active work, exact SHAs, current checkpoints and blockers.
- `docs/releases/` — durable release evidence.
- policy docs — dedicated long-lived rules only when they add unique value.
- Git history — routine historical execution.

Do not duplicate plans/specs/checkpoints across Knowledge and PC or commit chat handoffs and local verification diaries as routine project state.

## Release evidence

- Knowledge 1.2 release record: `docs/releases/1.2.0.md`
- Knowledge 1.1 final review: `docs/releases/1.1.0-review.md`
- Knowledge 1.1 release record: `docs/releases/1.1.0.md`
- Knowledge 1.0 final review: `docs/releases/1.0.0-review.md`
- Knowledge 1.0 release record: `docs/releases/1.0.0.md`
- Historical RC record: `docs/releases/1.0.0-rc.1.md`

## Governance

- Durable agent guardrails: `AGENTS.md`
- Editorial transformations: `docs/editorial-policy.md`
- Technical validation: `docs/validation-policy.md`
- Visual reconstruction: `docs/visual-spec-policy.md`
