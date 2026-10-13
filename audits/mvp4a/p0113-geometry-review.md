# MVP4A P0113 Geometry Review

Fecha: 2026-10-13

Estado: **SOURCE_GATE_RESOLVED — GEOMETRY REVIEW COMPLETE**

## Fuente canónica verificada

Archivo adjuntado directamente al runtime:

```text
libros_1751553390342_Carpintería para no Carpinteros Versión 2025(2).pdf
```

Verificación independiente sobre bytes reales:

```text
size = 339051027 bytes
SHA-256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
page_count = 295
```

Coincide exactamente con la identidad de fuente fijada por Knowledge 1.0.0.

Página inspeccionada:

```text
physical/pdf page = 113
printed page = 91
```

La página muestra la sección `Rieles o correderas para muebles`, el render grande de una corredera telescópica, el inset superior izquierdo de sección cajón/mueble y las notas manuscritas de holgura 1.3/1.4/1.5 cm por riel.

Resultado del gate:

```text
MVP4A_TASK3_SOURCE_GATE = PASS
```

## Marco geométrico

Se conserva el FigureSpec canónico:

```text
figure_id = FIG-CPNC-2025-P0113-001
page_id = PAGE-CPNC-2025-P0113
source.region = x 0.0605 / y 0.577 / width 0.88 / height 0.3815
```

Todas las coordenadas siguientes son locales a ese `source.region`, normalizadas en `0.0..1.0`:

```text
(0,0) = esquina superior izquierda del crop de figura
x aumenta hacia la derecha
y aumenta hacia abajo
```

El crop de QA renderizado desde la fuente exacta se inspeccionó a alta resolución. Las coordenadas son deliberadamente `approximate`; sirven para reconstrucción/composición visual y NO convierten posiciones gráficas en cotas técnicas.

## Entidades revisadas

### `telescopic-slide`

Evidencia visible:
la corredera telescópica domina el cuerpo central del crop, en perspectiva desde la parte inferior izquierda hacia la superior derecha.

Primitive:
`polyline`

Precision:
`approximate`

Puntos normalizados de silueta simplificada:

```json
[
  {"x": 0.106, "y": 0.399},
  {"x": 0.826, "y": 0.168},
  {"x": 0.904, "y": 0.202},
  {"x": 0.894, "y": 0.282},
  {"x": 0.246, "y": 0.668},
  {"x": 0.109, "y": 0.651},
  {"x": 0.106, "y": 0.399}
]
```

Razón:
el contorno exterior general es directamente visible. No se codifican perforaciones, rieles internos ni radios como geometría exacta porque las primitivas MVP4A son intencionalmente mínimas.

### `drawer`

Evidencia visible:
rectángulo gris central dentro del inset superior izquierdo, rotulado como `Exterior del cajón`.

Primitive:
`rect`

Precision:
`approximate`

Bounds:

```json
{"x": 0.059, "y": 0.119, "width": 0.207, "height": 0.090}
```

Razón:
los límites exteriores del cajón son visibles en el inset, pero el corte central quebrado hace que la forma completa sea una simplificación.

### `cabinet-left`

Evidencia visible:
lateral vertical izquierdo del mueble en el inset.

Primitive:
`rect`

Precision:
`approximate`

Bounds:

```json
{"x": 0.022, "y": 0.119, "width": 0.034, "height": 0.105}
```

### `cabinet-right`

Evidencia visible:
lateral vertical derecho del mueble en el inset.

Primitive:
`rect`

Precision:
`approximate`

Bounds:

```json
{"x": 0.286, "y": 0.118, "width": 0.032, "height": 0.105}
```

### `cross-section`

Evidencia visible:
recuadro/inset superior izquierdo que agrupa cajón, laterales y las referencias `Interior del mueble` / `Exterior del cajón`.

Primitive:
`rect`

Precision:
`unknown`

Bounds de ubicación/composición:

```json
{"x": 0.000, "y": 0.025, "width": 0.345, "height": 0.255}
```

Razón:
la posición del inset sí es visible y puede componerse; se conserva `precision = unknown` porque el FigureSpec histórico no demuestra geometría técnica interna suficiente para elevar su precisión.

## Anotaciones revisadas

Se asignan IDs estables solo porque serán miembros de `layers`.

### `ann-clearance-light`

Texto:
`Riel liviano 1.3cm por riel`

Measurement:
`MEAS-CPNC-2025-P0113-009`

Placement:

```json
{"x": 0.405, "y": 0.620, "precision": "approximate"}
```

### `ann-clearance-heavy`

Texto:
`Riel pesado 1.4cm por riel`

Measurement:
`MEAS-CPNC-2025-P0113-010`

Placement:

```json
{"x": 0.405, "y": 0.675, "precision": "approximate"}
```

### `ann-clearance-soft-close`

Texto:
`Riel push o cierre suave 1.5cm por riel`

Measurement:
`MEAS-CPNC-2025-P0113-011`

Placement:

```json
{"x": 0.405, "y": 0.728, "precision": "approximate"}
```

### `ann-interior-cabinet`

Texto:
`Interior del mueble`

Entity:
`cross-section`

Placement:

```json
{"x": 0.104, "y": 0.061, "precision": "approximate"}
```

### `ann-exterior-drawer`

Texto:
`Exterior del cajón`

Entity:
`cross-section`

Placement:

```json
{"x": 0.105, "y": 0.101, "precision": "approximate"}
```

## Layers propuestos

### `layer-cross-section` — order 0

```text
entities:
- cross-section
- drawer
- cabinet-left
- cabinet-right

annotations:
- ann-interior-cabinet
- ann-exterior-drawer
```

### `layer-slide` — order 1

```text
entities:
- telescopic-slide
```

### `layer-clearance-notes` — order 2

```text
annotations:
- ann-clearance-light
- ann-clearance-heavy
- ann-clearance-soft-close
```

## Camera

El contrato usa el viewport normalizado completo:

```json
{
  "coordinate_space": "normalized_figure",
  "viewport": {"x": 0, "y": 0, "width": 1, "height": 1}
}
```

## Medidas canónicas preservadas

Se verificó que `measurements.json` conserva:

```text
MEAS-CPNC-2025-P0113-009 = 13 mm, VISUALLY_VERIFIED
MEAS-CPNC-2025-P0113-010 = 14 mm, VISUALLY_VERIFIED
MEAS-CPNC-2025-P0113-011 = 15 mm, VISUALLY_VERIFIED
```

MVP4A no cambia sus valores, IDs ni autoridad.

## Guardrails de no invención

Este review NO afirma:

- medidas físicas derivadas desde coordenadas gráficas;
- radios/espesores exactos de la corredera;
- posición exacta de perforaciones;
- proporciones mecánicas exactas;
- geometría interna exacta del cross-section.

Los valores de posición son reconstrucción visual aproximada sustentada en el crop de la fuente exacta.

## Resultado

```text
SOURCE_GATE = PASS
GEOMETRY_REVIEW = COMPLETE
CANONICAL_FIGURE_MUTATION = AUTHORIZED_FOR_TASK3_GREEN
```
