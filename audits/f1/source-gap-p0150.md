# Source gap — PDF P0150 / printed 128

- Book: `cpnc-2025` / edición 2025.
- Canonical mapping: PDF `150` -> printed `128` (`verified` in `page-map.json`).
- Status: **PENDING — SOURCE_IMAGE_UNAVAILABLE**.
- The Library page reader can parse the backing PDF but exposes only the book header and printed page number for PDF 150; the rendered page image is unavailable.
- Raw-byte materialization of the Library PDF is not authorized in the current project runtime, and no identical local PDF copy is mounted under `/mnt/data`.
- Printed page 129 begins with `que vayas a realizar:`, proving that page 128 contains preceding instructional text and must not be treated as blank.
- Public web results found an older edition, but it is intentionally rejected because F1 policy forbids mixing editions.
- Therefore P0150 is deliberately left without canonical page files and remains pending in coverage.
- BATCH-041 uses an explicit source-boundary exception and covers PDF `151–152` only.
- Recovery rule: complete P0150 only when the exact 2025 source page can be rendered/read; do not reconstruct its text from another edition or from inference.
