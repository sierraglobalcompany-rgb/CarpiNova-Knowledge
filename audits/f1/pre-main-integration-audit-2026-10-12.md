# CarpiNova Knowledge F1 — Pre-main Integration Audit

**Date:** 2026-10-12  
**Phase:** P2.5 — pre-main compare / integration audit  
**Result:** **PASS — NO INTEGRATION BLOCKER FOUND**  
**Scope:** Git/GitHub integration safety only. This audit does not replace the technical/editorial human review plan documented for Knowledge 1.0.

## 1. Canonical inputs

- Repository: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- `main`: `ac0a0440de11df9514d7ba59e9957dff833bd7b1`
- `feat/knowledge-f1`: `3123ba913e7337f0c8c675e73af1bd4de6781e99`
- F1 tree: `af28f1e508a03f7c1c4be6a496d7fb3d868639d1`
- Merge base: `5222275528ee2e90a655e40d37af3ce04de60fe4`
- Merge-base tree: `25e0c5fbaf083cd02cf38846879f793cdeab2bcf`
- Current `main` tree: `25e0c5fbaf083cd02cf38846879f793cdeab2bcf`

The current `main` tree is byte-for-byte the same Git tree as the merge base.

## 2. P2 closure evidence

P2 documentation was integrated through PR #20.

- F1 post-P2 SHA: `3123ba913e7337f0c8c675e73af1bd4de6781e99`
- Canonical CI run: `38275672599`
- `pytest`: PASS
- Ruff: PASS
- repository validator: PASS
- F0 pilot acceptance: PASS
- overall job conclusion: SUCCESS

P2 is therefore closed before this P2.5 audit is promoted.

## 3. `main` divergence audit

Live compare `main` → `feat/knowledge-f1`:

- status: `diverged`
- F1 ahead: `360` commits
- F1 behind: `2` commits
- merge base: `5222275528ee2e90a655e40d37af3ce04de60fe4`

The two commits unique to `main` were inspected individually:

1. `f368afd765345167255ba4a5af1d7b604fb9bbe2` — message `noop`
   - adds only `docs/.noop`
   - one added line: `noop`
2. `ac0a0440de11df9514d7ba59e9957dff833bd7b1` — `revert: restore main tree after accidental noop commit`
   - removes only `docs/.noop`

Direct compare from the merge base to current `main` reports:

- ahead by: `2`
- changed files: `[]`

This is independently confirmed by tree identity:

`main tree == merge-base tree == 25e0c5fbaf083cd02cf38846879f793cdeab2bcf`

**Conclusion:** the two commits behind F1 are history-only net-zero changes. `main` contains no functional content that needs to be preserved separately before the F1 integration.

## 4. F1 source / repository guardrails

The live F1 book manifest still identifies:

- `book_id`: `cpnc-2025`
- `pdf_page_count`: `295`
- source SHA-256: `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`

A recursive Git tree inspection of F1 at `3123ba913e7337f0c8c675e73af1bd4de6781e99` found no tracked path containing `.pdf` and no tracked `source-books/` path. The source PDF therefore remains outside Git as required.

The current F1 workflow runs Knowledge QA on:

- pushes to `main`;
- pushes matching `feat/knowledge-f1*`;
- pushes matching `knowledge/f1-*`;
- pull requests targeting `main`.

The final F1 → `main` PR will therefore receive its own pull-request QA, and the merged `main` state will receive post-merge QA.

## 5. Integration strategy

Use a normal pull request:

`feat/knowledge-f1` → `main`

Do **not**:

- rebase `main` merely to remove the noop/revert history;
- force-push either branch;
- bypass CI;
- squash or rewrite the historical `main` commits for cosmetic reasons;
- reinterpret unresolved source content during integration.

Because current `main` has the same tree as the merge base, no content-side competing change exists on `main`. GitHub PR mergeability remains the final platform-level conflict check.

## 6. Human gate

P2.5 does **not** authorize the merge to `main`.

Next operation:

1. open the final PR `feat/knowledge-f1` → `main`;
2. verify its mergeability and pull-request CI;
3. present the PR plus this audit to the human owner;
4. merge only after explicit human approval;
5. verify post-merge `main` CI;
6. only after the remaining Knowledge 1.0 review/release gates are satisfied, create release `1.0.0`.

The technical/editorial review plan remains versioned in `docs/releases/1.0.0-rc.1.md`. `UNRESOLVED` items remain visible and are not converted into facts by this integration audit.

## 7. Operational incident recorded during P2.5

Draft PR #21 was accidentally opened with placeholder metadata while attempting to create the P2.5 branch. It was immediately closed without merge. `main` was not modified. The incident does not alter the integration assessment.

## 8. Verdict

```text
P2:                              CLOSED
P2.5 main-vs-F1 compare:         PASS
main unique functional content:  NONE
main tree vs merge-base tree:    IDENTICAL
source identity:                 VERIFIED IN LIVE MANIFEST
source PDF tracked in F1:        NO
canonical F1 CI after P2:        SUCCESS
recommended integration:         NORMAL PR, NO REBASE/FORCE
F1 -> main authorization:        HUMAN GATE REQUIRED
```

**P2.5 result: PASS. Proceed to the final F1 → `main` PR and stop at the human approval gate before merge.**
