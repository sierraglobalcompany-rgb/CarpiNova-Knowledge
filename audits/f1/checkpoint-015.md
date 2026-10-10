# F1 Checkpoint 015 — BATCH-025 GREEN

- Branch: `feat/knowledge-f1`
- BATCH-025 commit: `cef8e9b816fb9733ee64f1e19144e48072160c2d`
- Active CI run: `38058136233`
- Active CI job: `114230697736`
- CI result: GREEN (`pytest`, Ruff, repository validator, F0 pilot acceptance).
- BATCH-025 scope: PDF `118–119` / printed `96–97`.
- BATCH-025 topics: telescopic-slide technical/commercial sheet and Omega/butterfly hinges.
- Canonical coverage after BATCH-025: `119/295` complete; `176` pending; no duplicate batch assignments.
- Extraction policy: continue with exactly **2 physical PDF pages per F1 batch** unless a source-boundary exception is explicitly justified.
- Next genuinely pending pages confirmed absent from the repository: PDF `120–121`; planned as `BATCH-026`.
- Source book remains `libros_1751553390342_Carpintería para no Carpinteros Versión 2025.pdf`.
- Page-count discrepancy clarified: Files/Library currently exposes `294` readable pages, while the canonical repository page-map intentionally includes `PAGE-CPNC-2025-P0295` as `pdf_page: 295`, `printed_page: null`, `mapping_status: not_printed`. Keep canonical repository total at `295`; do not silently rewrite the manifest to 294.
- Current source-access caveat for BATCH-026: Files successfully rendered pages 118–119 but returned no readable content for 120–121. Do not substitute the older textual edition because its page 98–99 content does not match the 2025 edition. Recover 120–121 from the 2025 source or canonical audit before extracting.
- Method unchanged: source fidelity first; canonical JSON drives generated Markdown; meaningful visuals receive detailed FigureSpec; source measurements remain traceable; technical recommendations stay `CANDIDATE` until separately validated.
