# Source gap — PDF P0164 / printed 142

- Book: `cpnc-2025` / edición 2025.
- Canonical mapping: PDF `164` -> printed `142` (`verified` in `page-map.json`).
- Status: **PENDING — SOURCE_IMAGE_UNAVAILABLE**.
- During the BATCH-046 source audit, PDF 163 and PDFs 165–166 render from the exact 2025 source, but PDF 164 exposes only the book header and printed page number `142`; its rendered page image is unavailable.
- Raw-byte materialization of the Library PDF is not authorized in the current project runtime, so the page cannot be rendered independently in the container.
- The readable content on surrounding pages is not sufficient evidence to infer the missing page.
- Therefore P0164 is deliberately left without canonical page files and remains pending in coverage.
- BATCH-046 uses an explicit source-boundary exception and covers PDF `163` only.
- Recovery rule: complete P0164 only when the exact 2025 source page can be rendered/read; do not reconstruct its text from another edition, adjacent pages, or inference.
