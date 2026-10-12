# F1 Checkpoint 014 — BATCH-024 recovered and GREEN

- Branch: `feat/knowledge-f1`
- Recovery commit: `96f5cddc5a1aba4e514c5d11c34f90d18de81d17`
- CI run: `38057301150`
- CI result: GREEN (`pytest`, Ruff, repository validator, F0 pilot acceptance).
- Last completed F1 batch: `BATCH-024`.
- Correct BATCH-024 ownership: PDF `105–109` / printed `83–87`.
- PDF `110–117` remain owned by `BATCH-000-PILOT`; BATCH-024 must not overwrite or duplicate them.
- Pages `110–112` were restored exactly from the last pre-BATCH-024 GREEN state (`7b70e9054ee922d93104e4e0e2aeb4c06b1e378c`).
- Canonical coverage after recovery: `117/295` complete; `178` pending; no duplicate batch assignments.
- Next genuinely pending physical PDF page: `118` (printed `96`).
- New user-requested extraction policy: all following F1 batches use **2 physical PDF pages per batch** unless a source-boundary exception is explicitly justified.
- Therefore next planned batch: `BATCH-025` = PDF `118–119` / printed `96–97`.
- Source PDF remains available through Project/Library as `libros_1751553390342_Carpintería para no Carpinteros Versión 2025.pdf`.
- Source-access note: Files currently reports `294` pages while repository manifest records `295` for the canonical source SHA. Do not silently change the manifest; reconcile this discrepancy separately while preserving repository source-of-truth and page mapping.
- Method unchanged: KISS; source fidelity first; canonical JSON drives generated Markdown; detailed FigureSpec for meaningful visuals; measurements remain source-traceable; technical recommendations are not silently promoted beyond their validation status.
