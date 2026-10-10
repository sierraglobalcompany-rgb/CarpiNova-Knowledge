# F1 Checkpoint 003 — reanudación segura

**Corte:** después de `BATCH-009`, antes de iniciar `BATCH-010`.

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama activa: `feat/knowledge-f1`
- Último commit funcional antes de este checkpoint: `da2275a3a3505253542e5817644201dfe0af95b8`
- Último lote funcional: `BATCH-009`
- Workflow de verificación: `Knowledge QA`, run `38012993027`
- Resultado CI: **GREEN**
  - tests: success
  - Ruff: success
  - validate repository: success
  - F0 pilot acceptance: success

## Cobertura

- Páginas físicas canónicas: 295
- Páginas completas: 43
- Páginas pendientes: 252
- Duplicados entre lotes: 0
- F1 secuencial completado hasta PDF física 35
- Piloto F0 permanece en PDF físicas 110–117

## Lotes cerrados

- `BATCH-000-pilot`: GO
- `BATCH-001`: GO
- `BATCH-002`: GO
- `BATCH-003`: GO
- `BATCH-004`: GO
- `BATCH-005`: GO
- `BATCH-006`: GO
- `BATCH-007`: GO
- `BATCH-008`: GO
- `BATCH-009`: GO

### BATCH-008

- PDF físicas 30–32 / impresas 8–10.
- Tema: `Voy a enseñar a hacer muebles`.
- p30 preserva la transición narrada desde carpintería tradicional hacia tableros aglomerados, selección de tablero según ambiente y relevancia del ensamble.
- p31 preserva el origen narrado del programa Hágalo en Casa.
- p32 contiene FigureSpec de la secuencia histórica de seis paneles.

### BATCH-009

- PDF físicas 33–35 / impresas 11–13.
- Tema: `Aprendiendo y enseñando`.
- p33 conserva levantamiento del espacio, irregularidades, múltiples puntos de medición, tapa luces, formato de visita, diseño, registro firmado y orden de producción con condiciones del inmueble/acceso.
- p34 conserva los dos pilares declarados: registro detallado de medidas + orden de producción completa/técnica; también calidad de instalación, transparencia y aprender a desaprender.
- p35 contiene FigureSpec de seis paneles que resume medición, revisión con cliente, especificaciones, error de instalación, orden de trabajo y aprendizaje.
- No se promovieron recomendaciones del autor a reglas ejecutables ni medidas a `VALIDATED`.

## Siguiente punto exacto de reanudación

### BATCH-010 — aún NO publicado

Inspección visual ya realizada:

- PDF físicas: **36–41**
- Impresas: **14–19**
- Sección: **Nueva comunidad de carpinteros**
- p36–40 son principalmente texto.
- p41 es una infografía/historieta titulada `NUEVA COMUNIDAD DE CARPINTEROS` y debe evaluarse para FigureSpec reutilizable.
- p36 introduce distribuidores, centros de corte, servicios de diseño/despiece, mecanizados y la idea del Mall del Carpintero.
- El tramo continúa con el desarrollo de esa comunidad y la experiencia del autor.
- p42 corresponde al siguiente límite temático esperado (impresa 20 según el índice), por lo que **no debe incluirse en BATCH-010 sin inspección visual previa**.

## Orden al reanudar

1. Verificar que `feat/knowledge-f1` descienda de este checkpoint.
2. Inspeccionar individualmente p36–41 antes de generar contenido canónico.
3. Crear `batch-010.json` con PDF 36–41.
4. Extraer `source_transcription`, `normalized_text` y `learning_text` sin completar huecos con conocimiento externo.
5. Crear FigureSpec únicamente para visuales reutilizables confirmados; p41 es candidato confirmado por inspección inicial.
6. Mantener `measurements.json` y `rules.json` vacíos salvo que la fuente contenga medidas/reglas técnicas concretas; ninguna se promueve automáticamente a VALIDATED/EXECUTABLE.
7. Añadir prueba `BATCH-010 = GO` y actualizar cobertura a **49/295**, pendientes **246**, solo si las seis páginas quedan completas.
8. Publicar en un solo commit por fast-forward con lease.
9. Esperar CI completo GREEN antes del siguiente lote.

## Reglas KISS vigentes

- La prioridad es extraer el libro, no construir infraestructura.
- Utilidades suficientes: `report-batch` y `report-coverage`.
- Sin planner, WaveSpec, CoverageSpec canónico, motor de consolidación ni releases parciales obligatorias.
- `pdf_pages` es la identidad estable de lotes.
- FigureSpec solo cuando el visual aporta semántica reutilizable.
- QR se preserva como destino cuando aplica; no se ingiere automáticamente contenido externo.
- Branding/decoración se inventaría y se excluye con razón documentada.
- Ninguna medida pasa a `VALIDATED` automáticamente.
- Ninguna recomendación del libro se convierte en regla ejecutable de fabricación sin fase posterior de validación.
- No declarar un lote terminado sin CI GREEN.

**Decisión:** continuar F1 con `BATCH-010` usando el mismo flujo KISS.