# CarpiNova Knowledge — Diseño MVP4A: primera figura técnica renderizable

**Fecha:** 2026-10-13  
**Estado:** diseño auditado, listo para plan; no implementación  
**Repositorio:** `CarpiNova-Knowledge`  
**Base canónica auditada:** `main @ a47119aba3d4711c1ac69f33f7d236d9bc20bb78`  
**Figura piloto:** `FIG-CPNC-2025-P0113-001`  
**Lección consumidora futura:** `LESSON-SLIDES-X-2X-PILOT`

## 1. Propósito

MVP4A convierte **una sola figura técnica ya existente** en Knowledge en una figura que pueda reconstruirse de forma determinística a partir de datos estructurados, sin reinterpretar semánticamente la página fuente en cada consumidor.

El piloto es la corredera telescópica de la página PDF 113:

`FIG-CPNC-2025-P0113-001`

MVP4A termina en `CarpiNova-Knowledge`. No implementa todavía el renderer de `CarpiNova-PC`.

## 2. Problema

Knowledge ya conserva para el piloto identidad, procedencia, entidades, relaciones, medidas, anotaciones, secuencia educativa, estrategia de reconstrucción, accesibilidad y revisión visual.

Pero el registro actual todavía no es render-ready:

- `layers` está vacío;
- `camera` está vacío;
- `geometry` declara precisión pero no posiciones suficientes;
- las anotaciones no tienen placement renderizable;
- `deterministic_required: true` expresa una obligación, no evidencia de que un renderer pueda consumir la figura hoy.

MVP4A cierra ese hueco sin migrar prematuramente todas las figuras.

## 3. Principios no negociables

1. **Knowledge sigue siendo la fuente de verdad.** PC, Cell y otros consumidores no inventan geometría local.
2. **KISS.** Una figura, un contrato 2D mínimo, sin framework gráfico general.
3. **REUSE antes que ADD.** Se reutilizan `entities`, `annotations`, `layers`, `camera`, `visual_style` y `reconstruction`.
4. **No inventar precisión.** Coordenadas derivadas visualmente conservan `approximate`; lo no demostrable permanece `unknown`.
5. **Semántica antes que píxeles.** Se reconstruye la geometría técnica relevante, no cada píxel del libro.
6. **Raster no sustituye FigureSpec.** Un crop fuente puede servir para QA, no como único payload renderizable.
7. **Sin cambios silenciosos.** Medidas, textos, relaciones e IDs canónicos se preservan.
8. **Fail closed.** Solo una figura que satisface todo el contrato opt-in puede declararse render-ready.
9. **Compatibilidad progresiva.** Las demás figuras siguen siendo válidas aunque todavía no sean render-ready.
10. **Interacciones fuera de alcance.** `educational_sequence` y las interacciones de la lección siguen siendo metadata.

## 4. Alcance

### Incluye

- contrato 2D mínimo y opt-in;
- extensión compatible de `figure.schema.json`;
- enriquecimiento exclusivo de `FIG-CPNC-2025-P0113-001`;
- validación de geometría y referencias;
- distribución por el builder BOOK canónico;
- reconstrucción de referencia desde JSON;
- comparación visual contra la fuente.

### No incluye

- cambios en `CarpiNova-PC`;
- renderer de PC;
- `highlight`, `highlight_measurements`, `identify_parts` o `guided_sequence`;
- Canvas, WebGL, Three.js o 3D;
- registry/plugin system de renderers;
- migración de todas las figuras;
- IA generativa;
- corrección técnica de medidas;
- reglas `EXECUTABLE`;
- raster como sustituto del contrato estructurado.

## 5. Verdad canónica que debe preservarse

Archivo:

`books/cpnc-2025/pages/p0113/figures/fig-001.json`

Debe conservar:

- `figure_id = FIG-CPNC-2025-P0113-001`;
- `page_id = PAGE-CPNC-2025-P0113`;
- `type = technical_diagram`;
- `source.pdf_page = 113`;
- `source.printed_page = 91`;
- `reconstruction.preferred_renderer = hybrid`;
- `reconstruction.deterministic_required = true`;
- `reconstruction.generative_image_allowed = false`.

Las medidas enlazadas continúan siendo:

- `MEAS-CPNC-2025-P0113-009` = 13 mm por riel, `VISUALLY_VERIFIED`;
- `MEAS-CPNC-2025-P0113-010` = 14 mm por riel, `VISUALLY_VERIFIED`;
- `MEAS-CPNC-2025-P0113-011` = 15 mm por riel, `VISUALLY_VERIFIED`.

MVP4A no cambia esos valores ni su estado.

## 6. Separar “determinístico requerido” de “render-ready”

Se añade un indicador opt-in dentro de `reconstruction`:

```json
{
  "preferred_renderer": "hybrid",
  "deterministic_required": true,
  "generative_image_allowed": false,
  "render_contract": "normalized-2d-v1"
}
```

Semántica:

- sin `render_contract`: la figura conserva semántica y estrategia prevista, pero ningún consumidor debe asumir que ya puede dibujarla;
- con `render_contract = normalized-2d-v1`: la figura satisface este contrato y puede ser consumida por un renderer 2D compatible;
- `deterministic_required` no cambia de significado.

`render_contract` es opcional para las figuras legacy. Solo el piloto lo declara en MVP4A.

## 7. Coordenadas

`normalized-2d-v1` usa coordenadas locales a la figura en el intervalo `0.0..1.0`.

Se reutiliza `camera`:

```json
{
  "coordinate_space": "normalized_figure",
  "viewport": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0}
}
```

Reglas:

- `(0,0)` = esquina superior izquierda;
- `x` crece a la derecha;
- `y` crece hacia abajo;
- coordenadas renderizables dentro de `[0,1]`;
- independientes de DPI/resolución;
- `source.region` sigue referido a la página y no se mezcla con el espacio interno de figura.

## 8. Geometría mínima

Se reutiliza `entities[].geometry`.

Una entidad renderizada debe conservar `precision` y añadir `primitive` más sus coordenadas.

Primitivas permitidas en MVP4A:

- `rect` → `bounds {x,y,width,height}`;
- `line` → `points` de exactamente dos puntos;
- `polyline` → `points` de dos o más puntos.

Fuera de alcance:

- raw SVG/HTML;
- paths arbitrarios;
- bezier editor;
- transforms 3D;
- materiales/shaders;
- geometría paramétrica general.

Las primitivas deben bastar para una reconstrucción **esquemática y pedagógicamente fiel** de la corredera, cajón, laterales y sección relevante. Si la silueta fuente contiene detalle no demostrable, se simplifica manteniendo la relación técnica y `precision: approximate`.

## 9. Anotaciones y medidas visibles

Se reutiliza `annotations`.

Cada anotación visible debe tener `id` estable y `placement`:

```json
{
  "id": "ANN-...",
  "measurement_id": "MEAS-...",
  "text": "...",
  "placement": {
    "x": 0.0,
    "y": 0.0,
    "precision": "approximate"
  }
}
```

La anotación mantiene `entity_id` o `measurement_id`; no duplica la autoridad numérica del MeasurementSpec.

Las tres notas actuales de holgura pueden conservar su texto canónico. No es obligatorio implementar cotas CAD. `leader_to {x,y}` solo se admite cuando su punto puede derivarse visualmente sin ambigüedad.

## 10. Orden visual

Se reutiliza `layers` únicamente para orden.

Cada layer del piloto debe tener:

- `id`;
- `order` entero;
- `entity_ids` y/o `annotation_ids`.

`order` menor se pinta primero. IDs inexistentes invalidan una figura `normalized-2d-v1`. MVP4A no define animación ni estados interactivos.

## 11. Estilo y renderer `hybrid`

`visual_style` sigue siendo metadata de intención, no una API gráfica completa.

`preferred_renderer` permanece `hybrid` porque así está definido canónicamente. En MVP4A esto significa que el consumidor puede combinar tratamiento visual apropiado con la representación estructurada, pero **la reconstrucción técnica mínima debe producirse desde JSON sin IA y sin reinterpretar el PDF**.

Un crop de la fuente puede usarse para comparación de QA; no es una dependencia runtime obligatoria ni puede ser el único contenido gráfico.

## 12. Schema y validación fail-closed

`figure.schema.json` debe ampliarse sin invalidar figuras legacy por ausencia de `render_contract`.

Cuando `reconstruction.render_contract == normalized-2d-v1`, debe fallar si ocurre cualquiera de estos casos:

- `camera.coordinate_space != normalized_figure`;
- viewport ausente o inválido;
- `layers` vacío;
- referencia a entidad/anotación inexistente;
- primitive no permitida;
- geometry sin coordenadas requeridas;
- coordenadas fuera de `[0,1]`;
- `rect` con ancho/alto no positivos;
- `line` con número de puntos distinto de dos;
- `polyline` con menos de dos puntos;
- anotación visible sin `placement`;
- placement fuera de `[0,1]`;
- IDs de anotación duplicados;
- `entity_id` o `measurement_id` roto respecto al Knowledge canónico.

La validación automática prueba estructura y referencias; no certifica fidelidad visual. Esa parte exige comparación con la fuente.

## 13. Compatibilidad

MVP4A:

- no migra todas las figuras;
- no cambia IDs ni procedencia;
- no elimina campos;
- no cambia el significado de `precision`;
- no duplica la figura en otro modelo;
- no obliga a que toda figura con `deterministic_required=true` sea render-ready inmediatamente.

Las figuras sin `render_contract` siguen siendo Knowledge válido pero no render-ready.

Una futura `normalized-2d-v2` requerirá decisión explícita; no se diseña ahora.

## 14. Gobierno de versión y distribución BOOK

El release publicado `Knowledge 1.0.0` es evidencia histórica cerrada y **no se reetiqueta ni se sobrescribe silenciosamente** para fingir que ya contiene MVP4A.

Como `render_contract` añade capacidad consumible al schema/bundle, antes de publicar MVP4A el plan de implementación debe fijar explícitamente la siguiente versión de Knowledge conforme a la política de release. Hasta ese gate, el trabajo de MVP4A es un candidato no publicado sobre rama.

El cierre técnico debe ejecutar el builder BOOK canónico para `cpnc-2025` y comprobar en el `figures.bundle.json` generado que:

- existe `FIG-CPNC-2025-P0113-001`;
- conserva IDs, fuente y relaciones actuales;
- declara `render_contract = normalized-2d-v1`;
- conserva geometría, placements y layers necesarios;
- las referencias siguen resolviendo tras serializar/distribuir;
- la versión del artefacto generado coincide con la versión que el gate de release haya decidido, y nunca se presenta como el 1.0.0 histórico si su contenido cambió.

`dist/pilot` no sustituye este gate BOOK.

## 15. QA visual

Debe existir una reconstrucción de referencia generada únicamente desde el contrato estructurado del piloto.

Comparada contra la región fuente de la página 113 debe demostrar:

- corredera reconocible como telescópica;
- cajón y laterales mantienen la relación espacial esencial;
- la sección que explica holgura es comprensible;
- las tres notas de holgura están asociadas correctamente;
- ninguna entidad cambia de significado;
- ninguna coordenada `approximate` se presenta como `exact`.

La aceptación es de fidelidad técnica/pedagógica, no pixel-perfect.

Si la geometría estructurada no basta, MVP4A permanece abierto; no se tapa con imagen generada ni geometría inventada.

## 16. Tests mínimos de aceptación

MVP4A debe demostrar:

1. figura legacy sin `render_contract` sigue siendo válida;
2. figura `normalized-2d-v1` válida pasa;
3. cada fallo de la sección 12 falla cerrado;
4. la figura piloto real pasa schema/validación;
5. IDs, fuente, relaciones y measurement links permanecen intactos;
6. builder BOOK real conserva el contrato en `figures.bundle.json`;
7. serialización repetida del mismo Knowledge produce el mismo resultado lógico;
8. revisión visual queda registrada con evidencia.

## 17. Criterio de cierre

MVP4A solo cierra con evidencia de extremo a extremo:

```text
fuente PDF 113
→ FigureSpec canónico enriquecido
→ schema + validación fail-closed
→ builder BOOK
→ figures.bundle.json candidato versionado
→ reconstrucción de referencia desde JSON
→ comparación visual aprobada
```

Token de aceptación recomendado:

`CARPINOVA_KNOWLEDGE_MVP4A_RENDERABLE_FIGURE_PASS`

## 18. Qué habilita después

Solo después de cerrar MVP4A se abre MVP4B en `CarpiNova-PC` para:

- cargar `figures.bundle.json`;
- crear `figures` / `figuresById`;
- resolver `figure_ids` de la lección;
- renderizar `normalized-2d-v1`, preferentemente con SVG nativo;
- mostrar la figura en la lección X/2X.

Las interacciones quedan para un MVP posterior. Primero una figura estática correcta; después se decide si generalizar.

## 19. Ley anti-ruido

```text
REUSE FigureSpec existente
→ un marcador opt-in
→ una figura real
→ validar
→ distribuir
→ probar visualmente
```

No:

```text
new figure engine
scene graph framework
renderer registry
all-figure migration
3D/WebGL
AI reconstruction
PC implementation
Cell implementation
```
