# Changelog

## 1.0.0-rc.1 — F1 release candidate (unreleased)

- Completed canonical structured coverage for all 295 physical pages of `cpnc-2025`.
- Preserved the canonical source fingerprint `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c` without committing the source PDF.
- Added the global F1 audit gate covering repository validity, source-gap status, meaningful visuals, QR provenance, security candidates, and full-book coverage.
- Classified historical source-gap reports without erasing their provenance.
- Reviewed current safety-term candidates and restored explicit protection-language meaning where it had been weakened in P0259–P0263.
- Preserved known source conflicts instead of choosing a winner by inference.
- Added deterministic full-book consumer bundle generation for `knowledge`, `figures`, and `lessons`, plus a manifest with hashes and record counts.
- Added `build-book-dist` as the reproducible full-book build command.
- Kept all current rules non-executable; the candidate is not fabrication authority.

`1.0.0-rc.1` is not a final release. Promotion to `1.0.0` still requires the documented technical/editorial human review, pre-main integration audit, explicit approval for F1 → `main`, green `main` CI, and release creation.

## 0.1.0 — F0 pilot

- Audited the complete 2025 source PDF at physical-page level.
- Mapped physical pages to printed pages.
- Added canonical schemas for source, page, content, figure, measurement, rule, concept, lesson and batch records.
- Extracted and visually verified printed pages 88–95 (physical 110–117).
- Added FigureSpec reconstruction metadata, candidate rules, MeasurementSpec records and the first reusable LessonSpec.
- Added deterministic consumer bundles for CarpiNova Designer and CarpiNova Cell.
- Added repository validation and F0 pilot acceptance reporting.

No rule is executable fabrication authority in 0.1.0; technical rules remain candidates pending later technical validation.
