# Changelog

## 1.0.0 — 2026-10-12

- Completed canonical structured coverage for all `295` physical pages of `cpnc-2025` and preserved the exact source fingerprint `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c` without committing the PDF.
- Finalized the full-book bundle identity as `knowledge_version=1.0.0` while keeping the F0/batch identity at `0.1.0`.
- Added explicit KISS distribution filtering through `books/cpnc-2025/distribution.json`: `43` confirmed non-technical pages remain in canonical provenance but are omitted from the consumer bundle, leaving `252` useful carpentry pages.
- Preserved source conflicts instead of inventing winners, including p64/p65 quantity differences, p67 `64 mm` vs “sistema 37 y 32”, duplicated step numbering p72/p73, p208/p211 lock-height `90 cm` vs `95 cm`, and unreadable dimensions on p121.
- Retained safe `UNRESOLVED` states where evidence is insufficient and kept all distributed RuleSpec records non-`EXECUTABLE`.
- Reused and preserved the completed F1 safety review, including the restored protection language on P0259–P0263.
- Kept deterministic full-book consumer bundle generation for `knowledge`, `figures`, `lessons` and the manifest with hashes and counts.
- Added source page count and exclusion count to the full-book manifest.
- Completed the targeted exact-source final review with `NEEDS_CHANGE=0` and recorded explicit owner attestation for `PASS_FOR_1.0.0`.

## 1.0.0-rc.1 — F1 release candidate (superseded)

- Completed full canonical structured coverage and the global F1 audit.
- Added deterministic full-book bundle generation.
- Preserved known conflicts and safety evidence while awaiting the final exact-source review and useful-knowledge scope decision.

Superseded by `1.0.0`.

## 0.1.0 — F0 pilot

- Audited the complete 2025 source PDF at physical-page level.
- Mapped physical pages to printed pages.
- Added canonical schemas for source, page, content, figure, measurement, rule, concept, lesson and batch records.
- Extracted and visually verified printed pages 88–95 (physical 110–117).
- Added FigureSpec reconstruction metadata, candidate rules, MeasurementSpec records and the first reusable LessonSpec.
- Added deterministic consumer bundles for CarpiNova Designer and CarpiNova Cell.
- Added repository validation and F0 pilot acceptance reporting.

No rule is executable fabrication authority in 0.1.0; technical rules remain candidates pending later technical validation.
