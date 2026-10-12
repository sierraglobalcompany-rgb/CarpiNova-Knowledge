# Source gap — PDF P0160 / printed 138

- Book: `cpnc-2025` / edición 2025.
- Canonical mapping: PDF `160` -> printed `138` (`verified` in `page-map.json`).
- Status: **PENDING — SOURCE_IMAGE_UNAVAILABLE**.
- The exact 2025 Library source was re-read after BATCH-044: PDF 159 rendered once and is usable, but PDF 160 exposes only the book header and printed page number `138`; its rendered page image is unavailable.
- Raw-byte materialization of the Library PDF is not authorized in the current project runtime, so the page cannot be rendered independently in the container.
- PDF 159 continues the circular-saw chapter, but that continuity is not enough to reconstruct or infer the missing content of PDF 160.
- Therefore P0160 is deliberately left without canonical page files and remains pending in coverage.
- BATCH-045 uses an explicit source-boundary exception and covers PDF `159` only.
- Recovery rule: complete P0160 only when the exact 2025 source page can be rendered/read; do not reconstruct its text from another edition, adjacent pages, or inference.
