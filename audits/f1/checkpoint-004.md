# F1 Checkpoint 004 — reanudación segura

**Corte:** después de `BATCH-011`, antes de iniciar la sección `Mi historia, la de una empresa`.

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama: `feat/knowledge-f1`
- Último commit funcional antes de este checkpoint: `22584c55f47cd481d49faf5ec717d78e90b27ce5`
- Último lote cerrado: `BATCH-011`
- Knowledge QA run: `38013626591`
- CI: **GREEN**
  - tests: success
  - Ruff: success
  - validate repository: success
  - F0 pilot acceptance: success

## Cobertura

- Páginas físicas canónicas: 295
- Páginas completas: 53
- Páginas pendientes: 242
- Duplicados entre lotes: 0
- F1 secuencial completado hasta PDF física 45
- Piloto F0 permanece en PDF físicas 110–117

## Lotes cerrados desde el checkpoint anterior

- `BATCH-010`: GO — PDF 36–41 / impresas 14–19 — `Nueva comunidad de carpinteros`.
- `BATCH-011`: GO — PDF 42–45 / impresas 20–23 — `Un nuevo comienzo`.

### Hallazgos relevantes de BATCH-010

- Se preservan diseño/despiece y servicios de mecanizado ofrecidos por proveedores: perforaciones de bisagras, chaflanes, narices, curvas, vaciados y circunferencias.
- Se preservan referencias a minifix y tarugos sin convertirlas en reglas ejecutables.
- Se preserva la recomendación del autor de seleccionar tablero según ambiente y distinguir estándar/RH y otras variantes, sin promoverla a `VALIDATED`.
- p41 contiene FigureSpec de la historieta `NUEVA COMUNIDAD DE CARPINTEROS`.
- La fuente contiene cifras históricas del programa que difieren entre páginas. Se conserva cada cifra como declaración del autor con su página de procedencia; no se reconcilia silenciosamente.

### Hallazgos relevantes de BATCH-011

- Se preserva la transición de talleres presenciales a formación remota durante la pandemia.
- p43 conserva un ejemplo explícito de error de medición de cinco centímetros.
- Se preservan referencias a Zoom, Meet, grupos de WhatsApp, diseño/venta de escritorios y venta de herramientas como parte de la historia del programa.
- p44 menciona oportunidades alrededor del gremio: software de diseño, apps de despiece y herramientas para gestionar costos.
- p45 contiene FigureSpec de `UN NUEVO COMIENZO`, con instructor remoto, videollamada y estudiantes practicando.

## Siguiente punto exacto de reanudación

- Próxima página física pendiente: **PDF 46 / impresa 24**.
- Encabezado confirmado visualmente: **MI HISTORIA, LA DE UNA EMPRESA**.
- PDF 46–47 ya fueron vistos de forma preliminar y contienen relato biográfico/empresarial; todavía NO forman un lote publicado.
- No fijar el final de `BATCH-012` por anticipado: inspeccionar al menos PDF 46–51 y cortar por límite temático/densidad real.
- El índice sitúa `La evolución de la carpintería` en la impresa 34, pero la frontera debe confirmarse visualmente antes de crear lotes.

## Orden al reanudar

1. Verificar el HEAD de `feat/knowledge-f1` y que descienda de este checkpoint.
2. Inspeccionar visualmente PDF 46–51 y determinar un corte KISS de 3–8 páginas.
3. Extraer por página: `source_transcription`, `normalized_text`, `learning_text`, inventario visual y FigureSpec solo donde aporte semántica reutilizable.
4. Mantener reglas/medidas como candidatas o vacías; no promover automáticamente a autoridad ejecutable.
5. Actualizar `report-batch` test y cobertura en el mismo commit del lote.
6. Publicar por fast-forward con lease y esperar CI GREEN.

## Reglas KISS vigentes

- Extraer el libro es el objetivo; no crear arquitectura que no sea necesaria.
- Utilidades suficientes: `report-batch` y `report-coverage`.
- Sin planner, WaveSpec, CoverageSpec persistido, motor de consolidación ni releases parciales obligatorias.
- `pdf_pages` es identidad estable de lote.
- FigureSpec únicamente para visuales reutilizables.
- No corregir ni reconciliar silenciosamente contradicciones del libro.
- No convertir recomendaciones del autor en reglas ejecutables sin validación posterior.
- No declarar lote terminado sin CI GREEN.

**Decisión:** continuar desde PDF 46 con la misma metodología KISS.