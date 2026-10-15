# CarpiNova Knowledge — Agent Instructions

These instructions are durable repository guardrails. They do not replace live GitHub state, CI evidence, the canonical source, or a current handoff snapshot.

## Authority

Use this precedence when facts conflict:

1. live GitHub state, exact HEAD files, and exact-head CI;
2. canonical source-backed Knowledge records;
3. published agent/Codex delta;
4. current handoff/audit documents;
5. historical documents or memory.

`CarpiNova-Knowledge` is the canonical structured source of truth. Consumers must not silently reinterpret, complete, or correct canonical records.

## Master laws

### KISS

Apply this order:

`CORRECTO -> SIMPLE -> EFICIENTE -> OPTIMIZADO -> EFICAZ -> ESTABLE -> MANTENIBLE -> RAPIDO -> ESCALABLE SOLO SI HACE FALTA`

Prefer the smallest correct solution. Do not add frameworks, plugin systems, parallel renderers, generic helpers, schema expansion, backend services, or abstractions for hypothetical future needs.

### Anti-noise

Evaluate changes in this order:

`DELETE? -> SIMPLIFY? -> REUSE? -> MERGE? -> OPTIMIZE? -> EXTEND? -> ADD?`

Deletion requires evidence. Before deleting, check references, consumers, tests, workflows, provenance, unique historical evidence, reproducibility, rollback, and forensic value. If safety is not demonstrated, prefer `REVIEW` over `DELETE`.

### Anti-patch

Fix root causes, not symptoms. Do not stack compatibility hacks, test exceptions, duplicated truth, or special cases to force a green result.

## Source fidelity

- Preserve exact-source provenance page by page.
- Keep uncertainty explicit. `UNRESOLVED` is preferable to invented certainty.
- Never create manufacturing authority, dimensions, geometry, labels, or relationships that the source does not support.
- Do not edit `books/cpnc-2025/distribution.json` merely to make a candidate eligible.
- Distribution eligibility is a gate before RED/TDD work.

## Figure contract

- `normalized-2d-v1` is opt-in per FigureSpec through `reconstruction.render_contract`.
- Legacy FigureSpec records remain valid without migration.
- Reuse the existing contract when it fits source-faithfully.
- Defer a figure rather than invent geometry or expand schema/renderer for convenience.
- A new primitive, schema field, renderer capability, or contract version requires an explicit source/contract gate first.
- Do not bump the Knowledge version merely because more existing figures become render-ready.

## Change discipline

Before mutating:

1. read fresh `main`;
2. inspect the exact branch/PR head and compare against `main`;
3. verify there is no overlapping published work;
4. freeze one micro-objective;
5. keep one PR to one cause.

Do not treat handoff SHAs, synthetic merge SHAs, or stale branch names as merge leases.

For an R5-style figure slice, the default sequence is:

`SOURCE -> DISTRIBUTION -> CONTRACT FIT -> KISS/ANTI-NOISE -> FREEZE -> STOP -> RED -> GREEN -> CONSUMER PROOF -> MERGE GATE`

Do not start RED before source/contract freeze.

## Required verification

Run the repository QA before declaring a Knowledge change ready:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
```

If a change affects consumer-visible bundles or FigureSpec behavior, also require consumer compatibility evidence against the intended `CarpiNova-PC` exact head.

## Stop conditions

Stop and re-audit instead of improvising when any of these is true:

- source semantics are ambiguous;
- the candidate is excluded from distribution;
- source-faithful rendering needs a new primitive/schema/renderer contract;
- exact-head CI is red for a product reason;
- `main` moved after the branch was based;
- overlapping agent/Codex work cannot be reconciled;
- a merge would rely on stale or synthetic evidence.

No merge is authorized merely because a branch looks correct. Re-read exact HEAD, compare, CI, scope, and mergeability at the merge gate.
