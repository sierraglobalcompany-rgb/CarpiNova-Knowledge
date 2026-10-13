# MVP4A P0113 Geometry Review

Fecha: 2026-10-13

Estado: **SOURCE_GATE_UNRESOLVED — NO GEOMETRY MUTATION ALLOWED**

## Objetivo del gate

Antes de derivar coordenadas para `FIG-CPNC-2025-P0113-001`, el plan MVP4A exige demostrar que la inspección visual se realiza sobre la fuente canónica exacta:

```text
PDF = libros_1751553390342_Carpintería para no Carpinteros Versión 2025.pdf
SHA-256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
physical page = 113
```

El release histórico `docs/releases/1.0.0.md` fija además:

```text
source_page_count = 295
```

## Fuente visible disponible en este entorno

Se localizaron dos copias en el Project/Library:

```text
libros_1751553390342_Carpintería para no Carpinteros Versión 2025.pdf
libros_1751553390342_Carpintería para no Carpinteros Versión 2025(1).pdf
```

En ambas, la página accesible como PDF page 113 muestra:

- printed page `91`;
- encabezado de instalación de bisagras;
- sección `Rieles o correderas para muebles`;
- el render grande de una corredera telescópica;
- un inset superior izquierdo de sección cajón/mueble;
- notas manuscritas de holgura para riel liviano, pesado y push/cierre suave.

Esto coincide visualmente con el FigureSpec canónico existente:

```text
figure_id = FIG-CPNC-2025-P0113-001
page_id = PAGE-CPNC-2025-P0113
pdf_page = 113
printed_page = 91
source.region = x 0.0605 / y 0.577 / width 0.88 / height 0.3815
```

## Bloqueo

El lector de Project/Library reporta para ambas copias visibles:

```text
total_pages = 294
```

pero el release canónico histórico fija:

```text
source_page_count = 295
```

Además, las copias visibles no tienen una ruta de bytes autorizada para materialización en el contenedor. El intento de `raw_file` fue rechazado por el sistema de archivos del Project/Library.

Por tanto, en este entorno NO es posible ejecutar un SHA-256 independiente sobre los bytes de la copia visual y demostrar que corresponde exactamente al hash canónico:

```text
318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
```

La coincidencia de nombre + página + contenido visual es evidencia útil, pero NO sustituye el gate criptográfico exigido por el plan.

## Decisión fail-closed

Aplicando:

```text
UNRESOLVED > INVENTED
```

se detiene Task 3 antes de derivar coordenadas.

No se autoriza en este estado:

- asignar `render_contract` a la figura canónica;
- añadir `camera` render-ready;
- añadir geometrías `rect`, `line` o `polyline` a P0113;
- asignar placements a annotations;
- crear layers reales;
- fijar coordenadas normalizadas;
- crear tests de regresión con coordenadas;
- promover `unknown` a `approximate` por inferencia.

## Estado de la figura

`books/cpnc-2025/pages/p0113/figures/fig-001.json` permanece sin modificación durante este gate.

Sus entidades continúan con el estado histórico:

- `telescopic-slide` — `approximate`, sin primitive/coordinates;
- `drawer` — `approximate`, sin primitive/coordinates;
- `cabinet-left` — `approximate`, sin primitive/coordinates;
- `cabinet-right` — `approximate`, sin primitive/coordinates;
- `cross-section` — `unknown`, sin primitive/coordinates;
- `layers = []`;
- `camera = {}`;
- no `render_contract` todavía.

## Qué desbloquea Task 3

Hace falta una de estas dos evidencias:

1. disponer en el runtime de los bytes del PDF fuente exacto y calcular:

```text
SHA-256 = 318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c
```

O:

2. una fuente de almacenamiento autorizada que entregue los bytes y permita verificar el mismo hash antes de inspeccionar/derivar coordenadas.

Una vez satisfecho ese gate, la revisión debe registrar por cada entity/annotation:

```text
id
source evidence observed
primitive
normalized coordinates
precision
reason the value is demonstrable from source
```

solo entonces se permite continuar con RED/GREEN de `tests/test_mvp4a_figure.py` y la mutación de `fig-001.json`.

## Resultado

```text
MVP4A_TASK3_SOURCE_GATE = UNRESOLVED
GEOMETRY_MUTATION = BLOCKED
CANONICAL_FIGURE_CHANGED = NO
```
