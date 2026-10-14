# Changelog

## 1.1.0 — 2026-10-14

- Prepared the full-book Knowledge `1.1.0` release candidate without changing canonical source identity, page counts, exclusions, or source SHA-256.
- Added the opt-in `normalized-2d-v1` render contract only for `FIG-CPNC-2025-P0113-001`; the remaining FigureSpec records stay legacy-compatible and require no migration.
- Preserved KISS scope: one deterministic native 2D figure contract, no 3D/WebGL engine, renderer registry, plugin architecture, new runtime dependency, or new permanent workflow.
- Kept the book bundle deterministic at `976` content records, `643` measurements, `250` rules, `138` figures, `1` lesson and `0` taxonomy records.
- Verified CarpiNova-PC dual-version compatibility with real Knowledge `1.0.0` and candidate `1.1.0` bundles; PC accepts both versions and renders the P0113 support figure once when the new contract is present.
- Preserved safe `UNRESOLVED` and source-conflict handling; `1.1.0` does not elevate inferred or external facts into the canonical book.

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
