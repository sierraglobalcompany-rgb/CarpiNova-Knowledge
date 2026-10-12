# F1 Checkpoint 012

- Branch: `feat/knowledge-f1`
- Base commit before checkpoint: `1ff1e32c563c509744a3421ca23c17d591d34a25`
- Last CI-green completed batch: `BATCH-023`
- Published candidate batch: `BATCH-024` = PDF 105–112 / impresas 83–90
- Intended coverage after BATCH-024: `120/295`
- Intended pending after BATCH-024: `175`
- CI status: RED on commit `1ff1e32c563c509744a3421ca23c17d591d34a25`; failure occurred in Tests. Exact failure cause is still pending diagnosis.
- Completed/published scope in BATCH-024: PASO 2 — HERRAJES introduction, blank p106, system 37/32, assembly hardware, INDUMA editorial advertisement, adhesives/corner hardware, cup hinges, and hinge overlay diagram.
- Important state: do NOT advance to PDF page 113 until BATCH-024 CI is diagnosed and GREEN. If the data is valid, fix only the test/validation cause; if validation exposes a real data issue, correct only that issue.
- Resume action: inspect CI logs for workflow run `38021215439`, job `114122406430`, identify exact failing assertion/schema, apply minimal correction, rerun full CI, then confirm BATCH-024 as completed.
- Next physical PDF page after GREEN: `113`.
- Next section: continuation of `PASO 2 — HERRAJES` (installation/selection details following hinge types).
- Source/data policy unchanged: KISS; source fidelity first; normalized and learning layers separate; measurements are `VISUALLY_VERIFIED`; technical recommendations remain `CANDIDATE` until later validation; deterministic FigureSpec for exact technical diagrams.
- Preserved unresolved earlier source items remain unchanged from Checkpoint 011: p83 cm vs p84 m board-format units; p88 vs p89 alistonado thickness lists; p94 beam height values without printed unit; p95 `3-2.5 m`; p96 `arnillas de cama`; p99 ambiguous `8×4 / 8×4 / 8×2,5c` labels.
