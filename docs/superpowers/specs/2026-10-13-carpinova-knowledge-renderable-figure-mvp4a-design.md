# CarpiNova Knowledge — Diseño MVP4A: primera figura técnica renderizable

**Fecha:** 2026-10-13  
**Estado:** diseño aprobado para auditoría, no implementación  
**Repositorio:** `CarpiNova-Knowledge`  
**Base canónica:** `main @ a47119aba3d4711c1ac69f33f7d236d9bc20bb78`  
**Figura piloto:** `FIG-CPNC-2025-P0113-001`  
**Lección consumidora futura:** `LESSON-SLIDES-X-2X-PILOT`

## 1. Propósito

MVP4A debe convertir **una sola figura técnica ya existente** en Knowledge en una figura que pueda reconstruirse de forma determinística a partir de datos estructurados, sin volver a interpretar semánticamente la página fuente en cada consumidor.

El piloto es la figura de la corredera telescópica de la página PDF 113:

`FIG-CPNC-2025-P0113-001`

MVP4A termina en `CarpiNova-Knowledge`. No implementa todavía el renderer de `CarpiNova-PC`.

## 2. Problema que resuelve

Knowledge 1.0.0 ya conserva para la figura piloto:

- identidad y procedencia;
- `entities`;
- `relationships`;
- `measurements`;
- `annotations`;
- `educational_sequence`;
- `reconstruction`;
- resumen accesible;
- revisión visual.

Sin embargo, el registro actual no es todavía un contrato de render completo:

- `layers` está vacío;
- `camera` está vacío;
- las geometrías declaran `precision`, pero no contienen posiciones suficientes para dibujar;
- las anotaciones no tienen placement renderizable;
- `deterministic_required: true` expresa una obligación de reconstrucción, no evidencia de que la figura ya sea consumible por un renderer.

MVP4A cierra ese hueco sin generalizar prematuramente a todas las figuras.

## 3. Principios no negociables

1. **Knowledge sigue siendo la fuente de verdad.** PC, Cell u otros consumidores no inventarán geometría local.
2. **KISS.** Una figura, un contrato 2D mínimo, sin framework gráfico general.
3. **REUSE antes que ADD.** Se reutilizan `entities`, `annotations`, `layers`, `camera`, `visual_style` y `reconstruction` antes de crear estructuras paralelas.
4. **No inventar precisión.** Coordenadas derivadas visualmente de la fuente se conservan como `approximate`; `unknown` permanece `unknown`.
5. **Semántica antes que píxeles.** El objetivo es reconstruir la geometría técnica relevante, no clonar cada píxel del libro.
6. **Raster no sustituye FigureSpec.** Un recorte de la página puede servir como referencia de QA, pero no puede ser el único payload que haga “renderizable” a la figura.
7. **Sin cambios silenciosos.** Textos, medidas y relaciones continúan apuntando a sus IDs y fuentes canónicas.
8. **Fail closed.** Una figura solo puede declararse `render-ready` si satisface íntegramente el contrato opt-in.
9. **Compatibilidad progresiva.** Las figuras 1.0.0 que todavía no sean renderizables no deben romperse ni recibir geometría ficticia.
10. **No ejecutar interacciones todavía.** `educational_sequence` e interacciones de la lección siguen siendo metadata.

## 4. Alcance

### Incluye

- definir un contrato 2D renderizable mínimo y opt-in;
- extender el schema de figura de forma compatible;
- enriquecer exclusivamente `FIG-CPNC-2025-P0113-001` con geometría/placement sustentado por la fuente;
- validar referencias internas del contrato;
- mantener el builder de `figures.bundle.json` como vía canónica de distribución;
- demostrar que el BOOK distribution real conserva la figura render-ready;
- evidencia visual que compare la reconstrucción de referencia con la región fuente.

### No incluye

- renderer de CarpiNova-PC;
- cambios en CarpiNova-PC;
- interacciones `highlight`, `highlight_measurements`, `identify_parts` o `guided_sequence`;
- animación;
- Canvas, WebGL, Three.js o 3D;
- registry/plugin system de renderers;
- migración de todas las figuras;
- IA generativa;
- corrección técnica de medidas;
- promoción de reglas a `EXECUTABLE`;
- assets raster como sustituto del contrato estructurado.

## 5. Figura piloto y verdad canónica

La implementación solo puede enriquecer el registro existente:

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

La geometría nueva se deriva visualmente de la región fuente ya declarada. Si una forma o ubicación no puede determinarse suficientemente, no se inventa: se conserva o marca `unknown` y no se usa como requisito del dibujo piloto.

## 6. Separar “determinístico requerido” de “render-ready”

MVP4A añade un indicador opt-in dentro de `reconstruction`:

```json
{
  "preferred_renderer": "hybrid",
  "deterministic_required": true,
  "generative_image_allowed": false,
  "render_contract": "normalized-2d-v1"
}
```

Semántica:

- ausencia de `render_contract`: la figura conserva su semántica/reconstrucción prevista, pero ningún consumidor debe asumir que puede dibujarla automáticamente;
- `render_contract = normalized-2d-v1`: el registro satisface el contrato mínimo definido por esta spec y puede ser consumido por un renderer 2D compatible;
- `deterministic_required` no cambia de significado y no se reutiliza como bandera de completitud.

El campo es opcional para compatibilidad con las demás figuras 1.0.0. Solo la figura piloto lo declara en MVP4A.

## 7. Sistema de coordenadas

`normalized-2d-v1` usa coordenadas locales a la figura, normalizadas de `0.0` a `1.0`.

Se reutiliza `camera` para declarar el espacio:

```json
{
  "coordinate_space": "normalized_figure",
  "viewport": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0}
}
```

Reglas:

- `(0,0)` es la esquina superior izquierda de la figura;
- `x` crece hacia la derecha;
- `y` crece hacia abajo;
- toda coordenada renderizable debe quedar dentro de `[0,1]`;
- el sistema es independiente de resolución, DPI y tamaño de pantalla;
- `source.region` continúa expresándose respecto a la página y no se mezcla con las coordenadas internas de la figura.

No se introduce una segunda unidad gráfica en MVP4A.

## 8. Geometría mínima de entidades

Se reutiliza `entities[].geometry`.

Para una entidad renderizada bajo `normalized-2d-v1`, `geometry` debe contener:

- `precision` existente;
- `primitive`;
- los datos correspondientes a esa primitive.

Primitivas permitidas en MVP4A:

- `rect` → `bounds {x,y,width,height}`;
- `line` → `points` de exactamente dos puntos;
- `polyline` → `points` de dos o más puntos.

No se incorporan todavía:

- raw SVG;
- HTML embebido;
- paths arbitrarios;
- bezier editor;
- transforms 3D;
- materiales físicos;
- shaders;
- geometría paramétrica general.

Las primitivas disponibles deben ser suficientes para una reconstrucción **esquemática y pedagógicamente fiel** de la corredera, cajón, laterales y sección relevante. Si una silueta compleja del render original no puede expresarse sin inventar detalle, se simplifica preservando la relación técnica y manteniendo `precision: approximate`.

## 9. Anotaciones y medidas visibles

Se reutiliza `annotations`.

Cada anotación que vaya a mostrarse en la reconstrucción debe tener un `id` estable y un `placement`:

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

La anotación continúa enlazando por `entity_id` o `measurement_id`; no duplica la autoridad numérica del MeasurementSpec.

MVP4A puede utilizar el `text` canónico ya registrado para mostrar las tres notas de holgura. No convierte esos valores a una nueva verdad técnica ni cambia su estado de validación.

No es obligatorio implementar flechas/cotas CAD. Si la fuente permite identificar visualmente un punto de referencia sin ambigüedad, podrá añadirse un `leader_to {x,y}` normalizado; si no, se omite.

## 10. Orden visual con `layers`

Se reutiliza `layers` para ordenar elementos, no para crear un motor de escenas.

Cada layer del piloto debe tener:

- `id`;
- `order` entero;
- `entity_ids` y/o `annotation_ids`.

Reglas:

- `order` menor se pinta primero;
- IDs inexistentes invalidan una figura que declara `normalized-2d-v1`;
- una misma entidad/anotación no debe aparecer contradictoriamente en múltiples layers;
- el contrato no define animación ni estados interactivos.

## 11. Estilo

`visual_style` continúa siendo metadata de intención visual.

MVP4A no convierte colores, tipografías o strokes en una API gráfica completa. El contrato debe permitir que un renderer futuro aplique un estilo CarpiNova consistente sin alterar la geometría ni el significado.

La aceptación de renderabilidad depende de geometría, placement, orden y referencias; no de pixel-perfect styling.

## 12. Reconstrucción `hybrid`

Para la figura piloto, `preferred_renderer` permanece `hybrid` porque es la decisión canónica existente.

En MVP4A, `hybrid` significa que el consumidor puede combinar representación estructurada y tratamiento visual apropiado, pero **la reconstrucción técnica mínima debe poder producirse desde el JSON estructurado sin depender de IA ni de reinterpretar el PDF**.

Un crop de la fuente puede usarse durante QA para comparación visual. No se convierte automáticamente en dependencia runtime ni en sustituto de las entidades estructuradas.

## 13. Schema y validación

El schema debe ampliar `figure.schema.json` sin invalidar las figuras existentes solo por no tener `render_contract`.

Cuando `reconstruction.render_contract == normalized-2d-v1`, la validación debe fallar si ocurre cualquiera de estos casos:

- `camera.coordinate_space` no es `normalized_figure`;
- viewport ausente o distinto del espacio normalizado definido;
- `layers` vacío;
- entidad referenciada por layer inexistente;
- anotación referenciada por layer inexistente;
- primitive no permitida;
- geometry sin coordenadas requeridas por su primitive;
- coordenadas fuera de `[0,1]`;
- `rect` con ancho/alto no positivos;
- `line` con cantidad de puntos distinta de dos;
- `polyline` con menos de dos puntos;
- anotación visible sin `placement`;
- `placement` fuera de `[0,1]`;
- duplicación de IDs de anotación;
- referencias `entity_id` / `measurement_id` rotas respecto a la figura o al Knowledge canónico.

La validación automática no certifica que una coordenada sea visualmente correcta; eso requiere comparación con la fuente.

## 14. Compatibilidad y migración

MVP4A es incremental:

- no migra todas las figuras;
- no obliga a que todas las figuras determinísticas sean inmediatamente `render-ready`;
- no cambia IDs existentes;
- no cambia la procedencia;
- no elimina campos actuales;
- no cambia el significado de `precision`;
- no duplica la figura en otra carpeta/modelo.

Las figuras sin `render_contract` siguen siendo Knowledge válido pero no render-ready.

Cualquier futura `normalized-2d-v2` requerirá una decisión explícita; MVP4A no diseña esa versión por adelantado.

## 15. Distribución BOOK

La prueba de MVP4A no se hará contra `dist/pilot` como sustituto del release real.

El gate de cierre debe ejecutar el builder BOOK canónico para `cpnc-2025` y comprobar en el `figures.bundle.json` generado que:

- Knowledge sigue siendo `1.0.0` salvo que un cambio de versión sea decidido explícitamente por release policy;
- existe `FIG-CPNC-2025-P0113-001`;
- conserva sus IDs/fuentes actuales;
- declara `render_contract = normalized-2d-v1`;
- conserva toda la geometría/placement/layers necesarios;
- las referencias siguen resolviendo después de serializar/distribuir.

No se declarará MVP4A cerrado basándose solo en el JSON fuente o en el `dist/pilot` histórico.

## 16. QA visual

Debe existir una reconstrucción de referencia generada únicamente desde el contrato estructurado del piloto.

Se compara contra la región fuente de la página 113 para verificar, como mínimo:

- corredera reconocible como corredera telescópica;
- cajón y laterales conservan su relación espacial esencial;
- el área/sección que explica la holgura es comprensible;
- las tres notas de holgura se asocian correctamente;
- ninguna entidad cambia de significado;
- ninguna coordenada `approximate` se presenta como `exact`.

La aceptación es de fidelidad **técnica/pedagógica**, no de clonación pixel-perfect.

Si la comparación revela que la geometría estructurada no basta, el MVP4A permanece abierto; no se tapa el hueco con una imagen generada o geometría inventada.

## 17. Tests mínimos de aceptación

MVP4A debe demostrar:

1. schema actual sigue aceptando una figura legacy sin `render_contract`;
2. figura `normalized-2d-v1` válida pasa;
3. cada clase de fallo enumerada en la sección 13 falla cerrada;
4. la figura piloto real pasa schema/validación;
5. `figure_id`, `page_id`, fuente, relaciones, measurement IDs y annotation links siguen intactos;
6. builder BOOK real produce `figures.bundle.json` con el contrato intacto;
7. serialización repetida del mismo Knowledge produce el mismo resultado lógico/determinístico;
8. revisión visual del piloto queda registrada con evidencia y no sustituida por una afirmación textual.

## 18. Criterio de cierre

MVP4A puede declararse cerrado solamente si existe evidencia de extremo a extremo:

```text
fuente PDF 113
→ FigureSpec canónico enriquecido
→ schema + validación fail-closed
→ builder BOOK
→ figures.bundle.json
→ reconstrucción de referencia desde JSON
→ comparación visual aprobada
```

Token de aceptación recomendado:

`CARPINOVA_KNOWLEDGE_MVP4A_RENDERABLE_FIGURE_PASS`

## 19. Qué habilita después

Solo después de cerrar MVP4A puede abrirse MVP4B en `CarpiNova-PC` para:

- cargar `figures.bundle.json`;
- crear `figures` / `figuresById`;
- resolver `figure_ids` de la lección;
- renderizar `normalized-2d-v1` con un componente pequeño, preferentemente SVG nativo;
- mostrar la figura dentro de la lección X/2X.

Las interacciones continúan fuera de MVP4B inicial. Primero se prueba una figura correcta y estática; después se decide si vale la pena generalizar.

## 20. Ley anti-ruido aplicada

MVP4A debe terminar con menos incertidumbre, no con más infraestructura.

Decisión:

```text
REUSE existing FigureSpec fields
→ add one opt-in render contract marker
→ enrich one real figure
→ validate it
→ distribute it
→ visually prove it
```

No decisión:

```text
new figure engine
new scene graph framework
renderer registry
all-figure migration
3D
WebGL
AI reconstruction
PC implementation
Cell implementation
```
