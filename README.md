# CarpiNova Knowledge

Canonical structured knowledge base and validation toolchain for CarpiNova.

The source book PDF is intentionally kept outside Git. The repository stores traceable structured knowledge, schemas, derived review views, validation tooling, and versioned consumer bundles.

## Release status

Stable validated release: `0.1.0` (F0 pilot).

Current F1 release candidate: `1.0.0-rc.1`.

The F1 candidate covers the complete canonical book `cpnc-2025` (295 physical pages) and preserves the source fingerprint:

`318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`

The global F1 automated audit has no automatic blockers and repository QA is green. This does **not** make `1.0.0-rc.1` a final release: technical/editorial review, the pre-main integration audit, explicit human approval for F1 → `main`, post-merge `main` CI, and the final release step are still required.

No rule in the F1 candidate is executable fabrication authority. Known source conflicts remain explicit instead of being silently reconciled.

## Reproduce the full-book bundle

From the repository root:

```bash
uv sync --all-groups
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge build-book-dist --root . --book-id cpnc-2025 --out work/f1-bundle
```

The build produces four deterministic consumer artifacts:

- `knowledge.bundle.json`
- `figures.bundle.json`
- `lessons.bundle.json`
- `manifest.json`

`manifest.json` identifies the bundle with `scope=BOOK`, `book_id=cpnc-2025`, `knowledge_version=1.0.0-rc.1`, the canonical source SHA-256, record counts, and hashes of the generated bundle files.

`work/` is local scratch space and is not committed. The source PDF is also excluded from Git.

## Governance

- Editorial transformations: `docs/editorial-policy.md`
- Technical validation: `docs/validation-policy.md`
- Visual reconstruction: `docs/visual-spec-policy.md`
- F1 candidate notes and human review plan: `docs/releases/1.0.0-rc.1.md`
