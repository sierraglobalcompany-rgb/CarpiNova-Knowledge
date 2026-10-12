# CarpiNova Knowledge — Checkpoint pre-BATCH-108

Date: 2026-10-12
Repository: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
Checkpoint branch: `checkpoint/batch108-preaudit-20261012`
Canonical F1 branch: `feat/knowledge-f1`

## Frozen canonical state

- BATCH-107 was merged through PR #4 into `feat/knowledge-f1`.
- Merge commit / canonical F1 HEAD at checkpoint: `f66f73fa301e4ff1cd175dcdfb3bd4dc7fcff16c`.
- PR #4 is closed and merged.
- Post-merge GitHub Actions run: `38194183457`.
- Post-merge CI result: **SUCCESS**.
- CI steps passed: tests, Ruff, repository validation, F0 pilot acceptance.
- Coverage contract on the merged tree remains `278/295`, pending `17`, duplicates `[]`.
- `main` was not touched.

## BATCH-108 status

**NOT STARTED.**

No canonical files for P0161 or P0162 have been created in this continuation session.
No implementation branch for BATCH-108 has been created yet.

Expected next microbatch from V7/V7A:

```yaml
batch: BATCH-108
pages: [161, 162]
```

Reason: these are the next real pending pages and P0160 has explicit source continuity into P0161.

## Pre-audit completed before stopping

### Mapping

`page-map.json` confirms:

- P0161 -> PDF 161 -> printed page 139 -> `verified`
- P0162 -> PDF 162 -> printed page 140 -> `verified`

### Canonical existence / historical source-gap state

- `books/cpnc-2025/pages/p0161/` is absent on canonical F1.
- `books/cpnc-2025/pages/p0162/` is absent on canonical F1.
- Historical provenance files remain:
  - `audits/f1/source-gap-p0161.md`
  - `audits/f1/source-gap-p0162.md`
- Those historical files record the old state `SOURCE_IMAGE_UNAVAILABLE`; preserve them as provenance even after recovery. Do not delete them just because the pages become canonical.

### Continuity evidence already recovered from the exact 2025 source audit in this conversation

P0160 ends with:

`... indicando las posiciones exactas entre parales (postes verticales) para`

P0161 begins with:

`facilitar la construcción de muros.`

Therefore P0160 -> P0161 is a real continuation and must be modeled without inventing text on P0160.

A second boundary was also identified:

P0162 ends with:

`... En estos casos, se toma la medida menor`

P0163 begins canonically with:

`del vano y se instalan molduras o espumas expansivas para cubrir las luces sobrantes.`

Therefore P0162 -> P0163 is also a real continuation.

### Important source-access caveat

The current conversation file reader still fails to render page images 160-162 from the attached ~339 MB PDF, and raw materialization exceeds the 100 MB runtime limit. Do **not** replace exact-source evidence with another edition, web text, adjacent-page inference, or invented reconstruction.

If a fresh full-page extraction of P0161/P0162 is required on resume, use only the exact attached 2025 source through an available exact-source rendering path. `UNRESOLVED > INVENTED` remains binding.

### P0163 dependency to audit when P0162 is recovered

P0163 is already canonical and its first `source_transcription` is the continuation fragment beginning `del vano...`.

Its current normalized/learning text still describes the preceding context as unavailable. Once P0162 is recovered, audit whether those **derived** descriptions need a minimal synchronization update. Do not rewrite P0163 source transcription.

P0163 already contains a meaningful visual inventory plus `FIG-CPNC-2025-P0163-001` for the escuadra/nivel reference illustration. Do not duplicate that figure in BATCH-108.

## Resume exactly here

1. Read back `feat/knowledge-f1` before any mutation.
2. Expected canonical HEAD at this checkpoint: `f66f73fa301e4ff1cd175dcdfb3bd4dc7fcff16c`.
3. If HEAD differs, STOP and audit drift; do not force.
4. Confirm post-merge CI `38194183457` remains SUCCESS.
5. Create a fresh isolated BATCH-108 implementation branch from the current canonical F1 HEAD.
6. Re-audit exact-source P0161/P0162 content, visuals, measurements, rules, QR, safety, and both continuity boundaries.
7. Follow TDD: RED first, then minimal canonical implementation, then GREEN.
8. Keep `content.json` canonical; regenerate/synchronize `source.md`, `normalized.md`, and `learning.md` from canonical meaning.
9. Add FigureSpec only for meaningful visuals actually present on P0161/P0162; no speculative figures.
10. Preserve historical `source-gap-p0161.md` and `source-gap-p0162.md` as provenance.
11. After implementation, expected coverage if both pages are validly recovered: `280/295`, pending `15`, duplicates `[]`.
12. Run full tests, Ruff, repository validator, coverage audit, and F0 acceptance.
13. Audit branch diff/tree before any promotion.
14. Do not merge to `feat/knowledge-f1` without explicit Andrés approval.
15. Do not touch `main`.

## Guardrails

- Exact 2025 source beats all secondary sources.
- Preserve source transcription exactly, including page-boundary fragments.
- Never complete continuity by grammar or intuition.
- `UNRESOLVED > INVENTED`.
- One responsibility per microbatch.
- No schema change for an isolated edge case.
- No force push / force ref update.
- No bypass of CI.
- No branch cleanup during extraction.
- No merge to F1 or main without explicit approval.

## Stop point

Checkpoint created intentionally before starting BATCH-108 implementation. Resume from the read-back/drift check above; do not redo BATCH-107.