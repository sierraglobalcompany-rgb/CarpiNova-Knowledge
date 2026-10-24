# CarpiNova Knowledge — Agent Instructions

These are durable repository guardrails for ChatGPT, Codex, Copilot, and other agents. They are intentionally compact. Live GitHub state and canonical source evidence remain authoritative for current facts.

## Authority and recovery

When facts conflict, use this precedence:

1. live GitHub state: exact `main`, branch/PR heads, compare, CI, reviews and open issues;
2. canonical source-backed Knowledge records for carpentry facts and provenance;
3. these durable `AGENTS.md` rules;
4. the active issue/PR contract or checkpoint for the current work item;
5. `README.md` and current release records;
6. historical documents, old checkpoints or memory.

A new chat/session must recover state from the repositories, not from memory: read `AGENTS.md`, `README.md`, fresh `main`, open issues/PRs, exact diffs and exact-head CI before continuing.

`CarpiNova-Knowledge` is the canonical structured source of truth. Consumers must not silently reinterpret, complete or correct canonical records.

## The four master laws

These four laws apply to every change. They are not optional review notes.

### 1. KISS — smallest correct path

Apply this order:

`CORRECTO -> SIMPLE -> EFICIENTE -> OPTIMIZADO -> EFICAZ -> ESTABLE -> MANTENIBLE -> RAPIDO -> ESCALAR SOLO SI HACE FALTA`

Prefer `A -> B` when it solves the problem correctly. Do not add frameworks, plugin systems, parallel renderers, generic helpers, schema expansion, backend services, compatibility layers, workflows or abstractions for hypothetical future needs.

A safeguard that costs more complexity than the risk it controls must be simplified. Repetition of audit ceremony is also complexity.

### 2. Anti-noise — keep only useful truth

Evaluate changes in this order:

`DELETE? -> SIMPLIFY? -> REUSE? -> MERGE? -> OPTIMIZE? -> EXTEND? -> ADD?`

Do not accumulate stale docs, duplicate truth, copied plans, temporary workflows, obsolete branches, historical experiments or unrelated files.

Deletion still requires evidence. Before deleting, check references, consumers, tests, workflows, provenance, reproducibility, rollback and unique forensic value. If safety is not demonstrated, classify `REVIEW` instead of guessing.

Git history is the default historical archive. Routine execution history does not need another committed Markdown copy.

### 3. Anti-patch — root cause before fix

Use this sequence:

`OBSERVE -> REPRODUCE -> ISOLATE -> SOURCE AUDIT -> ROOT CAUSE -> REAL RED -> MINIMAL FIX -> REMOVE OBSOLETE WORKAROUND -> GREEN -> REGRESSION -> CONSUMER`

Do not stack exceptions, flags, fallbacks, helpers, compatibility hacks, figure-ID branches or special cases to force green.

If the root cause cannot be stated clearly, stop before changing production behavior.

### 4. Design law — clear, consistent, accessible, source-faithful

Apply this order to user-visible/rendered behavior:

`APPROVED DIRECTION -> TOKENS/CONTRACT -> HIERARCHY -> COMPONENTS -> STATES -> RESPONSIVE -> ACCESSIBILITY -> POLISH`

Design must never become a second source of truth. A better-looking reconstruction may not invent dimensions, labels, relationships, geometry, URLs, QR payloads, capacities, tolerances or technical authority.

Normalized geometry is presentation geometry, never a physical measurement.

The external UI/UX Pro Max project (`nextlevelbuilder/ui-ux-pro-max-skill`) is an advisory design reference only. Reuse relevant principles; do **not** vendor its CLI, databases, search engine, framework or architecture into CarpiNova unless a separate demonstrated need is approved.

The approved CarpiNova product mockup is the visual authority in `CarpiNova-PC`; Knowledge supplies source-faithful data/contracts, not UI aesthetics.

## Source fidelity

- `SOURCE TRUTH > CANONICAL KNOWLEDGE > CONTRACT > TEST > IMPLEMENTATION`.
- `UNRESOLVED > INVENTED`.
- Preserve exact-source provenance page by page.
- Never create manufacturing authority, dimensions, geometry, labels, relationships, capacities, angles or tolerances unsupported by the source.
- Do not infer mm/cm/inches from bounds, proportions, placements, screenshots, OCR uncertainty or neighboring figures.
- Do not import values from another figure/page unless the canonical relationship explicitly supports it.
- Do not edit `books/cpnc-2025/distribution.json` merely to make a candidate eligible.
- Distribution eligibility is checked before implementation.

## Figure contract

- `normalized-2d-v1` is opt-in per FigureSpec through `reconstruction.render_contract`.
- Legacy FigureSpec records remain valid without forced migration.
- Reuse the existing contract when it fits source-faithfully.
- Existing normalized primitives are `rect`, `line` and `polyline`; annotations provide text.
- A new primitive, schema field, renderer capability or contract version requires a separate contract decision because it changes architecture.
- Defer a figure rather than invent geometry or inflate schema/renderer for convenience.
- Do not bump Knowledge version merely because more existing figures become render-ready.
- Layer references must be deterministic; entities and annotations must not be silently duplicated or omitted.

## Default delivery flow — KISS batches

Routine work using existing contracts follows:

`SOURCE BATCH -> CONTRACT/DISTRIBUTION CHECK -> TDD IMPLEMENT -> KNOWLEDGE QA -> PC REAL-BUNDLE PROOF IF CONSUMER-VISIBLE -> MERGE -> POSTMERGE SMOKE -> CHECKPOINT/CLOSE`

Rules:

- Prefer a cohesive batch of roughly 10–20 pages when source semantics and the same existing contract allow it. Reduce batch size when ambiguity or a new contract boundary appears.
- One PR means one cohesive cause/batch, not necessarily one figure.
- Routine figures using the existing contract do **not** require a temporary PC branch/workflow/PR per figure.
- Do not create artificial STOP gates between every mechanical substep.
- If an active issue explicitly freezes a next gate, honor that checkpoint; otherwise continue through the normal flow until the next material decision, failure or merge boundary.

Use the older extended forensic sequence only when justified by one of these conditions:

- new schema/primitive/renderer/interaction/version/distribution behavior;
- destructive migration or compatibility removal;
- ambiguous or conflicting source truth;
- unexplained CI/regression failure;
- security-sensitive behavior;
- a cross-repository change whose consumer impact is not already covered by the reusable proof path.

## Ten-pass audit

Run these ten passes before implementation/merge; record only material findings, not ceremonial prose:

1. **Identity** — repo, owner, exact `main`, branch/PR head, version.
2. **Objective/batch** — one cohesive cause; split unrelated work.
3. **Source truth** — page/figure/text/provenance/measurements/relationships/annotations.
4. **Contract/distribution** — reuse, extend or defer; verify eligibility.
5. **KISS** — remove unnecessary layers, helpers, workflows and side effects.
6. **Anti-noise** — only files needed for the cause enter the PR; identify removable residue separately.
7. **Anti-patch** — verify root cause and remove superseded workaround when safe.
8. **Design fit** — for user-visible/render-ready changes, preserve source fidelity and consumer design constraints; mark `N/A` for data-only work.
9. **QA/consumer** — real RED when behavior changes, minimal GREEN, full QA, and real-bundle proof when consumer-visible.
10. **Governance/continuity** — fresh compare/CI/reviews/mergeability, expected-head merge, postmerge smoke and durable live-state checkpoint.

A material contradiction means stop and re-audit; do not compensate by adding architecture.

## Required Knowledge QA

Before declaring a Knowledge change ready:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
```

For consumer-visible bundle/FigureSpec behavior, use the permanent exact-SHA consumer proof in `CarpiNova-PC` with the real generated bundle. Synthetic fixtures alone are insufficient, but page-specific consumer workflows should not be duplicated when Knowledge tests already own the semantics.

## Documentation and continuity without noise

Use each surface for one purpose:

- `AGENTS.md`: durable laws and operating rules.
- `README.md`: stable architecture, commands and recovery path.
- GitHub issue/PR: current work, exact SHAs, decisions, checkpoints and blockers.
- Git history: historical execution detail.
- `docs/releases/`: durable release evidence.
- policy docs: only rules that genuinely need a dedicated long-lived document.

Do **not** add routine gate/checkpoint files, copied chat handoffs, duplicate specs/plans, local verification diaries or the same document to both repositories. A final release/audit artifact is allowed only when it has unique durable value.

If a chat ends, the next session must be able to continue from live GitHub without a private conversation transcript.

## Branch and temporary-artifact hygiene

- Keep only active work branches plus branches with demonstrated rollback/forensic value.
- After merge/closure, audit obsolete branches and delete only when their commits are safely represented by `main`/Git history.
- Temporary consumer-proof branches/workflows are exceptional; prefer the permanent reusable PC workflow.
- Never force `main`.
- Never leave a temporary branch with product delta after a proof.

## Merge discipline

Immediately before merge, fresh-read `main`, PR head, compare, exact-head CI, reviews, scope and mergeability. Use expected-head protection where supported.

After merge, verify the new exact `main` and the normal postmerge workflow/smoke. Do not repeat full forensic consumer proof unless the merged tree or consumer head materially differs from what was already proven.

## Stop conditions

Stop and classify instead of improvising when:

- `main` moved and the relevant delta is unknown;
- overlapping agent/Codex work is unknown;
- source semantics are ambiguous;
- a candidate is excluded from distribution;
- a test requires invented truth;
- source-faithful support requires a new schema/primitive/renderer contract without an explicit decision;
- PC would need duplicated canonical truth or a source-specific special case;
- an unrelated file appears in the delta;
- CI failure is unexplained;
- merge head changed;
- product and unrelated governance cleanup are mixed;
- a version bump or compatibility removal appears without an explicit decision.

Evidence controls execution. Complexity is never a substitute for certainty.

## L1 — KISS + Ponytail
Consultar `.agents/skills/kiss-ponytail/SKILL.md` en tareas de código. Aplicar primero NO CREAR → reutilizar el repositorio → stdlib/nativo → dependencia instalada → mínimo código nuevo legible. Comprobar consumidores directos/dinámicos, contratos y riesgos; nunca recortar seguridad, precisión, validaciones, fabricación, datos, accesibilidad o pruebas necesarias. Conservar instrucciones de carpintería, reglas L2–L6 y permisos de fabricación. Plugin global/hook Codex requiere instalación y confianza aparte.
