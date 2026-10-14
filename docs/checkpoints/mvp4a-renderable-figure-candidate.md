# CarpiNova Knowledge — MVP4A Renderable Figure Candidate Checkpoint

Fecha: 2026-10-13

Estado: **MVP4A_RENDER_CONTRACT_PASS / RELEASE_BLOCKED_BY_MVP4B**

## Alcance

Checkpoint final de MVP4A para el primer FigureSpec técnico determinísticamente reconstruible.

Este documento certifica la implementación candidata dentro de la rama; **no** publica Knowledge 1.1.0, no autoriza merge a `main` y no autoriza consumo todavía por CarpiNova-PC.

## Identidad de rama

```text
repository = sierraglobalcompany-rgb/CarpiNova-Knowledge
branch = design/renderable-figure-mvp4a-20261013
base SHA = a47119aba3d4711c1ac69f33f7d236d9bc20bb78
verified candidate implementation HEAD = 3175fbe0e5a99834ef98b93b92f3fafaede13ae3
release-review evidence commit = 7b691edc4ed19d8c37d60136b062ad2b4d43fba9
```

El commit que contiene este checkpoint y su CI final se registra como HEAD exacto de PR #31 después de crear este archivo. Un commit no puede incluir criptográficamente su propio SHA en su contenido; por ello se conserva aquí el HEAD de implementación auditado y el HEAD documental inmediatamente anterior, y el HEAD documental final queda anclado por PR #31 + run de CI final.

## Fuente canónica

```text
book_id = cpnc-2025
source PDF pages = 295
source SHA-256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
pilot figure PDF page = 113
printed page = 91
```

Fuente sin cambios respecto a 1.0.0.

## Resultado Tasks 1–6

```text
Task 1 — normalized-2d-v1 schema       GREEN / CLOSED
Task 2 — semantic validation           GREEN / CLOSED
Task 3 — geometry + correction         GREEN / CLOSED
Task 4 — reference SVG renderer        GREEN / CLOSED
Task 5 — visual QA                     PASS / CLOSED
Task 6 — BOOK 1.1.0 candidate          GREEN / CLOSED
Task 7 — final candidate verification  PASS pending only final docs CI
```

## Figura candidata

```text
figure_id = FIG-CPNC-2025-P0113-001
render_contract = normalized-2d-v1
preferred_renderer = hybrid
deterministic_required = true
generative_image_allowed = false
```

Conserva:

- camera normalized 0..1;
- layer ordering determinístico;
- primitivas `rect | line | polyline`;
- perfiles telescópicos mínimos;
- sección lateral cajón/mueble/rieles;
- annotation placements;
- MeasurementSpec refs 009/010/011;
- geometría visual `approximate` y `cross-section` `unknown`;
- identidad/provenance de fuente original.

## Visual review

Evidencia:

`audits/mvp4a/p0113-render-review.md`

Resultado:

```text
MVP4A_TASK5_VISUAL_GATE = PASS
```

SVG aprobado:

```text
SHA-256 = 7aaed9b446f0192e5eea1aaae22a29403b1275e11e96ffbcf3e134d99c825e43
```

## Task 7 — QA completo fresco

Workflow aislado:

```text
name = MVP4A Task7 Final Audit
run = 38464168907
job = 115526689111
result = SUCCESS
checked out exact candidate HEAD = 3175fbe0e5a99834ef98b93b92f3fafaede13ae3
```

Resultados:

```text
pytest = 237 passed / 0 failed
Ruff = PASS
repository validation = valid / 0 errors
pilot report = GO
```

El audit ejecutó realmente:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
```

## BOOK candidate manifest

Dos builds independientes produjeron:

```text
scope = BOOK
book_id = cpnc-2025
knowledge_version = 1.1.0
source_manifest_sha256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
source_page_count = 295
excluded_page_count = 43
distributed pages = 252
content = 976
measurements = 643
rules = 250
figures = 138
lessons = 1
taxonomy_records = 0
```

## Determinismo BOOK

Los cuatro outputs de build A y build B fueron byte-idénticos.

SHA-256:

```text
knowledge.bundle.json = 68872af855f7eb3a7739f6da18a283978567a5e7153d8f3c7f2bb2b1e4742026
figures.bundle.json   = 46dd840fccd6757c56f5a55f9a57c87693f5d0de6f1cf9f1a745b5eaccc0a29a
lessons.bundle.json   = d6de0f0d9b654dd6122395be16ee372be043c21b5ba6652d358b9fab64df9a1e
manifest.json         = 69f360bb0edc02030a5850aed66b6da507371fa472b4eb62a4e503f827cb7c3c
```

## Distribución de P0113

Sobre `figures.bundle.json` del BOOK real:

```text
FIG-CPNC-2025-P0113-001 count = 1
render_contract = normalized-2d-v1
source pdf_page = 113
source printed_page = 91
camera = present
layers = present
geometries = present
annotation placements = present
measurement refs 009/010/011 = present
```

No se perdió el contrato durante serialización.

## Render desde output distribuido

Task 7 pasó el record extraído de `figures.bundle.json` directamente a:

```python
render_normalized_2d_svg(figure)
```

y lo comparó con el render del FigureSpec canónico.

Resultado:

```text
distributed SVG vs canonical SVG = BYTE_IDENTICAL
SHA-256 = 7aaed9b446f0192e5eea1aaae22a29403b1275e11e96ffbcf3e134d99c825e43
```

Esto coincide con el SVG aprobado visualmente en Task 5.

## Audit artifact

```text
name = mvp4a-task7-final-audit
artifact_id = 11848191542
artifact size = 336552 bytes
artifact digest = sha256:5d0e4a1ad4fc68a849367e793411341c0b650d022f2c1c78a8cbedcf8ca667a8
```

El PR temporal #36 utilizado exclusivamente para ejecutar el workflow quedó:

```text
CLOSED
NOT MERGED
DRAFT
```

## KISS / anti-noise diff audit

Comparación completa contra:

`a47119aba3d4711c1ac69f33f7d236d9bc20bb78`

Pre-documentation Task 7:

```text
ahead_by = 28
behind_by = 0
changed files = 18
```

Contenido permitido encontrado:

```text
spec + plan MVP4A
figure schema
semantic validator
one canonical pilot FigureSpec
reference SVG renderer
tests
audit evidence
BOOK candidate version/review
derived pilot bundle/manifest
```

Los dos cambios de `dist/pilot/*` fueron regeneraciones determinísticas obligadas por `report-pilot` después del cambio canónico de P0113. No son una segunda fuente de verdad ni una arquitectura adicional.

Ausente:

```text
new dependencies
permanent workflow additions
CarpiNova-PC changes
CarpiNova-cell changes
3D / WebGL / Three.js
generic renderer registry
plugin architecture
course engine
all-figure migration
new runtime interactions
```

Resultado:

```text
KISS_DIFF_AUDIT = PASS
ANTI_NOISE_AUDIT = PASS
```

## Release status

`docs/releases/1.1.0-review.md` fue avanzado únicamente a:

```text
READY_FOR_MVP4B_COMPATIBILITY_GATE
```

No se usa:

```text
PASS_FOR_1.1.0
```

Knowledge `1.1.0` sigue siendo candidato de rama.

## Consumer blocker

CarpiNova-PC mantiene actualmente:

```text
EXPECTED_KNOWLEDGE_VERSION = 1.0.0
```

Por tanto:

```text
consumer compatibility = BLOCKED
owner = MVP4B
merge Knowledge PR #31 = BLOCKED
publish Knowledge 1.1.0 = BLOCKED
mark PR #31 ready = BLOCKED
```

El release publicado sigue siendo 1.0.0.

## Token de cierre MVP4A

Todos los gates técnicos de MVP4A previos al consumer compatibility gate pasaron:

`CARPINOVA_KNOWLEDGE_MVP4A_RENDERABLE_FIGURE_PASS`

Este token significa **MVP4A implementation pass**, no release 1.1.0 publicado.

## Estado permitido

```text
MVP4A implementation = PASS
Knowledge 1.1.0 = candidate only
PR #31 = DRAFT / NOT MERGED
main = still published 1.0.0
release = BLOCKED
next = MVP4B compatibility in CarpiNova-PC
```

No iniciar MVP4B dentro de este checkpoint.
