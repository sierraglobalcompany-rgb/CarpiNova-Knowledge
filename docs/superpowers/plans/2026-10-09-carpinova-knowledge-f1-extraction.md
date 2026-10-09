# CarpiNova Knowledge F1 — KISS Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extraer y clasificar el 100 % del libro `cpnc-2025` usando la infraestructura validada en F0, con la menor cantidad posible de código nuevo.

**Architecture:** F1 reutiliza F0. No habrá planificador automático de lotes, `WaveSpec`, base de cobertura paralela, motor de consolidación ni releases parciales obligatorias. Los lotes se eligen manualmente según complejidad visual, se validan con las herramientas existentes y el progreso se calcula a partir de los archivos canónicos ya guardados.

**Tech Stack:** Python 3.12; uv; PyMuPDF; JSON Schema; jsonschema; pytest; Ruff; JSON canónico; Markdown generado; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-09-carpinova-knowledge-f0-f1-design.md`

## Principios KISS congelados

1. Reutilizar antes de crear.
2. Una sola fuente de verdad: los JSON de página existentes.
3. No crear una abstracción hasta que exista un caso real que la necesite.
4. No automatizar una decisión que una inspección visual de 30 segundos resuelve mejor.
5. Lotes normales de 5–8 páginas; 3–4 solo cuando sean visualmente densas.
6. No cruzar un límite de capítulo si se puede evitar.
7. Un commit por lote terminado.
8. Un checkpoint cada ~5 lotes o ~30 páginas.
9. El PDF fuente permanece fuera de Git.
10. Ninguna medida técnica se vuelve `VALIDATED` automáticamente.
11. Ninguna regla extraída se vuelve autoridad ejecutable de fabricación en F1.
12. Las páginas físicas 110–117 del piloto F0 ya están completas y no se reextraen salvo corrección explícita.

## Lo que se elimina del plan anterior

- No `f1_planner.py`.
- No `wave.schema.json`.
- No `coverage.schema.json` como segunda base de datos de estado.
- No `consolidate-wave` ni motor de consolidación automática.
- No 10 ramas rígidas `wave-*` predefinidas.
- No bundle/release parcial obligatorio cada ~30 páginas.
- No infraestructura nueva para conflictos antes de encontrar un conflicto real.

Si aparece una contradicción real durante extracción, se registra inmediatamente en `audits/f1/conflicts.json` con las dos fuentes y estado `OPEN`; solo entonces se evalúa si merece schema/herramienta propia.

## Review Focus

1. **Página omitida o duplicada:** el reporte de cobertura debe detectar huecos y duplicados usando `page-map.json` y carpetas `pages/pXXXX/`.
2. **Figura significativa omitida:** un lote no puede quedar `GO` si `visual-inventory.json` marca una figura relevante sin FigureSpec o exclusión justificada.
3. **Número técnico sin verificación visual:** debe mantenerse por debajo de `VALIDATED`.
4. **Texto pedagógico que inventa contenido:** `learning_text` debe conservar procedencia al contenido fuente.
5. **Falso final de F1:** Knowledge 1.0 solo se publica cuando las 295 páginas físicas están clasificadas y las relevantes extraídas.

## Flujo operativo de cada lote

1. Elegir manualmente 5–8 páginas consecutivas desde la primera página pendiente; reducir a 3–4 si son densas.
2. Inspeccionar visualmente todas las páginas del lote.
3. Crear/actualizar `page.json`, `content.json`, `visual-inventory.json`, `measurements.json`, `rules.json` y `figures/*.json` cuando aplique.
4. Generar `source.md`, `normalized.md` y `learning.md` desde los JSON canónicos.
5. Ejecutar `validate`.
6. Ejecutar `report-batch`; exige `GO`.
7. Ejecutar pruebas + Ruff.
8. Commit `knowledge: extract <batch-id>`.
9. Actualizar el reporte de cobertura derivado.

Cada ~5 lotes o ~30 páginas: revisión manual corta de términos duplicados, contradicciones, calidad de FigureSpec y texto pedagógico. No se crea un motor para esa revisión.

---

### Task 1: Corregir CI para F1 y `main`

**Files:**
- Modify: `.github/workflows/knowledge-qa.yml`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: workflow F0 existente.
- Produces: el mismo QA ejecutándose en PRs a `main`, pushes a `main` y ramas `feat/knowledge-f1*` / `knowledge/f1-*`.

- [ ] **Step 1: Escribir prueba RED de política de CI**

La prueba carga el YAML como texto y comprueba que `push` incluye `main`; no introducir dependencia YAML nueva.

- [ ] **Step 2: Ejecutar RED**

Run: `uv run pytest tests/test_cli.py -v`

Expected: FAIL porque el workflow actual solo contempla `feat/knowledge-f0` para push.

- [ ] **Step 3: Cambio mínimo al workflow**

Cambiar únicamente triggers. Mantener exactamente los pasos actuales de Python 3.12, tests, Ruff, `validate` y regresión del piloto.

- [ ] **Step 4: Ejecutar GREEN**

Run: `uv run pytest tests/test_cli.py -v && uv run ruff check .`

Expected: PASS.

- [ ] **Step 5: Commit**

Commit: `ci: run knowledge QA on main and F1`.

---

### Task 2: Generalizar el QA del piloto a cualquier lote

**Files:**
- Create: `src/carpinova_knowledge/report_batch.py`
- Create: `tests/test_report_batch.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Modify: `tests/test_cli.py`
- Keep: `src/carpinova_knowledge/report_pilot.py`

**Interfaces:**
- Consumes: un `batch-*.json` existente y los archivos canónicos de sus páginas.
- Produces: `build_batch_report(root: Path, batch_id: str) -> dict`; CLI `report-batch`; salida `GO|NO_GO`.

- [ ] **Step 1: Escribir pruebas RED**

El piloto F0 debe dar `GO`. Debe dar `NO_GO` si falta una página, falta una figura relevante, hay refs rotas, un número técnico carece de fuente o el Markdown generado está desactualizado.

- [ ] **Step 2: Ejecutar RED**

Run: `uv run pytest tests/test_report_batch.py -v`

- [ ] **Step 3: Implementar reutilizando lógica F0**

Extraer/reutilizar funciones pequeñas del reporte del piloto; no duplicar validadores ni crear framework de reporting.

- [ ] **Step 4: Ejecutar GREEN completo**

Run: `uv run pytest -q && uv run ruff check . && uv run python -m carpinova_knowledge validate --root . && uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot`

Expected: todo PASS y piloto `GO`.

- [ ] **Step 5: Commit**

Commit: `feat: validate any knowledge batch`.

---

### Task 3: Reporte de cobertura derivado, sin nueva base de datos

**Files:**
- Create: `src/carpinova_knowledge/report_coverage.py`
- Create: `tests/test_report_coverage.py`
- Modify: `src/carpinova_knowledge/cli.py`
- Runtime output: `audits/f1/coverage.md`

**Interfaces:**
- Consumes: `manifest.json`, `page-map.json`, batch manifests y carpetas `books/cpnc-2025/pages/`.
- Produces: `build_coverage_report(root: Path) -> dict`; CLI `report-coverage`.

- [ ] **Step 1: Escribir pruebas RED**

Comprobar: total 295; piloto 110–117 contado como completo; detectar página duplicada en batches; detectar huecos; reportar páginas con carpeta completa, páginas solo clasificadas y páginas pendientes.

- [ ] **Step 2: Ejecutar RED**

Run: `uv run pytest tests/test_report_coverage.py -v`

- [ ] **Step 3: Implementar por escaneo**

No crear `coverage.json`. Calcular siempre el estado a partir de los archivos canónicos presentes.

- [ ] **Step 4: Ejecutar GREEN**

Run: `uv run pytest -q && uv run ruff check .`

- [ ] **Step 5: Commit**

Commit: `feat: report knowledge extraction coverage`.

---

### Task 4: Primer lote productivo F1

**Files:**
- Create: `books/cpnc-2025/batches/batch-001.json`
- Create/Modify: páginas físicas iniciales elegidas tras inspección visual, empezando en `p0001`
- Create as needed: `audits/f1/batches/batch-001.md`

**Interfaces:**
- Consumes: schemas y herramientas F0 + Tasks 1–3.
- Produces: primer lote F1 real terminado y patrón operativo probado.

- [ ] **Step 1: Inspeccionar páginas físicas 1–8**

Elegir 5–8 páginas consecutivas sin cruzar un límite natural; si una página es densa, reducir el lote. Documentar el rango exacto en `batch-001.json`.

- [ ] **Step 2: Extraer solo lo soportado por la fuente**

Crear PageSpec y contenido pertinente. Páginas decorativas/legales/separadores se clasifican sin inventar texto técnico.

- [ ] **Step 3: Tratar cada visual relevante**

Crear FigureSpec cuando aporta información reutilizable; justificar exclusión cuando sea meramente decorativo.

- [ ] **Step 4: Renderizar y validar**

Run por página: `render-docs`; luego `validate` y `report-batch --batch batch-001`.

Expected: `GO`.

- [ ] **Step 5: Ejecutar regresión completa**

Run: `uv run pytest -q && uv run ruff check . && uv run python -m carpinova_knowledge report-coverage --root .`

- [ ] **Step 6: Commit**

Commit: `knowledge: extract batch-001`.

---

### Task 5: Extracción secuencial del resto del libro

Este no crea código nuevo salvo que un caso real demuestre una carencia del schema/validador.

**Regla de ejecución:** repetir el flujo operativo de lote desde la primera página física pendiente, respetando el índice existente y saltando 110–117 ya aceptadas.

- [ ] Crear siguiente `batch-NNN.json` con 5–8 páginas normalmente.
- [ ] Inspeccionar visualmente antes de transcribir.
- [ ] Extraer texto/figuras/medidas/reglas soportadas por la fuente.
- [ ] Renderizar Markdown.
- [ ] `validate` + `report-batch = GO` + tests + Ruff.
- [ ] Commit del lote.
- [ ] Cada ~5 lotes/~30 páginas ejecutar `report-coverage` y una revisión manual de contradicciones/taxonomía/calidad.
- [ ] Si aparece contradicción real, crear/actualizar `audits/f1/conflicts.json` preservando ambas fuentes; no resolver automáticamente.
- [ ] Abrir PR por capítulo o aproximadamente 25–40 páginas; no crear ramas vacías por adelantado.

**Criterio para corregir infraestructura:** solo modificar schemas/código si una página real no puede representarse correctamente con F0. La corrección debe ser mínima y acompañada de prueba.

---

### Task 6: Auditoría final y Knowledge 1.0

**Files:**
- Create: `audits/f1/final-coverage.md`
- Create: `audits/f1/final-audit.md`
- Modify: `CHANGELOG.md`
- Build: `dist/knowledge-1.0/`

**Interfaces:**
- Consumes: libro completamente clasificado/extractado.
- Produces: Knowledge 1.0 auditable.

- [ ] **Step 1: Verificar cobertura**

`report-coverage` debe contabilizar las 295 páginas físicas y no dejar huecos desconocidos.

- [ ] **Step 2: Ejecutar QA global**

Run: tests, Ruff, `validate`, todos los batches `report-batch`.

- [ ] **Step 3: Revisar pendientes reales**

Listar conflictos abiertos, figuras bloqueadas, medidas no verificadas y cualquier página `NEEDS_REVIEW`; no ocultarlos.

- [ ] **Step 4: Construir bundle final reproducible**

Generar dos veces y comparar hashes.

- [ ] **Step 5: Publicar `Knowledge 1.0`**

Actualizar changelog y abrir PR final. No marcar 1.0 si cobertura o QA fallan.

---

## Self-review KISS

- **Spec coverage:** conserva cobertura total, lotes adaptativos, tres capas textuales, FigureSpec, QA numérico/visual, conflictos y Knowledge 1.0.
- **Arquitectura eliminada:** planner automático, waves rígidas, schemas de coordinación, ledger de cobertura paralelo, consolidación automática y releases parciales forzadas.
- **Fuente de verdad:** sigue siendo una sola: los archivos JSON de página + batch manifests.
- **Código nuevo mínimo:** solo QA genérico y reporte de cobertura; ambos resuelven riesgos repetitivos reales.
- **Operación principal:** extracción manual asistida y validada, que es el objetivo de F1.

## Execution Handoff

Método aprobado para esta sesión: **Native**. Ejecutar Tasks 1–4 primero. Si el primer lote productivo demuestra que el flujo es estable, continuar Task 5 lote por lote con checkpoints periódicos.