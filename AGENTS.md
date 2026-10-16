# CarpiNova Knowledge — Agent Instructions

These are durable repository guardrails for ChatGPT, Codex, Copilot, and other agents. They do not replace live GitHub state, exact-head CI, the canonical source, or the current recovery handoff.

## Authority

When facts conflict, use this precedence:

1. live GitHub state, exact HEAD files, exact-head CI and published agent/Codex delta;
2. canonical source-backed Knowledge records;
3. current approved contract/checkpoint;
4. current handoff/audit document;
5. historical documents or memory.

`CarpiNova-Knowledge` is the canonical structured source of truth. Consumers must not silently reinterpret, complete, or correct canonical records.

## Master laws

### KISS — smallest correct solution

Apply this order:

`CORRECTO -> SIMPLE -> EFICIENTE -> OPTIMIZADO -> EFICAZ -> ESTABLE -> MANTENIBLE -> RAPIDO -> ESCALAR SOLO SI HACE FALTA`

Prefer `A -> B` when it solves the problem correctly. Do not add frameworks, plugin systems, parallel renderers, generic helpers, schema expansion, backend services, or abstractions for hypothetical future needs.

### Anti-noise

Evaluate changes in this order:

`DELETE? -> SIMPLIFY? -> REUSE? -> MERGE? -> OPTIMIZE? -> EXTEND? -> ADD?`

Deletion requires evidence. Before deleting, check references, consumers, tests, workflows, provenance, unique historical evidence, reproducibility, rollback, and forensic value. If safety is not demonstrated, prefer `REVIEW` over `DELETE`.

Do not carry stale docs, duplicate truth, temporary workflows, historical experiments, or unrelated files into a product PR.

### Anti-patch / root cause

Use this sequence:

`OBSERVE -> REPRODUCE -> ISOLATE -> SOURCE AUDIT -> ROOT CAUSE -> REAL RED -> MINIMAL FIX -> REMOVE OBSOLETE WORKAROUND -> GREEN -> REGRESSION -> CONSUMER`

Do not stack exceptions, flags, fallbacks, helpers, special cases, or figure-ID branches to force a green result.

If the root cause cannot be stated in one clear sentence, stop before fixing.

## Source fidelity

- `SOURCE TRUTH > CANONICAL KNOWLEDGE > CONTRACT > TEST > IMPLEMENTATION`.
- `UNRESOLVED > INVENTED`.
- Preserve exact-source provenance page by page.
- Never create manufacturing authority, dimensions, geometry, labels, relationships, capacities, angles, or tolerances that the source does not support.
- Normalized coordinates are presentation geometry, not physical measurements.
- Do not infer mm/cm/inches from bounds, proportions, placements, screenshots, OCR uncertainty, or neighboring figures.
- Do not import measurements from another figure on the same page unless the canonical relationship explicitly supports it.
- Do not edit `books/cpnc-2025/distribution.json` merely to make a candidate eligible.
- Distribution eligibility is a gate before RED/TDD work.

## Figure contract

- `normalized-2d-v1` is opt-in per FigureSpec through `reconstruction.render_contract`.
- Legacy FigureSpec records remain valid without migration.
- Reuse the existing contract when it fits source-faithfully.
- Existing normalized primitives are `rect`, `line`, and `polyline`; annotations provide text.
- A new primitive, schema field, renderer capability, or contract version requires a separate SOURCE/CONTRACT gate first.
- Defer a figure rather than invent geometry or inflate schema/renderer for convenience.
- Do not bump the Knowledge version merely because more existing figures become render-ready.
- Every layer reference must be deterministic; entities and annotations must not be silently duplicated or omitted.
- JSON semantic equality is more important than textual key order unless order is explicitly part of the contract.

## Ten-pass audit before implementation

Apply these ten checks to code, docs, prompts, and merge gates:

1. **Identity** — repo, owner, `main`, branch, PR, exact head, version.
2. **Micro-objective** — one cause only; split independent work.
3. **Source truth** — page, figure, text, inventory, measurements, relationships, annotations, provenance.
4. **Contract fit / distribution** — `REUSE`, `EXTEND`, or `DEFER`; verify distribution eligibility before RED.
5. **KISS** — remove unnecessary layers, helpers, primitives, frameworks, workflows, and side effects.
6. **Anti-noise** — classify files as `NEEDED`, `RELATED_BUT_NOT_NEEDED`, or `UNRELATED`; only `NEEDED` enters the PR.
7. **Anti-patch** — confirm root cause, not an exception.
8. **TDD / QA** — real RED, correct failure, minimal GREEN, focal tests, full suite, lint/validator.
9. **Consumer / regression** — real generated bundle and semantic assertions when consumer-visible behavior changes.
10. **Governance** — fresh main/head/compare/CI/reviews/mergeability, expected-head merge, postmerge QA, cleanup, checkpoint.

A material contradiction at any pass means `STOP` and re-audit; do not compensate with more architecture.

## Change discipline

Before mutating:

1. read fresh `main`;
2. inspect open PRs/issues and any published Codex/agent delta;
3. inspect exact branch/PR head and compare against `main`;
4. freeze one micro-objective;
5. identify allowed and forbidden files;
6. define RED/GREEN evidence and STOP condition.

Keep one PR to one cause. Do not mix product R5 work with README/governance cleanup.

Do not treat handoff SHAs, branch names, synthetic merge refs, historical green CI, or “Codex done” as future merge leases.

## R5 figure-slice sequence

Default sequence:

`SOURCE/DISCOVERY -> DISTRIBUTION -> CONTRACT FIT -> KISS/ANTI-NOISE -> FREEZE -> CHECKPOINT/STOP -> RED -> CHECKPOINT/STOP -> GREEN -> KNOWLEDGE QA -> CHECKPOINT/STOP -> PC PREMERGE PROOF -> CLEANUP ZERO DELTA -> MERGE READINESS -> EXPECTED-HEAD MERGE -> POSTMERGE KNOWLEDGE QA -> PC FULL-STATE PROOF -> CLEANUP ZERO DELTA -> FINAL CHECKPOINT -> CLOSED`

One execution should advance only the currently frozen gate unless a larger scope was explicitly authorized. Do not chain the next slice automatically.

## Required verification

Run Knowledge QA before declaring a Knowledge change ready:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
```

If a change affects consumer-visible bundles or FigureSpec behavior, also require consumer compatibility evidence against the intended exact `CarpiNova-PC` head using the real generated Knowledge bundle.

A synthetic fixture alone is not sufficient consumer proof.

## Temporary audit hygiene

Temporary consumer-proof workflows/branches are audit tools, not product.

After evidence capture:

- close the temporary PR without merge;
- reset the temporary branch only with force-with-lease and a known expected SHA;
- compare against the intended PC main;
- require `ahead=0`, `behind=0`, `files=[]`.

Never force `main`.

## Merge and closure

Immediately before merge, re-read fresh `main`, PR head, compare, exact-head CI, review threads, scope, and mergeability. Merge with expected-head protection.

`MERGED != CLOSED` until postmerge Knowledge QA, required PC full-state proof, temporary cleanup, and durable checkpoint are complete.

## Stop conditions

Stop and classify instead of improvising when any of these is true:

- `main` moved and the delta was not audited;
- overlapping Codex/agent work is unknown;
- source semantics are ambiguous;
- the candidate is excluded from distribution;
- a test requires invented truth;
- source-faithful rendering needs a new primitive/schema/renderer contract without a gate;
- PC would need duplicated canonical truth or a source-specific special case;
- an unrelated file appears in the delta;
- CI failure is unexplained or the runner executed no steps;
- a temporary branch cannot return to zero delta;
- merge head changed;
- docs/governance and product are mixed;
- a version bump appears without an explicit release decision.

No merge is authorized merely because a branch looks correct. Evidence and the current approved gate control execution.
