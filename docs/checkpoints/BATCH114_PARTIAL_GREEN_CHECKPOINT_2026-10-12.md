# CarpiNova — Checkpoint BATCH-114 partial GREEN — 2026-10-12

## Canonical base

- Repository: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Canonical F1 branch: `feat/knowledge-f1`
- Canonical F1 base used by B114: `e02f4bc4671feb0133130fe9945dd2c687efec2d`
- BATCH-113 was already promoted before starting B114.

## BATCH-114 scope

- Target pages: PDF `P0189` / printed `167` and PDF `P0190` / printed `168`.
- Previous state for both pages: historical `SOURCE_IMAGE_UNAVAILABLE` gap records.
- Exact 2025 source page renders are now available and were visually inspected; recovery must continue only from that exact source.
- Do not infer from adjacent pages or another edition.

## TDD RED evidence

- RED branch: `feat/knowledge-f1-b114-red`
- RED commit: `870a2643d4d21cc0c52ac305800e6b2708c18c08`
- Workflow run: `38202688325`
- Result: expected FAILURE in tests.
- Test summary: `2 failed, 178 passed`.
- Expected failures:
  1. `batch-114` does not exist yet.
  2. Coverage is still `287`, while the B114 contract expects `289` after recovering both pages.
- RED contract currently encodes candidate totals for B114: 2 pages, 9 content records, 1 figure, 9 measurements and 8 rules. These totals still require full implementation and GREEN verification against the exact source.

## Implementation branch state

- Branch: `feat/knowledge-f1-b114`
- Frozen HEAD: `b084cf9528d52526e5449461145b8063233d7321`
- Current tree is PARTIAL GREEN only; no claim of GREEN is valid yet.

### Files already created

1. `books/cpnc-2025/batches/batch-114.json`
2. `books/cpnc-2025/pages/p0189/page.json`
3. `books/cpnc-2025/pages/p0189/content.json`

`p0189/content.json` currently contains 6 source-derived records covering: geometric verification, importance of recording irregularities, kitchen connections, kitchen height references, closet measurements/example, and the beginning of door measurements.

## Still missing before any GREEN claim

- Complete P0189 measurements/rules/derived Markdown/visual inventory/FigureSpec as warranted by the source.
- Create the complete P0190 canonical page folder and all derived artifacts.
- Resolve continuity P0189 -> P0190 exactly from source.
- Update historical gap audits for P0189/P0190 to `RESOLVED` while preserving provenance.
- Update `tests/test_report_coverage.py` only when canonical files justify `289/295`, pending `[194,195,202,207,213,223]`, duplicates `[]`.
- Run full candidate QA: pytest, Ruff, repository validator, F0 pilot acceptance.
- Audit full diff against canonical F1 before opening any PR.
- No PR exists for B114 yet.
- No merge has occurred for B114.

## Resume instruction

Resume on `feat/knowledge-f1-b114` from `b084cf9528d52526e5449461145b8063233d7321`. Do not redo the RED phase. Continue with the remaining exact-source artifacts for P0189/P0190, then run GREEN verification. Stop again at the promotion/merge gate unless explicit human authorization is given.
