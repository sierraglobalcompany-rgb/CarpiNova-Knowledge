# CarpiNova Knowledge MVP4A — Renderable Figure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convertir exclusivamente `FIG-CPNC-2025-P0113-001` en la primera figura técnica `render-ready` de CarpiNova Knowledge, validada fail-closed, distribuida determinísticamente y comprobada visualmente contra la fuente, sin tocar todavía CarpiNova-PC.

**Architecture:** Extender el FigureSpec existente de forma opt-in con `reconstruction.render_contract = "normalized-2d-v1"`; mantener la forma estructural en JSON Schema y las referencias cruzadas en `validate_repository()`. Enriquecer solo la figura piloto con geometría normalizada sustentada por la página 113, generar una reconstrucción SVG de referencia con una función Python mínima y demostrar que el builder BOOK conserva el contrato. No crear un engine gráfico general.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, `jsonschema`, pytest, Ruff y el builder/validator existentes. No añadir dependencias.

**Spec:** `docs/superpowers/specs/2026-10-13-carpinova-knowledge-renderable-figure-mvp4a-design.md`

## Global Constraints

- Base de implementación: rama `design/renderable-figure-mvp4a-20261013`; no trabajar sobre `main`.
- Fuente canónica: `cpnc-2025`, 295 páginas, SHA-256 `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`.
- Figura única: `FIG-CPNC-2025-P0113-001`.
- Mantener `page_id = PAGE-CPNC-2025-P0113`, `type = technical_diagram`, `preferred_renderer = hybrid`, `deterministic_required = true`, `generative_image_allowed = false`.
- Mantener `MEAS-CPNC-2025-P0113-009/010/011` con 13/14/15 mm y estado `VISUALLY_VERIFIED`; MVP4A no cambia su autoridad técnica.
- Contrato opt-in único: `normalized-2d-v1`.
- Coordenadas locales de figura: `0.0..1.0`; `(0,0)` arriba-izquierda; x a la derecha; y hacia abajo.
- Primitivas MVP4A: `rect`, `line`, `polyline`; nada de raw SVG, arbitrary path, 3D, Canvas, WebGL o renderer registry.
- Figura legacy sin `render_contract` debe seguir siendo válida.
- Raster/crop solo puede usarse como referencia de QA; nunca como sustituto de FigureSpec.
- No tocar CarpiNova-PC ni CarpiNova-cell en MVP4A.
- No ejecutar `highlight`, `highlight_measurements`, `identify_parts` ni `guided_sequence`.
- No añadir dependencias Python ni cambiar `pyproject.toml` salvo que aparezca una necesidad demostrada; la expectativa del plan es cero cambios allí.
- El release histórico `1.0.0` es inmutable. El candidato de esta rama usará `knowledge_version = 1.1.0`, pero **no puede mergearse/publicarse en `main` antes de que MVP4B haga compatible CarpiNova-PC**. PC actual exige `EXPECTED_KNOWLEDGE_VERSION = "1.0.0"`.
- `README.md`, `CHANGELOG.md` y `docs/releases/1.0.0*` continúan describiendo el release publicado 1.0.0 durante MVP4A. No se cambian a “1.1.0 publicado”.
- Cada task se ejecuta como bloque corto: RED → GREEN → CI/evidencia → checkpoint → PARAR. No encadenar tasks automáticamente.

## Review Focus

1. **Compatibilidad legacy:** una figura sin `render_contract` debe seguir validando exactamente como antes; Task 1 lo fija con test explícito.
2. **Geometría fuera de contrato:** primitive desconocida, datos incompletos, puntos fuera de `[0,1]` o rectángulos no positivos deben fallar cerrados; Task 1 cubre shape/ranges.
3. **Referencias internas rotas:** layers con IDs inexistentes, IDs de anotación duplicados o anotaciones visibles sin placement deben producir errores semánticos claros; Task 2 lo prueba.
4. **Precisión inventada:** ninguna coordenada se escribe sin contraste directo con la página 113 exacta; Task 3 exige revisión visual y evidencia antes de editar el piloto.
5. **Version/release drift:** un bundle modificado no puede seguir presentándose como 1.0.0 ni publicarse antes de que PC soporte la nueva versión; Task 6 fija `1.1.0` solo como candidato de rama y Task 7 bloquea merge/release.

---

### Task 1: Contrato estructural `normalized-2d-v1` en JSON Schema

**Files:**
- Modify: `schemas/figure.schema.json`
- Modify: `tests/test_schemas.py`
- Keep unchanged as legacy proof: `tests/fixtures/schemas/valid/figure.json`

**Interfaces:**
- Consumes: `validate_instance("figure", instance)` de `src/carpinova_knowledge/schema_loader.py`.
- Produces: schema opt-in que acepta figuras legacy y define la forma mínima de `render_contract`, `camera`, geometrías, annotations y layers.

- [ ] **Step 1: Write RED tests for legacy compatibility and one valid render-ready figure**

Añadir en `tests/test_schemas.py`:

```python
def test_figure_legacy_without_render_contract_stays_valid() -> None:
    figure = _fixture("figure")
    assert "render_contract" not in figure["reconstruction"]
    assert validate_instance("figure", figure) == []


def test_figure_accepts_normalized_2d_v1_contract() -> None:
    figure = _normalized_2d_figure_fixture()
    assert validate_instance("figure", figure) == []
```

`_normalized_2d_figure_fixture()` debe derivarse de `_fixture("figure")` y añadir solo el mínimo contrato de esta spec: `render_contract`, `camera`, una entidad `rect`, una annotation con `id`/`placement` y un layer no vacío.

- [ ] **Step 2: Write RED parametrized shape/range tests**

Cubrir en schema, como mínimo:

```text
render_contract != normalized-2d-v1
camera.coordinate_space incorrecto
viewport distinto de {0,0,1,1}
primitive desconocida
rect sin bounds
rect width <= 0
rect height <= 0
line con != 2 puntos
polyline con < 2 puntos
point x/y fuera de [0,1]
annotation placement x/y fuera de [0,1]
layers vacío cuando existe render_contract
```

Cada mutación debe hacer que `validate_instance("figure", figure)` devuelva al menos un error.

- [ ] **Step 3: Run schema RED**

Run:

```bash
uv run pytest tests/test_schemas.py -q
```

Expected: los nuevos tests `normalized-2d-v1` fallan porque el schema actual no acepta `render_contract` y no conoce la forma requerida.

- [ ] **Step 4: Extend `schemas/figure.schema.json` minimally**

Decisiones exactas:

- `reconstruction.render_contract`: opcional, enum solo `"normalized-2d-v1"`.
- Si existe ese valor, exigir `camera` y `layers` no vacío.
- `camera.coordinate_space`: `"normalized_figure"`.
- `camera.viewport`: exactamente `x=0`, `y=0`, `width=1`, `height=1`.
- Punto: objeto `{x, y}` numérico con ambos valores `[0,1]`, sin propiedades adicionales necesarias para MVP4A.
- `rect`: `bounds {x,y,width,height}` con x/y `[0,1]`, width/height `>0`, y validación posterior semántica de `x+width <= 1`, `y+height <= 1` si JSON Schema se vuelve innecesariamente complejo.
- `line`: exactamente 2 puntos.
- `polyline`: mínimo 2 puntos.
- Annotation puede conservar campos legacy, pero cuando declara `placement`, este sigue `{x,y,precision}` y `precision ∈ {exact, approximate, unknown}`; el requisito “annotation visible => placement” queda en Task 2 porque depende de layers.
- Layer: `{id, order, entity_ids?, annotation_ids?}`; `order` entero; al menos una de las listas presente y no vacía.

No crear un schema nuevo paralelo; extender `figure.schema.json`.

- [ ] **Step 5: Run schema GREEN**

```bash
uv run pytest tests/test_schemas.py -q
uv run ruff check tests/test_schemas.py
```

Expected: PASS.

- [ ] **Step 6: Run legacy repository regression**

```bash
uv run pytest tests/test_validate_repo.py::test_valid_repository_has_zero_errors -q
```

Expected: PASS con el fixture legacy intacto.

- [ ] **Step 7: Commit Task 1**

```bash
git add schemas/figure.schema.json tests/test_schemas.py
git commit -m "feat: define normalized 2d figure contract"
```

- [ ] **Step 8: Open/refresh a draft PR and require Knowledge QA for exact Task 1 HEAD**

No marcar ready. Registrar run ID, resultado y HEAD en checkpoint Task 1. Después PARAR.

---

### Task 2: Validación semántica fail-closed de referencias renderables

**Files:**
- Modify: `src/carpinova_knowledge/validate_repo.py`
- Modify: `tests/test_validate_repo.py`

**Interfaces:**
- Consumes: shape válido de Task 1.
- Produces: validación semántica dentro de `validate_repository(root: Path) -> dict[str, Any]`; no nuevo servicio/validator paralelo.

- [ ] **Step 1: Add a helper in tests to turn the existing valid figure into a render-ready fixture**

El helper debe añadir IDs explícitos a annotations, placements y layers, manteniendo el fixture legacy original sin cambios en disco.

- [ ] **Step 2: Write RED tests for semantic failures**

Añadir tests que muten la figura dentro de `_valid_repo(tmp_path)` y comprueben códigos concretos:

```text
render_contract_unknown_layer_entity
render_contract_unknown_layer_annotation
render_contract_duplicate_annotation_id
render_contract_visible_annotation_missing_placement
render_contract_duplicate_layer_member
unresolved_reference   # annotation.measurement_id roto
unresolved_reference   # annotation.entity_id roto
render_contract_bounds_out_of_view  # rect x+width/y+height > 1 si no quedó en schema
```

También añadir un test positivo:

```python
def test_valid_render_contract_repository_has_zero_errors(tmp_path: Path) -> None:
    ...
    assert validate_repository(tmp_path)["valid"] is True
```

- [ ] **Step 3: Run semantic RED**

```bash
uv run pytest tests/test_validate_repo.py -q
```

Expected: los nuevos casos semánticos fallan porque `validate_repository()` todavía no inspecciona layers/annotation refs.

- [ ] **Step 4: Implement one small helper in `validate_repo.py`**

Firma preferida:

```python
def _validate_render_contract(
    record: dict[str, Any],
    path: Path,
    errors: list[dict[str, Any]],
    refs: list[tuple[str, Path, str | None, str]],
) -> None:
    ...
```

Responsabilidades exclusivas:

- retornar inmediatamente si `render_contract != "normalized-2d-v1"`;
- construir sets locales de `entity.id`, `annotation.id` y miembros de layers;
- detectar referencias locales inexistentes/duplicadas;
- exigir placement solo a annotations que realmente aparecen en layers;
- añadir `annotation.entity_id` y `annotation.measurement_id` a `refs` para resolver con el mecanismo global existente;
- comprobar bounds sumados si esa condición no quedó expresada limpiamente en JSON Schema.

No mover lógica no relacionada de `validate_repository()`.

- [ ] **Step 5: Call the helper from the existing figure loop**

Llamarlo después del schema/source/reconstruction checks y antes del cierre del bloque de figura.

- [ ] **Step 6: Run semantic GREEN + focused regression**

```bash
uv run pytest tests/test_validate_repo.py tests/test_schemas.py -q
uv run ruff check src/carpinova_knowledge/validate_repo.py tests/test_validate_repo.py
```

Expected: PASS.

- [ ] **Step 7: Commit Task 2**

```bash
git add src/carpinova_knowledge/validate_repo.py tests/test_validate_repo.py
git commit -m "feat: validate renderable figure references"
```

- [ ] **Step 8: Require CI on exact Task 2 HEAD, checkpoint, PARAR**

---

### Task 3: Derivar y versionar la geometría real de la figura P0113

**Files:**
- Modify: `books/cpnc-2025/pages/p0113/figures/fig-001.json`
- Create: `tests/test_mvp4a_figure.py`
- Create: `audits/mvp4a/p0113-geometry-review.md`

**Interfaces:**
- Consumes: schema + validator GREEN de Tasks 1–2 y el PDF canónico exacto.
- Produces: `FIG-CPNC-2025-P0113-001` con `render_contract = normalized-2d-v1` y evidencia de cómo se derivó cada geometría/placement.

- [ ] **Step 1: Gate exact source before touching coordinates**

Verificar el archivo fuente:

```text
libros_1751553390342_Carpintería para no Carpinteros Versión 2025.pdf
SHA-256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
physical page = 113
source.region = figure region already stored in FigureSpec
```

Si la fuente exacta no está disponible para inspección visual: marcar `UNRESOLVED`, no editar geometría y PARAR.

- [ ] **Step 2: Write the geometry review before the data mutation**

En `audits/mvp4a/p0113-geometry-review.md`, registrar por entidad/anotación:

```text
entity/annotation id
source evidence observed
chosen primitive
normalized coordinates
precision = approximate|unknown
reason the value is demonstrable from source
```

No promover `unknown` a `approximate` sin evidencia directa visible.

- [ ] **Step 3: Write RED canonical-figure tests**

`tests/test_mvp4a_figure.py` debe cargar el archivo real y exigir, como mínimo:

```text
figure_id/page_id/type unchanged
source pdf/printed page unchanged
preferred_renderer = hybrid
generative_image_allowed = false
render_contract = normalized-2d-v1
camera.coordinate_space = normalized_figure
layers non-empty
three measurement annotation links 009/010/011 preserved
13/14/15 measurement records remain VISUALLY_VERIFIED in measurements.json
all layer entity IDs resolve locally
all layer annotation IDs resolve locally
visible annotations have placement
validate_repository(ROOT) has no errors
```

No fijar en test coordenadas “inventadas”. Si una coordenada exacta se fija como regresión, debe copiarse del review visual ya registrado en Step 2.

- [ ] **Step 4: Run canonical RED**

```bash
uv run pytest tests/test_mvp4a_figure.py -q
```

Expected: FAIL porque la figura real aún no declara el contrato/geometría/layers.

- [ ] **Step 5: Enrich only `fig-001.json` from the reviewed values**

Reglas:

- preservar todos los IDs y relaciones existentes;
- añadir `render_contract` al reconstruction actual, no reemplazarlo;
- `camera` declara el espacio normalizado;
- usar solo `rect`, `line`, `polyline`;
- asignar IDs estables a las annotations que se usan en layers;
- añadir placement solo sustentado por revisión;
- layers expresan orden visual, no estado interactivo;
- mantener `educational_sequence` sin ejecutarla/modificar su significado.

- [ ] **Step 6: Run canonical GREEN + full repository validator**

```bash
uv run pytest tests/test_mvp4a_figure.py tests/test_validate_repo.py tests/test_schemas.py -q
uv run python -m carpinova_knowledge validate --root .
uv run ruff check tests/test_mvp4a_figure.py
```

Expected: PASS / zero validation errors.

- [ ] **Step 7: Commit Task 3**

```bash
git add books/cpnc-2025/pages/p0113/figures/fig-001.json tests/test_mvp4a_figure.py audits/mvp4a/p0113-geometry-review.md
git commit -m "feat: make slide figure renderable"
```

- [ ] **Step 8: CI exact HEAD + checkpoint + PARAR**

---

### Task 4: Renderer SVG de referencia mínimo para QA

**Files:**
- Create: `src/carpinova_knowledge/render_figure.py`
- Create: `tests/test_render_figure.py`

**Interfaces:**
- Consumes: una figura ya validada `normalized-2d-v1`.
- Produces:

```python
def render_normalized_2d_svg(figure: dict[str, Any]) -> str:
    ...
```

Este renderer es tooling de referencia en Knowledge, no el renderer de CarpiNova-PC y no se registra como framework/plugin.

- [ ] **Step 1: Write RED tests for supported primitives and determinism**

Cubrir:

```text
reject figure without normalized-2d-v1
layers sorted by order
rect renders
line renders
polyline renders
visible annotation renders as escaped text
unknown referenced ID raises ValueError defensively
same input => byte-identical SVG string
```

El test no necesita pixel snapshots; debe inspeccionar elementos/atributos esenciales y comparar output repetido.

- [ ] **Step 2: Run renderer RED**

```bash
uv run pytest tests/test_render_figure.py -q
```

Expected: FAIL porque el módulo no existe.

- [ ] **Step 3: Implement only `render_normalized_2d_svg()`**

Decisiones:

- Python stdlib solamente;
- escapar texto con `html.escape`;
- usar un `viewBox` determinístico y transformar coordenadas normalizadas de forma simple;
- estilo fijo de QA, legible y neutro; no crear API de temas;
- no interpretar `educational_sequence`;
- no ejecutar interacciones;
- no leer PDF dentro del renderer;
- no crear CLI nuevo salvo que una necesidad real lo demuestre.

- [ ] **Step 4: Run renderer GREEN**

```bash
uv run pytest tests/test_render_figure.py -q
uv run ruff check src/carpinova_knowledge/render_figure.py tests/test_render_figure.py
```

Expected: PASS.

- [ ] **Step 5: Render the real pilot into ignored scratch space**

Ejemplo reproducible:

```bash
uv run python -c "import json; from pathlib import Path; from carpinova_knowledge.render_figure import render_normalized_2d_svg; p=Path('books/cpnc-2025/pages/p0113/figures/fig-001.json'); f=json.loads(p.read_text(encoding='utf-8')); out=Path('work/mvp4a/p0113.svg'); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(render_normalized_2d_svg(f), encoding='utf-8')"
```

`work/` sigue sin commit.

- [ ] **Step 6: Commit Task 4**

```bash
git add src/carpinova_knowledge/render_figure.py tests/test_render_figure.py
git commit -m "feat: render normalized figure reference svg"
```

- [ ] **Step 7: CI exact HEAD + checkpoint + PARAR**

---

### Task 5: Aceptación visual real contra la página 113

**Files:**
- Modify/Create: `audits/mvp4a/p0113-render-review.md`
- No product code unless the visual gate exposes a real defect.

**Interfaces:**
- Consumes: SVG generado por Task 4 + fuente PDF exacta.
- Produces: evidencia humana/visual de que el contrato conserva el significado técnico/pedagógico.

- [ ] **Step 1: Generate a fresh SVG from the exact Task 4 HEAD**

No reutilizar un SVG viejo sin verificar hash/HEAD.

- [ ] **Step 2: Inspect source page 113 and the generated SVG side by side**

Verificar explícitamente:

```text
corredera reconocible como telescópica
cajón/laterales conservan relación espacial esencial
sección/espacio de holgura es comprensible
notas 13/14/15 mm asociadas correctamente
no entity meaning drift
no approximate shown/documented as exact
no invented detail required to understand the figure
```

- [ ] **Step 3: Record evidence in `p0113-render-review.md`**

Registrar:

```text
source PDF SHA
source page
figure ID
feature HEAD
SVG SHA-256
PASS/FAIL per criterion
review notes
```

No copiar/commitear el PDF ni un crop raster de la fuente.

- [ ] **Step 4: If visual review FAILS, stop and fix root cause in the owning prior task**

No “aceptar con nota” una geometría incorrecta. Volver a Task 3 si los datos son erróneos; a Task 4 si solo el renderer de referencia es erróneo.

- [ ] **Step 5: Commit PASS evidence only after actual inspection**

```bash
git add audits/mvp4a/p0113-render-review.md
git commit -m "docs: record MVP4A visual figure review"
```

- [ ] **Step 6: Checkpoint Task 5 and PARAR**

No avanzar a versionado si el review no es PASS.

---

### Task 6: Bundle BOOK candidato 1.1.0 y prueba de distribución

**Files:**
- Modify: `src/carpinova_knowledge/build_dist.py`
- Modify: `tests/test_build_dist.py`
- Modify: `tests/test_cli.py`
- Create: `docs/releases/1.1.0-review.md`
- Do NOT modify yet: `README.md`, `CHANGELOG.md`, `docs/releases/1.0.0.md`

**Interfaces:**
- Consumes: figura real visualmente aprobada.
- Produces: bundle BOOK determinístico identificado como candidato `1.1.0`, con el contrato intacto.

- [ ] **Step 1: Write RED version/distribution assertions first**

En `tests/test_build_dist.py`:

- cambiar la expectativa del BOOK candidate a `1.1.0`;
- leer `figures.bundle.json` del build BOOK;
- localizar `FIG-CPNC-2025-P0113-001`;
- assert `reconstruction.render_contract == "normalized-2d-v1"`;
- assert camera/layers/geometría/annotation placements sobrevivieron a serialización;
- assert source/IDs/measurement references se conservaron;
- mantener el build doble y comparación de hashes existente.

En `tests/test_cli.py` cambiar solo el test de `build-book-dist` para esperar `1.1.0` en esta rama candidata.

- [ ] **Step 2: Run candidate-version RED**

```bash
uv run pytest tests/test_build_dist.py tests/test_cli.py -q
```

Expected: FAIL porque `BOOK_KNOWLEDGE_VERSION` sigue en `1.0.0`.

- [ ] **Step 3: Set candidate BOOK version to 1.1.0**

En `src/carpinova_knowledge/build_dist.py`:

```python
BOOK_KNOWLEDGE_VERSION = "1.1.0"
```

No cambiar `KNOWLEDGE_VERSION = "0.1.0"` del batch/piloto.

- [ ] **Step 4: Add `docs/releases/1.1.0-review.md` as CANDIDATE_NOT_RELEASED**

Debe registrar:

```text
status = CANDIDATE_NOT_RELEASED
base release = 1.0.0
new capability = normalized-2d-v1 for one figure
source SHA unchanged
MVP4A visual gate result
consumer blocker = CarpiNova-PC current EXPECTED_KNOWLEDGE_VERSION is 1.0.0
merge/release blocked until MVP4B compatibility gate
```

No afirmar `PASS_FOR_1.1.0` todavía.

- [ ] **Step 5: Run candidate GREEN**

```bash
uv run pytest tests/test_build_dist.py tests/test_cli.py -q
uv run python -m carpinova_knowledge build-book-dist --root . --book-id cpnc-2025 --out work/mvp4a-book
```

Inspeccionar `work/mvp4a-book/manifest.json` y `figures.bundle.json`.

Expected:

```text
scope = BOOK
book_id = cpnc-2025
knowledge_version = 1.1.0
source_manifest_sha256 unchanged
FIG-CPNC-2025-P0113-001 render_contract = normalized-2d-v1
```

- [ ] **Step 6: Commit Task 6**

```bash
git add src/carpinova_knowledge/build_dist.py tests/test_build_dist.py tests/test_cli.py docs/releases/1.1.0-review.md
git commit -m "build: prepare Knowledge 1.1 render contract candidate"
```

- [ ] **Step 7: CI exact HEAD + checkpoint + PARAR**

**Hard guardrail:** no merge a `main`, no GitHub release 1.1.0, no actualización del README como versión publicada.

---

### Task 7: Verificación completa del candidato MVP4A y handoff a MVP4B

**Files:**
- Create: `docs/checkpoints/mvp4a-renderable-figure-candidate.md`
- Update `docs/releases/1.1.0-review.md` only with fresh evidence from this task.
- No new product feature files.

**Interfaces:**
- Consumes: Tasks 1–6 GREEN.
- Produces: candidato auditable `MVP4A_RENDER_CONTRACT_PASS / RELEASE_BLOCKED_BY_MVP4B`.

- [ ] **Step 1: Run full fresh QA from the final candidate HEAD**

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python -m carpinova_knowledge validate --root .
uv run python -m carpinova_knowledge report-pilot --root . --batch batch-000-pilot
```

Todos deben PASS.

- [ ] **Step 2: Rebuild BOOK twice and compare every output hash**

```bash
rm -rf work/mvp4a-book-a work/mvp4a-book-b
uv run python -m carpinova_knowledge build-book-dist --root . --book-id cpnc-2025 --out work/mvp4a-book-a
uv run python -m carpinova_knowledge build-book-dist --root . --book-id cpnc-2025 --out work/mvp4a-book-b
```

Comparar SHA-256 de:

```text
knowledge.bundle.json
figures.bundle.json
lessons.bundle.json
manifest.json
```

Expected: byte-identical.

- [ ] **Step 3: Re-run the real pilot figure checks on distributed output**

Desde `figures.bundle.json` comprobar:

```text
figure exists exactly once
render_contract = normalized-2d-v1
source identity unchanged
measurement refs 009/010/011 present
camera/layers/geometries/placements present
```

- [ ] **Step 4: Re-render from the distributed figure, not only source JSON**

Pasar el record extraído de `figures.bundle.json` a `render_normalized_2d_svg()` y comparar su SVG con el generado desde el JSON canónico.

Expected: mismo resultado lógico/byte-identical si el renderer serializa solo datos del record.

- [ ] **Step 5: Audit final diff against canonical base**

Comparar rama contra:

`a47119aba3d4711c1ac69f33f7d236d9bc20bb78`

Debe contener solo:

```text
spec + plan docs
figure schema
validator
pilot figure data
tests
reference renderer
audit evidence
1.1.0 candidate version/review docs
```

No workflows nuevos, dependencias nuevas, PC/Cell, 3D, engine genérico ni figuras adicionales.

- [ ] **Step 6: Record exact evidence**

`docs/checkpoints/mvp4a-renderable-figure-candidate.md` debe contener:

```text
final branch HEAD
base SHA
CI run ID
pytest count/result
Ruff result
validate result
pilot report result
BOOK manifest identity
bundle hashes
visual-review evidence SHA
rendered SVG SHA
KISS diff audit
consumer compatibility blocker
```

Añadir token solo si todos los gates anteriores pasaron:

`CARPINOVA_KNOWLEDGE_MVP4A_RENDERABLE_FIGURE_PASS`

- [ ] **Step 7: Update `docs/releases/1.1.0-review.md` to READY_FOR_CONSUMER_COMPATIBILITY**

No usar `PASS_FOR_1.1.0`; estado exacto:

`READY_FOR_MVP4B_COMPATIBILITY_GATE`

- [ ] **Step 8: Final CI on exact documentation HEAD**

Repetir Knowledge QA y registrar el run.

- [ ] **Step 9: STOP without merge**

Estado final permitido del bloque:

```text
MVP4A implementation = PASS
Knowledge 1.1.0 = candidate only
PR = DRAFT / NOT MERGED
main = still published 1.0.0
next = MVP4B compatibility in CarpiNova-PC
```

No marcar el PR ready y no mergear Knowledge hasta que un plan separado de MVP4B haga que PC acepte el nuevo Knowledge sin romper 1.0.0 durante la transición.

---

## Self-Review Result

### 1. Spec coverage

- opt-in render contract → Task 1
- fail-closed shape/ranges → Task 1
- cross-reference semantics → Task 2
- real P0113 geometry from source → Task 3
- deterministic reference reconstruction → Task 4
- human visual comparison → Task 5
- BOOK distribution + deterministic serialization → Task 6/7
- no silent 1.0.0 overwrite → Task 6/7
- no PC implementation/interactions/general engine → global constraints + diff audit Task 7

No spec requirement queda sin owner.

### 2. Step scan

Cada step produce una acción verificable: RED, comando, implementación limitada, GREEN o commit. La única entrada no prefijable numéricamente —coordenadas de la figura— se resuelve primero mediante contraste visual obligatorio de la fuente, no por decisión libre del implementador.

### 3. Type/interface consistency

- schema name continúa `figure`;
- validator público continúa `validate_repository(root: Path)`;
- builder público continúa `build_book_distribution(root, book_id, out_dir)`;
- renderer nuevo tiene una sola interfaz: `render_normalized_2d_svg(figure) -> str`;
- bundle continúa llamándose `figures.bundle.json`;
- no se crea un segundo modelo de figura.

### 4. Review Focus coverage

Los cinco riesgos del encabezado tienen test/gate propietario en Tasks 1, 2, 3 y 6/7.

### 5. Proportion / KISS

La implementación esperada toca dos puntos existentes (`figure.schema.json`, `validate_repository()`), un solo FigureSpec real y un renderer de QA pequeño. El plan explícitamente evita framework gráfico, runtime consumer, interacciones y migración masiva.

## Execution Handoff

Método preservado del proyecto: **Native execution by ChatGPT**, task por task, con CI/checkpoint y parada entre tasks. No delegar a Codex salvo bloqueo genuino que no pueda resolverse con las herramientas disponibles.

Antes de implementar, el usuario debe revisar/aprobar este plan. Después, ejecutar únicamente Task 1 y parar en su checkpoint.