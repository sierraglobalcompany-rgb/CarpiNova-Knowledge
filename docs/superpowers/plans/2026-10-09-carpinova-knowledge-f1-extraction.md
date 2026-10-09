# CarpiNova Knowledge F1 Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extraer y clasificar sistemáticamente el 100 % del libro `cpnc-2025`, preservando trazabilidad, figuras, medidas, reglas candidatas, texto pedagógico y conflictos, hasta producir una `Knowledge 1.0` reproducible y auditable.

**Architecture:** F1 extiende el pipeline validado en F0 sin reemplazarlo. La extracción se ejecuta en lotes adaptativos de 3–8 páginas (objetivo 5–6), agrupados en ondas de aproximadamente 30 páginas; cada lote debe pasar QA antes de avanzar y cada onda termina con consolidación, revisión de conflictos y reporte de cobertura. El PDF fuente continúa fuera de Git y los datos estructurados siguen siendo la fuente canónica.

**Tech Stack:** Python 3.12; uv; PyMuPDF 1.26.x; JSON Schema Draft 2020-12; jsonschema 4.x; pytest 8.x; Ruff; JSON canónico; Markdown generado para revisión; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-09-carpinova-knowledge-f0-f1-design.md`

## Global Constraints

- Repositorio canónico: `sierraglobalcompany-rgb/CarpiNova-Knowledge`, privado.
- No subir el PDF fuente ni copias masivas de imágenes de terceros.
- `pdf_page` es 1-based y es la identidad estable; `printed_page` puede ser `null`.
- Mantener separadas `source_transcription`, `normalized_text` y `learning_text`.
- `content.json` sigue siendo canónico; los Markdown son vistas generadas.
- Toda procedencia usa localización de página y, cuando aplique, región normalizada `[0,1]`.
- Ningún número técnico pasa a `VALIDATED` por OCR/extracción automática.
- Todo dibujo relevante tiene `FigureSpec` o una razón documentada para no tenerlo.
- Ninguna regla F1 se vuelve autoridad ejecutable de fabricación por el mero hecho de ser extraída.
- El enriquecimiento externo debe permanecer separado y citado explícitamente.
- Los conflictos nunca se resuelven silenciosamente sobrescribiendo una fuente.
- Tamaño de lote: mínimo 3, máximo 8, objetivo 5–6 páginas; se permite reducir a 3–4 si las páginas son visualmente densas.
- Checkpoint: cada ~5 lotes o ~30 páginas.
- F1 busca cobertura completa de las 295 páginas físicas.
- Las páginas físicas 110–117 ya pertenecen al piloto F0 aceptado y se consideran completas; no se reextraen salvo corrección explícita.
- Cada onda de extracción debe vivir en una rama/PR separada después de que la infraestructura F1 sea integrada en `main`.

## Review Focus

1. **Página omitida o duplicada entre lotes.** Task 3 debe probar que las 295 páginas aparecen exactamente una vez entre páginas ya completadas y batches F1.
2. **Falso 100 % de cobertura.** Task 4 debe distinguir `EXTRACTED`, `NOT_RELEVANT`, `BLOCKED`, `UNPROCESSED` y piloto ya completo; una página relevante bloqueada impide `complete=true`.
3. **Contradicción sobrescrita durante consolidación.** Task 6 debe conservar todas las fuentes y generar `ConflictSpec` sin elegir una versión automáticamente.
4. **Figura perdida porque el texto extraído parece suficiente.** Task 5 debe fallar si el inventario visual declara una figura significativa sin `FigureSpec` ni exclusión documentada.
5. **`learning_text` introduce una regla no presente en la fuente.** Task 5 y el validador deben exigir derivación explícita de `content_id` o `external_enrichment` citado.

## Execution Topology

F1 no se implementa como un único PR gigante.

1. **F1 Infrastructure PR** — Tasks 1–8.
2. **Wave PRs** — Tasks 9–18, una rama/PR por onda.
3. **F1 Finalization PR** — Task 19.

Nombre recomendado de ramas:

- `feat/knowledge-f1-infra`
- `knowledge/f1-wave-01` ... `knowledge/f1-wave-10`
- `release/knowledge-1.0`

La rama actual `feat/knowledge-f1` contiene únicamente este plan hasta su aprobación.

## Standard Batch Completion Contract

Todo batch de extracción de Tasks 9–18 cumple, en este orden:

1. Confirmar su rango desde `books/cpnc-2025/f1-plan.json`.
2. Inspeccionar visualmente todas sus páginas antes de reescribir texto.
3. Completar `page.json`, `content.json`, `visual-inventory.json`, `measurements.json`, `rules.json` y `figures/*.json` cuando aplique.
4. Mantener incertidumbres como incertidumbres; no inferir precisión ausente.
5. Generar `source.md`, `normalized.md` y `learning.md` desde JSON canónico.
6. Ejecutar `validate`.
7. Ejecutar `report-batch`; resultado requerido: `GO`.
8. Actualizar `coverage.json`.
9. Commit por batch con mensaje `knowledge: extract <batch-id>`.

Al terminar una onda:

1. Ejecutar validación global.
2. Ejecutar reporte de cobertura.
3. Ejecutar consolidación temática no destructiva.
4. Registrar conflictos nuevos.
5. Generar reporte `audits/f1/<wave-id>.md`.
6. Construir release/bundle parcial reproducible.
7. Abrir PR de la onda y no mezclar si el QA no está verde.

---

### Task 1: Harden CI for F1 and main

**Files:**
- Modify: `.github/workflows/knowledge-qa.yml`
- Modify: `tests/test_cli.py`
- Modify: `src/carpinova_knowledge/cli.py`

**Interfaces:**
- Consumes: F0 CLI and validation commands.
- Produces: CI that runs on pushes to `main`, `feat/knowledge-f1-infra`, `knowledge/f1-wave-*`, `release/knowledge-1.0`, and on PRs to `main`; CLI placeholders are not added until their owning tasks.

- [ ] **Step 1: Write failing workflow-policy test**

Add a test that loads `.github/workflows/knowledge-qa.yml` and asserts `main` is included in the `push` branches and that PRs to `main` remain covered.

- [ ] **Step 2: Run RED**

Run: `uv run pytest tests/test_cli.py -v`

Expected: FAIL because `push.branches` currently contains only `feat/knowledge-f0`.

- [ ] **Step 3: Update CI triggers only**

Do not change the QA steps yet. Preserve Python 3.12, pytest, Ruff, repository validation and F0 pilot regression.

- [ ] **Step 4: Run GREEN**

Run: `uv run pytest tests/test_cli.py -v && uv run ruff check .`

Expected: PASS.

- [ ] **Step 5: Commit**

Commit: `ci: extend knowledge QA for F1 and main`.

---

### Task 2: Add F1 schemas for conflicts, coverage and waves

**Files:**
- Create: `schemas/conflict.schema.json`
- Create: `schemas/coverage.schema.json`
- Create: `schemas/wave.schema.json`
- Modify: `src/carpinova_knowledge/schema_loader.py`
- Modify: `tests/test_schemas.py`
- Create: `tests/fixtures/schemas/valid/conflict.json`
- Create: `tests/fixtures/schemas/valid/coverage.json`
- Create: `tests/fixtures/schemas/valid/wave.json`

**Interfaces:**
- Consumes: existing SourceSpec/PageSpec conventions.
- Produces: schemas for `ConflictSpec`, global page coverage and F1 wave metadata.

- [ ] **Step 1: Write valid-fixture and negative tests**

Tests must reject: conflict with fewer than two source claims; conflict marked resolved without resolution provenance; coverage record outside `pdf_page` 1–295; unknown coverage state; wave with overlapping physical ranges; wave omitting its declared batch IDs.

- [ ] **Step 2: Run RED**

Run: `uv run pytest tests/test_schemas.py -v`

Expected: FAIL because the F1 schemas do not exist.

- [ ] **Step 3: Implement schemas**

Coverage states: `UNPROCESSED`, `CLASSIFIED`, `EXTRACTED`, `NOT_RELEVANT`, `BLOCKED`, `PILOT_COMPLETE`.

Conflict states: `OPEN`, `REVIEWED`, `RESOLVED`, `DEFERRED`.

- [ ] **Step 4: Run GREEN**

Run: `uv run pytest tests/test_schemas.py -v && uv run ruff check .`

- [ ] **Step 5: Commit**

Commit: `feat: define F1 coverage and conflict schemas`.

---

### Task 3: Build the deterministic adaptive batch planner

**Files:**
- Create: `src/carpinova_knowledge/f1_planner.py`
- Create: `tests/test_f1_planner.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Modify: `tests/test_cli.py`
- Runtime output: `books/cpnc-2025/f1-plan.json`

**Interfaces:**
- Consumes: `raw-page-audit.json`, `page-map.json`, `index.json`, completed page set `{110..117}`.
- Produces: `plan_f1_batches(audit: dict, page_map: dict, index: dict, completed_pages: set[int]) -> dict`; CLI `plan-f1`.

- [ ] **Step 1: Write planner coverage tests**

Assert: physical pages 1–295 appear exactly once across planned batches plus completed pilot pages; 110–117 are not scheduled; batch size is 3–8; output is deterministic; ranges remain ascending.

- [ ] **Step 2: Write adaptive-complexity tests**

Synthetic audit must produce smaller batches when image/drawing density is high and larger batches for low-density text pages, without using OCR-derived semantics.

- [ ] **Step 3: Run RED**

Run: `uv run pytest tests/test_f1_planner.py tests/test_cli.py -v`

- [ ] **Step 4: Implement planner**

Use objective audit fields (`text_length`, image count, drawing count, block count) plus structural section boundaries. Prefer target 5–6 pages; never exceed 8 or go below 3 except a final remainder merged into its preceding batch.

Hard checkpoint waves:

| Wave | Physical pages | Notes |
|---|---:|---|
| W01 | 1–30 | front matter + printed 1–8 |
| W02 | 31–59 | printed 9–37 |
| W03 | 60–81 | printed 38–59 |
| W04 | 82–109 | printed 60–87 |
| Pilot F0 | 110–117 | already accepted, do not schedule |
| W05 | 118–145 | printed 96–123 |
| W06 | 146–172 | printed 124–150 |
| W07 | 173–202 | printed 151–180 |
| W08 | 203–232 | printed 181–210 |
| W09 | 233–262 | printed 211–240 |
| W10 | 263–295 | printed 241–272 + final unnumbered page if applicable |

- [ ] **Step 5: Run GREEN and generate real plan**

Run planner twice and compare hashes. Output must be byte-identical.

- [ ] **Step 6: Commit**

Commit: `feat: plan adaptive F1 extraction batches`.

---

### Task 4: Add the canonical F1 coverage ledger and report

**Files:**
- Create: `src/carpinova_knowledge/coverage.py`
- Create: `tests/test_coverage.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Modify: `tests/test_cli.py`
- Runtime output: `books/cpnc-2025/coverage.json`
- Runtime output: `audits/f1/coverage.md`

**Interfaces:**
- Consumes: F1 plan, page folders, pilot batch and validator results.
- Produces: `build_coverage(root: Path) -> dict`, `render_coverage_report(report: dict) -> str`; CLI `report-coverage`.

- [ ] **Step 1: Write coverage tests**

Assert all 295 pages exist in the ledger; 110–117 begin as `PILOT_COMPLETE`; missing page folder cannot be reported as `EXTRACTED`; a relevant `BLOCKED` page keeps global `complete=false`; `NOT_RELEVANT` requires classification reason.

- [ ] **Step 2: Run RED**

Run: `uv run pytest tests/test_coverage.py tests/test_cli.py -v`

- [ ] **Step 3: Implement ledger/report**

Report totals for classified, extracted, not relevant, blocked, pilot complete, figures, measurements by status, rules, conflicts and pages with learning text.

- [ ] **Step 4: Run GREEN**

Run full tests + Ruff.

- [ ] **Step 5: Commit**

Commit: `feat: track F1 extraction coverage`.

---

### Task 5: Generalize pilot QA into per-batch F1 QA

**Files:**
- Create: `src/carpinova_knowledge/report_batch.py`
- Create: `tests/test_report_batch.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Modify: `tests/test_cli.py`
- Modify: `src/carpinova_knowledge/validate_repo.py`
- Runtime outputs: `audits/f1/batches/<batch-id>.md`

**Interfaces:**
- Consumes: canonical page records, visual inventories, figures, measurements, rules and coverage ledger.
- Produces: `build_batch_report(root: Path, batch_id: str) -> dict`, `render_batch_report(report: dict) -> str`; CLI `report-batch`; result `GO|NO_GO`.

- [ ] **Step 1: Write NO_GO tests**

NO_GO when: a batch page lacks PageSpec; relevant text has no ContentSpec; visual inventory declares meaningful figure without FigureSpec/exclusion; technical number lacks source; learning text lacks provenance; unresolved refs exist; generated Markdown is stale.

- [ ] **Step 2: Write GO fixture test**

Use the accepted F0 pilot as a compatibility fixture; generic batch QA must accept it without weakening F0 rules.

- [ ] **Step 3: Run RED**

Run: `uv run pytest tests/test_report_batch.py -v`.

- [ ] **Step 4: Implement generic batch QA**

Do not delete `report-pilot`; it remains an F0 regression gate.

- [ ] **Step 5: Run GREEN**

Run full tests, Ruff, validator and report-pilot.

- [ ] **Step 6: Commit**

Commit: `feat: add F1 batch acceptance reporting`.

---

### Task 6: Add non-destructive thematic consolidation and conflict registry

**Files:**
- Create: `src/carpinova_knowledge/consolidate.py`
- Create: `tests/test_consolidate.py`
- Create: `conflicts/index.json`
- Create: `concepts/index.json`
- Modify: `src/carpinova_knowledge/cli.py`
- Modify: `tests/test_cli.py`
- Runtime outputs: `audits/f1/consolidation/<wave-id>.md`

**Interfaces:**
- Consumes: content/concept/rule/measurement records across completed pages.
- Produces: `build_consolidation_report(root: Path, wave_id: str) -> dict`; CLI `consolidate-wave`.

- [ ] **Step 1: Write contradiction preservation tests**

Given two source-derived claims for the same canonical concept with incompatible values, assert both claims remain intact and an `OPEN` ConflictSpec is created/reported; no value is selected automatically.

- [ ] **Step 2: Write duplicate-source tests**

Repeated identical claims may consolidate under one concept but must retain all source references.

- [ ] **Step 3: Run RED**

Run: `uv run pytest tests/test_consolidate.py -v`.

- [ ] **Step 4: Implement report/index updates**

Automatic logic may detect exact/equivalent normalized values; semantic conflict resolution remains manual/review-only.

- [ ] **Step 5: Run GREEN and commit**

Commit: `feat: consolidate F1 knowledge without losing provenance`.

---

### Task 7: Build multi-batch partial releases and final release manifests

**Files:**
- Create: `src/carpinova_knowledge/build_release.py`
- Create: `tests/test_build_release.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Modify: `tests/test_cli.py`
- Runtime outputs: `dist/releases/<release-id>/...`

**Interfaces:**
- Consumes: completed batch IDs, coverage, taxonomy, conflicts and canonical records.
- Produces: `build_release(root: Path, release_id: str, wave_ids: list[str], out_dir: Path) -> dict`; CLI `build-release`.

- [ ] **Step 1: Write determinism tests**

Two builds from unchanged inputs must have identical SHA-256 outputs.

- [ ] **Step 2: Write coverage-manifest tests**

Partial release manifest declares total pages, processed pages, blocked pages and `complete=false`; `1.0.0` cannot claim `complete=true` unless final coverage criteria pass.

- [ ] **Step 3: Run RED**

Run: `uv run pytest tests/test_build_release.py -v`.

- [ ] **Step 4: Implement stable multi-batch bundling**

Preserve FigureSpec reconstruction metadata, provenance, text layers, candidate rule states and conflict references.

- [ ] **Step 5: Run GREEN and commit**

Commit: `feat: build versioned F1 knowledge releases`.

---

### Task 8: Freeze the F1 extraction runbook before production waves

**Files:**
- Create: `docs/f1-extraction-runbook.md`
- Create: `docs/f1-review-checklist.md`
- Modify: `docs/validation-policy.md`
- Modify: `docs/editorial-policy.md`
- Modify: `docs/visual-spec-policy.md`

**Interfaces:**
- Consumes: Tasks 2–7.
- Produces: exact operational procedure for every wave/batch and human review checklist.

- [ ] **Step 1: Document the Standard Batch Completion Contract**

Include commands for scaffold/render/validate/report-batch/report-coverage/consolidate-wave/build-release.

- [ ] **Step 2: Document page classification rules**

Define when a page is `NOT_RELEVANT`, `BLOCKED`, or requires extraction. `NOT_RELEVANT` never means “not useful to the model”; it means the page was visually inspected and contains no knowledge requiring structured extraction under the approved spec.

- [ ] **Step 3: Document visual/numeric review gates**

No technical number reaches `VALIDATED` without independent technical review; F1 extraction may use `EXTRACTED` or `VISUALLY_VERIFIED` according to evidence.

- [ ] **Step 4: Run full infrastructure gate**

```bash
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
uv run python -m carpinova_knowledge plan-f1 --root .
uv run python -m carpinova_knowledge report-coverage --root .
```

Expected: tests PASS, Ruff PASS, validator 0 errors, pilot `GO`, deterministic F1 plan and coverage report generated.

- [ ] **Step 5: Open F1 Infrastructure PR**

Do not start Wave 01 until this PR is reviewed and merged.

---

### Task 9: Extract F1 Wave 01 — physical pages 1–30

**Files:**
- Modify/Create: page folders listed by W01 batches in `books/cpnc-2025/f1-plan.json`
- Create: `audits/f1/wave-01.md`
- Modify: `books/cpnc-2025/coverage.json`
- Modify as needed: taxonomy, concepts, conflicts

**Interfaces:**
- Consumes: F1 infrastructure and source PDF.
- Produces: complete W01 batch set and partial release `f1-wave-01`.

- [ ] **Step 1: Execute every W01 batch using the Standard Batch Completion Contract**
- [ ] **Step 2: Require `GO` for every W01 batch**
- [ ] **Step 3: Run `consolidate-wave --wave W01`**
- [ ] **Step 4: Generate W01 coverage and partial release twice; hashes must match**
- [ ] **Step 5: Open `knowledge/f1-wave-01` PR; merge only after green QA**

---

### Task 10: Extract F1 Wave 02 — physical pages 31–59

Apply the Standard Batch Completion Contract to all W02 batches.

- [ ] All W02 batches `GO`.
- [ ] Consolidation/conflict audit completed.
- [ ] Global coverage advances without duplicate/omitted physical pages.
- [ ] Partial release deterministic.
- [ ] Open and review `knowledge/f1-wave-02` PR.

---

### Task 11: Extract F1 Wave 03 — physical pages 60–81

Apply the Standard Batch Completion Contract to all W03 batches.

Special review focus: project/assembly examples must remain examples unless the source explicitly states a general rule.

- [ ] All W03 batches `GO`.
- [ ] Consolidation/conflict audit completed.
- [ ] Partial release deterministic.
- [ ] Open and review `knowledge/f1-wave-03` PR.

---

### Task 12: Extract F1 Wave 04 — physical pages 82–109

This covers the beginning of **Materiales** and **Herrajes** immediately before the accepted pilot.

Special review focus: thicknesses, formats, edge banding and hardware dimensions require visual numeric verification status.

- [ ] All W04 batches `GO`.
- [ ] Cross-check terminology against pilot pages 110–117 without rewriting pilot facts silently.
- [ ] Conflicts with pilot facts create ConflictSpec.
- [ ] Open and review `knowledge/f1-wave-04` PR.

---

### Task 13: Extract F1 Wave 05 — physical pages 118–145

Continue **Herrajes** after the F0 pilot; do not reprocess pages 110–117.

Special review focus: slide clearances, hinge systems, pistons, sliding-door systems and wall supports must preserve applicability conditions and examples.

- [ ] All W05 batches `GO`.
- [ ] Pilot + W04 + W05 hardware concepts consolidated non-destructively.
- [ ] Open conflicts explicitly reported.
- [ ] Open and review `knowledge/f1-wave-05` PR.

---

### Task 14: Extract F1 Wave 06 — physical pages 146–172

Covers **Herramientas**.

Special review focus: distinguish tool description, safety/procedure and product-specific reference; do not turn brand/model mentions into universal rules.

- [ ] All W06 batches `GO`.
- [ ] Tool taxonomy expanded only as required by source.
- [ ] Open and review `knowledge/f1-wave-06` PR.

---

### Task 15: Extract F1 Wave 07 — physical pages 173–202

Covers first half of **Despiece y optimización**, measurement and start of kitchen content.

Special review focus: despiece fields, tapacantos, machining services, optimizer inputs, measurement forms and kitchen dimensions must retain their original context.

- [ ] All W07 batches `GO`.
- [ ] Tables/forms represented structurally, not flattened only to prose.
- [ ] Open and review `knowledge/f1-wave-07` PR.

---

### Task 16: Extract F1 Wave 08 — physical pages 203–232

Covers remaining **Despiece y optimización** content including closets, doors, beds and related project examples.

Special review focus: furniture cut lists remain source examples until later Furniture Engine validation; do not silently convert them into parametric formulas.

- [ ] All W08 batches `GO`.
- [ ] Furniture patterns linked to source examples.
- [ ] Open and review `knowledge/f1-wave-08` PR.

---

### Task 17: Extract F1 Wave 09 — physical pages 233–262

Covers first part of **Proyectar mobiliario — Aprende y emprende**.

Special review focus: separate technical furniture knowledge from business/costing/checklist content while preserving both for future Designer/Cell modules.

- [ ] All W09 batches `GO`.
- [ ] Business concepts use appropriate taxonomy instead of being forced into Furniture Engine rules.
- [ ] Open and review `knowledge/f1-wave-09` PR.

---

### Task 18: Extract F1 Wave 10 — physical pages 263–295

Covers end of project/business content, SENA/certificate material, glossary and final pages.

Special review focus: glossary terms should consolidate aliases without deleting the page-specific wording; certificate/administrative pages may be `NOT_RELEVANT` only after visual classification.

- [ ] All W10 batches `GO`.
- [ ] Physical page 295 classified explicitly even if unnumbered/non-technical.
- [ ] Global coverage includes all 295 pages exactly once.
- [ ] Open and review `knowledge/f1-wave-10` PR.

---

### Task 19: Global F1 audit and Knowledge 1.0 release

**Files:**
- Create: `src/carpinova_knowledge/report_f1.py`
- Create: `tests/test_report_f1.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Create: `audits/f1-final-acceptance.md`
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Runtime output: `dist/releases/1.0.0/`

**Interfaces:**
- Consumes: all ten merged waves, pilot F0, coverage, conflicts and consolidated indexes.
- Produces: `build_f1_report(root: Path) -> dict`; CLI `report-f1`; result `GO|NO_GO`; final deterministic `Knowledge 1.0.0` bundle.

- [ ] **Step 1: Write final NO_GO tests**

NO_GO if: any physical page is unclassified; any relevant page is not extracted; any meaningful figure lacks FigureSpec/exclusion; broken refs exist; conflict is silently resolved; coverage report disagrees with page folders; global validator fails; a final bundle claims `complete=true` prematurely.

- [ ] **Step 2: Run RED**

Run: `uv run pytest tests/test_report_f1.py -v`.

- [ ] **Step 3: Implement global report**

Report at minimum: 295/295 classification coverage; relevant extraction coverage; figures detected/spec’d/excluded; measurements by status; rules by status; open/deferred/resolved conflicts; concepts consolidated; learning-text coverage; blocked pages/figures; schema errors.

- [ ] **Step 4: Build Knowledge 1.0 twice**

Compare SHA-256 for every bundle/manifest. Unchanged source must be byte-identical.

- [ ] **Step 5: Run final gate**

```bash
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
uv run python -m carpinova_knowledge report-coverage --root . --require-complete
uv run python -m carpinova_knowledge report-f1 --root .
```

Expected: all PASS, validator 0 errors, pilot `GO`, coverage complete, F1 `GO`.

- [ ] **Step 6: Final reconstruction audit**

Sample every major visual class and every book section. If a future renderer/tutorial author would need to rediscover the semantic meaning of a figure from the PDF, F1 is not complete for that figure.

- [ ] **Step 7: Update release docs**

Set README current release to `1.0.0`; changelog states actual coverage and explicit deferred conflicts/pending technical validations.

- [ ] **Step 8: Open `release/knowledge-1.0` PR**

Do not tag/release 1.0 until human review and green CI.

---

## Self-Review Results

### Spec coverage

- 100 % physical-page classification: Tasks 3, 4, 9–19.
- Adaptive 3–8 page batches: Task 3.
- Checkpoint every ~30 pages: wave topology Tasks 9–18.
- Three text layers/provenance: Standard Batch Contract + Task 5.
- FigureSpec coverage: Task 5 + every wave + final audit.
- Measurements/rules/conflicts: Tasks 2, 5, 6 and all waves.
- Consolidation without provenance loss: Task 6 + wave checkpoints.
- Partial 0.x releases: Task 7 + each wave.
- Knowledge 1.0 exit criteria: Task 19.
- Rights/source constraints: Global Constraints and runbook.

### Type/interface consistency

New commands introduced by this plan: `plan-f1`, `report-coverage`, `report-batch`, `consolidate-wave`, `build-release`, `report-f1`. Each command has one owning task and later tasks depend only on that published interface.

### Proportion

The plan intentionally describes extraction operations and review gates rather than embedding page content or implementation bodies. Semantic extraction remains source-driven and is never pre-invented in the plan.
