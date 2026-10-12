# CarpiNova Knowledge — Checkpoint BATCH-108 promoted

Date: 2026-10-12

## Canonical state

- Repository: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Canonical F1 branch: `feat/knowledge-f1`
- Canonical F1 HEAD: `2460fcea08d96bb30063d4a2495e3ccd7a1c48bd`
- `main` remains untouched at `5222275528ee2e90a655e40d37af3ce04de60fe4`.
- PR #5 was merged into `feat/knowledge-f1`.
- Merge commit: `2460fcea08d96bb30063d4a2495e3ccd7a1c48bd`.

## BATCH-108

BATCH-108 is PROMOTED to canonical F1.

Recovered exact-source 2025 PDF pages:
- P0161 / printed 139
- P0162 / printed 140

Confirmed source continuities:
- P0160 -> P0161: `... para` + `facilitar la construcción de muros.`
- P0162 -> P0163: `... se toma la medida menor` + `del vano y se instalan molduras...`

The batch includes canonical page artifacts, generated Markdown derivatives, technical measurements/rules, visual inventory, and a deterministic FigureSpec for the meaningful dual-scale ruler reference on P0161.

## Verification

Candidate GREEN CI before merge:
- run `38195069956`
- tests: `168 passed`
- Ruff: PASS
- repository validator: `valid=true`, `error_count=0`
- F0 pilot acceptance: GO

Canonical post-merge CI:
- run `38195954003`
- status: COMPLETED
- conclusion: SUCCESS
- tests: PASS
- Ruff: PASS
- repository validator: PASS
- F0 pilot acceptance: PASS

## Coverage frozen at checkpoint

- Total physical PDF pages: `295`
- Complete canonical pages: `280`
- Pending pages: `15`
- Duplicate batch pages: `[]`
- Pending PDF pages exactly:
  - `164`
  - `172`
  - `173`
  - `174`
  - `178`
  - `184`
  - `186`
  - `189`
  - `190`
  - `194`
  - `195`
  - `202`
  - `207`
  - `213`
  - `223`

## Known next boundary

P0164 remains explicitly pending under `audits/f1/source-gap-p0164.md` because it previously lacked renderable exact-source evidence. Do not infer its contents from adjacent pages or another edition.

P0172 and P0173 also remain explicit source gaps. Recovery must continue from the exact 2025 PDF only.

## Resume instruction

On resume:
1. Read back `feat/knowledge-f1` and confirm HEAD is still `2460fcea08d96bb30063d4a2495e3ccd7a1c48bd` or audit any legitimate later movement before changing anything.
2. Reconfirm coverage from canonical files before opening a new recovery batch.
3. Start with the next pending-page/source-gap audit, beginning at P0164 unless a newer approved plan supersedes it.
4. Use exact 2025 source evidence only; no reconstruction by inference.
5. Preserve TDD/RED -> minimal implementation -> GREEN -> diff audit -> draft PR -> explicit approval before merge.
6. Do not touch `main`.

No new recovery batch has been started after BATCH-108 at this checkpoint.
