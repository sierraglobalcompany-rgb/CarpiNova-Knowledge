# MVP4A P0113 Render Review

Fecha: 2026-10-13

Estado: **VISUAL QA — PASS**

## Alcance

Aceptación visual de la reconstrucción determinística de:

`FIG-CPNC-2025-P0113-001`

contra la fuente canónica exacta, sin evaluar todavía release BOOK ni consumo en CarpiNova-PC.

## Fuente canónica

```text
book_id = cpnc-2025
PDF page = 113
printed page = 91
SHA-256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
page_count = 295
source.region = x 0.0605 / y 0.577 / width 0.88 / height 0.3815
```

La fuente muestra una corredera telescópica abierta, un inset de sección cajón/mueble y las notas de holgura 1.3 / 1.4 / 1.5 cm por riel.

## HEAD evaluado

```text
bcdee340b8fc17a0eea18412f8da5a12b79ce1c6
```

Renderer:

`src/carpinova_knowledge/render_figure.py`

FigureSpec:

`books/cpnc-2025/pages/p0113/figures/fig-001.json`

## SVG fresco

Se regeneró el SVG desde el FigureSpec y renderer de ese HEAD exacto.

```text
svg_bytes = 2309
SHA-256 = 7aaed9b446f0192e5eea1aaae22a29403b1275e11e96ffbcf3e134d99c825e43
```

Este hash cambia respecto al SVG previo porque Task 3 fue corregido después del primer visual gate FAIL.

## Criterios de aceptación

### 1. Corredera reconocible como telescópica

**PASS**

La reconstrucción ya no es una única silueta genérica. Conserva:

- contorno exterior principal;
- `slide-middle-profile`;
- `slide-inner-profile`.

Los tres cuerpos longitudinales superpuestos son suficientes para comunicar visualmente una corredera telescópica esquemática.

No se exige reproducir perforaciones, radios ni herrajes internos para este contrato MVP4A.

### 2. Perfiles internos distinguibles

**PASS**

Los dos perfiles internos están separados visualmente del contorno exterior y mantienen la dirección/perspectiva principal de la fuente.

Sus coordenadas continúan declaradas como `approximate`.

### 3. Relación cajón / laterales / rieles del inset

**PASS**

El inset conserva:

- cajón central;
- lateral izquierdo;
- lateral derecho;
- `slide-section-left`;
- `slide-section-right`;
- labels `Interior del mueble` y `Exterior del cajón`.

Las dos pequeñas secciones de riel aparecen entre el cajón y los laterales, que es el concepto técnico necesario para comprender la holgura lateral.

### 4. Holgura lateral comprensible

**PASS**

La separación lateral ya no está representada únicamente por vacío entre rectángulos: contiene una sección de riel a cada lado.

El render no presenta ese ancho como medida exacta; la geometría permanece `approximate`.

### 5. Notas 13 / 14 / 15 mm contextualizadas

**PASS**

Los textos visibles son:

```text
Riel liviano 1.3cm por riel
Riel pesado 1.4cm por riel
Riel push o cierre suave 1.5cm por riel
```

Se mantienen debajo de la corredera, coherentes con la disposición de la fuente, y el FigureSpec los vincula explícitamente a:

`entity_id = telescopic-slide`

Los `measurement_id` canónicos siguen siendo:

```text
MEAS-CPNC-2025-P0113-009 = 13 mm
MEAS-CPNC-2025-P0113-010 = 14 mm
MEAS-CPNC-2025-P0113-011 = 15 mm
```

MVP4A no cambia su autoridad técnica.

### 6. Sin semantic drift

**PASS**

La entidad principal sigue comunicando `drawer_slide / telescopic-slide`; los perfiles agregados refuerzan esa identidad en vez de cambiarla.

El inset comunica ubicación lateral del riel respecto al cajón y mueble.

### 7. Approximate no presentado como exact

**PASS**

No se dibujan cotas geométricas exactas derivadas de posiciones normalizadas.

Las geometrías visibles nuevas permanecen `precision = approximate`; `cross-section` continúa `precision = unknown`.

### 8. Sin detalle inventado necesario para el significado

**PASS**

No se añadieron:

- perforaciones inventadas;
- rodamientos;
- tornillos;
- radios;
- espesores mecánicos exactos;
- dimensiones no presentes en MeasurementSpec.

La reconstrucción usa únicamente los cues mínimos demostrables desde la fuente.

## Diferencia aceptada respecto a la fuente

La fuente es un render técnico con sombreado y detalle mecánico. El SVG es deliberadamente una reconstrucción lineal mínima para QA del contrato `normalized-2d-v1`.

El objetivo de MVP4A no es fotorealismo ni equivalencia pixel a pixel; es preservar significado técnico suficiente desde datos estructurados determinísticos.

Con la corrección de Task 3, ese umbral mínimo se cumple.

## Resultado

```text
SOURCE_IDENTITY = PASS
FRESH_RENDER = PASS
TELESCOPIC_IDENTITY = PASS
CLEARANCE_SECTION = PASS
MEASUREMENT_CONTEXT = PASS
SEMANTIC_DRIFT = NONE MATERIAL
PRECISION_GUARDRAIL = PASS
INVENTED_DETAIL = NONE REQUIRED
MVP4A_TASK5_VISUAL_GATE = PASS
```

Task 5 queda autorizado para cierre después de CI del commit documental.

No autoriza todavía Task 6, merge ni release.