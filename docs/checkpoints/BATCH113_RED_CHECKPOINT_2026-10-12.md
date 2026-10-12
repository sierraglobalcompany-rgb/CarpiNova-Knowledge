# BATCH-113 RED checkpoint — 2026-10-12

## Canonical F1 state

- Repository: `sierraglobalcompany-rgb/CarpiNova-Knowledge`.
- Canonical F1 branch: `feat/knowledge-f1`.
- BATCH-112 was promoted through PR #9.
- Canonical F1 HEAD after that promotion: `bb18f24d0852a918b265dacf8f1e03ec13581197`.
- Canonical post-merge CI: run `38200911730` — `SUCCESS`.
- Canonical coverage after BATCH-112: `286/295` complete, `9` pending, duplicate batch pages `[]`.
- Expected pending PDF pages after BATCH-112: `[186, 189, 190, 194, 195, 202, 207, 213, 223]`.
- `main` was not modified by this work.

## BATCH-113 current state

- Target page: `P0186` / printed page `164`.
- Historical provenance remains in `audits/f1/source-gap-p0186.md`; do not delete it.
- The current file reader can extract only the repeated header plus printed page number from PDF page 186, and did not provide the page image. This is not proof that the page is blank.
- Adjacent canonical pages P0185 and P0187 are Cortecloud content, but adjacency must not be used to invent or reconstruct P0186.
- RED branch: `feat/knowledge-f1-b113-red`.
- RED commit: `291f622ee01f60b662fe6a4b6446996c91909873`.
- RED test file added: `tests/test_batch_113.py`.
- RED CI run: `38201176911`.
- At checkpoint creation that RED run was still `in_progress`, specifically inside `Run tests`.
- No BATCH-113 GREEN implementation exists yet.
- No BATCH-113 manifest, canonical `p0186` directory, PR, or merge has been created.

## Resume point

1. Read back `feat/knowledge-f1` and confirm the expected canonical HEAD `bb18f24d0852a918b265dacf8f1e03ec13581197`; if it drifted, stop and audit before continuing.
2. Check final result and logs for RED CI `38201176911`; RED must fail for the intended missing BATCH-113 / coverage assertions, not for unrelated infrastructure or regression causes.
3. Re-audit exact 2025 source page P0186. Do not classify it as blank from parser absence. Require an actual exact-source render/read sufficient to recover the page faithfully.
4. If exact source cannot be inspected sufficiently, keep P0186 unresolved and do not invent content.
5. If exact source becomes available, create a fresh GREEN implementation branch from canonical F1 and implement the minimum exact-source recovery required by the RED tests.
6. Preserve source / normalized / learning separation and keep `content.json` canonical.
7. Meaningful visuals require exact visual inspection before `VISUALLY_VERIFIED` or FigureSpec creation.
8. Expected coverage only if P0186 is validly recovered: `287/295`, `8` pending, duplicates `[]`; verify from the actual report before claiming it.
9. Run full tests, Ruff, repository validator and F0 pilot acceptance; audit diff/tree before opening a draft PR.
10. Do not merge into `feat/knowledge-f1` without explicit human approval. Do not touch `main`.

## Guardrails

- Exact 2025 PDF is the source authority.
- `UNRESOLVED > INVENTED`.
- No inference from adjacent pages.
- No destructive cleanup, force push, schema bypass or branch cleanup.
- Keep historical source-gap files as provenance even after later resolution.
