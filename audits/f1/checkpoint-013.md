# F1 Checkpoint 013 — BATCH-024 diagnosis recovered

- Branch: `feat/knowledge-f1`
- Branch head before this checkpoint: `b1d7426a1c3d16340d7076bee40806b90ad26f7d`
- Last fully CI-green batch remains: `BATCH-023`
- Active candidate: `BATCH-024`
- BATCH-024 source scope: PDF 105–112 / printed 83–90
- Do NOT advance to PDF 113 until BATCH-024 is GREEN.

## What was recovered

1. The first RED boundary is exactly commit `1ff1e32c563c509744a3421ca23c17d591d34a25` (BATCH-024). Its parent `7b70e9054ee922d93104e4e0e2aeb4c06b1e378c` was fully CI GREEN.
2. BATCH-024 introduced FigureSpec contract violations on P0105/P0110/P0112.
3. Minimal fix commit published on active branch: `b1d7426a1c3d16340d7076bee40806b90ad26f7d` (`fix: restore batch-024 FigureSpec contracts`).
4. That fix restored required `geometry.precision` on FigureSpec entities and changed P0110 `figure.measurements` back to measurement-id references instead of embedding a measurement object.
5. CI run for that fix: `38055918981`, job `114224342034`. Result: still RED in pytest, but the previous dict/reference crash was removed and the validator could be diagnosed cleanly.

## Exact validator diagnosis

A temporary diagnostic branch was created only to run repository validation before pytest:
- Branch: `feat/knowledge-f1-diagnostic`
- Diagnostic commit: `48422d37d4b9f6a5eb54e55c43801797440f9b91`
- Diagnostic CI run: `38056265644`
- Diagnostic job: `114225323068`

The validator reports exactly `20` errors:
- `17` x `stale_generated_markdown`
- `3` x invalid `content_type`

Invalid content types:
- `books/cpnc-2025/pages/p0107/content.json` → `CONTENT-CPNC-2025-P0107-002` uses `standard_measurement` (not allowed by current content schema).
- `books/cpnc-2025/pages/p0111/content.json` → `CONTENT-CPNC-2025-P0111-002` uses `standard_measurement` (not allowed).
- `books/cpnc-2025/pages/p0112/content.json` → `CONTENT-CPNC-2025-P0112-001` uses `technical_diagram` (not allowed as content_type; technical_diagram is a FigureSpec type).

Stale generated Markdown files reported by validator:
- P0105: `source.md`
- P0107: `source.md`, `normalized.md`, `learning.md`
- P0108: `source.md`, `normalized.md`, `learning.md`
- P0109: `normalized.md`, `learning.md`
- P0110: `source.md`, `normalized.md`, `learning.md`
- P0111: `source.md`, `normalized.md`, `learning.md`
- P0112: `normalized.md`, `learning.md`

These Markdown files must be regenerated from canonical `content.json` using the repository renderer; do not hand-edit their prose independently.

## Coverage/accounting issue recovered

The prior checkpoint claim `120/295` was incorrect because BATCH-024 overlaps pages already represented by the F0 pilot.

Evidence:
- Before BATCH-024, the last GREEN state already had `112/295` complete pages.
- `BATCH-000-PILOT` is defined by printed pages 88–95, which resolve into physical PDF pages overlapping BATCH-024.
- Current pytest reports only `117/295` complete after adding BATCH-024, which is consistent with only PDF 105–109 being genuinely new physical pages.
- Current duplicate assignments reported include PDF 111 and 112 (and test injection shows 110 as expected when deliberately duplicated).

Therefore do NOT force coverage to 120. The correct next step is to reconcile BATCH-024 assignment with the existing F0 pilot and update the coverage expectation to the real canonical total after duplicates are removed.

## Current pytest symptoms after FigureSpec fix

CI run `38055918981`:
- `31 failed, 52 passed`
- Most batch/pilot tests fail transitively because repository validation returns 20 errors.
- Coverage assertion currently shows `117 != 120`.
- Duplicate-batch test sees `[110, 111, 112]` instead of only injected `[110]`, proving 111–112 are already duplicated by repository state.

## Next execution sequence

1. Fix the 3 invalid `content_type` values using existing allowed schema values without changing source meaning.
2. Regenerate the 17 stale Markdown outputs from canonical content.
3. Reconcile BATCH-024 vs BATCH-000-PILOT assignments so no physical PDF page is owned by two batches.
4. Correct `tests/test_report_coverage.py` to the canonical physical coverage instead of the erroneous 120 target.
5. Run full CI: pytest → Ruff → repository validator → F0 pilot acceptance.
6. Only after full GREEN, mark BATCH-024 accepted/completed and resume from physical PDF 113.
7. Diagnostic branch is temporary and should be deleted after the active branch is GREEN.

## Policies unchanged

- KISS.
- Source fidelity first.
- `content.json` is canonical; generated Markdown must be rendered from it.
- Normalized and learning layers stay separate from source transcription.
- Measurements remain source-traceable and visually verified where applicable.
- Technical recommendations remain `CANDIDATE` until later validation.
- Exact technical diagrams use deterministic FigureSpec where required.
