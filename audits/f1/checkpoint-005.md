# F1 Checkpoint 005 — reanudación segura

**Corte:** después de `BATCH-013`, antes de iniciar `La evolución de la carpintería`.

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama: `feat/knowledge-f1`
- Último commit funcional antes de este checkpoint: `803296d4981e05540f314fad7886af0bb3094bb0`
- Último lote cerrado: `BATCH-013`
- Knowledge QA run: `38014377501`
- CI: **GREEN**
  - tests: success
  - Ruff: success
  - validate repository: success
  - F0 pilot acceptance: success

## Cobertura

- Páginas físicas canónicas según report-coverage: 295
- Páginas completas: 63
- Páginas pendientes: 232
- Duplicados entre lotes: 0
- F1 secuencial completado hasta PDF física 55
- Piloto F0 permanece en PDF físicas 110–117

## Lotes cerrados desde el checkpoint anterior

- `BATCH-012`: GO — PDF 46–51 / impresas 24–29 — primera parte de `Mi historia, la de una empresa`.
- `BATCH-013`: GO — PDF 52–55 / impresas 30–33 — cierre de la historia empresarial + definición de carpintería.

## Hallazgos relevantes de BATCH-012

- Se preserva el paso desde pequeños negocios y estampación textil hacia importaciones y DITECNO.
- Se conserva la transición soportes de TV → instalación → repisas → mobiliario completo.
- Se registran explícitamente material, proveedor, despiece, ensamble e instalación como decisiones que aparecen al aumentar la complejidad del mueble.
- Las cifras comerciales y de capacidad se conservan como declaraciones del autor, no como parámetros ejecutables.

## Hallazgos relevantes de BATCH-013

- Se preserva la distinción entre aprendizaje empírico e informalidad.
- p53 contiene FigureSpec de cuatro hitos de la historia del autor.
- p54 define carpintería en sentido amplio y presenta el enfoque del libro en carpintería moderna y funcional.
- La afirmación de que el tablero aglomerado está compuesto en un 80% por pino y eucalipto se conserva como dato de fuente pendiente de validación; no se promueve a conocimiento técnico autorizado.
- p55 contiene FigureSpec de la definición visual de carpintería.

## Siguiente punto exacto de reanudación

Inspección visual directa del PDF ya realizada:

- PDF 56 / impresa 34: `La evolución de la carpintería` — texto completo.
- PDF 57 / impresa 35: continuación de la misma sección — texto completo.
- PDF 58 / impresa 36: infografía `LA EVOLUCIÓN DE LA CARPINTERÍA` con cuatro paneles: trabajo en madera sólida, montaje y acabado de muebles, uso de tableros preelaborados, eficiencia.
- PDF 59 / impresa 37: separador gráfico de Hágalo en Casa; no aporta contenido técnico reutilizable.
- PDF 60 / impresa 38: página prácticamente en blanco.
- PDF 61 / impresa 39: portada de sección `Mi primer Ensamble`.

### Decisión de corte

- `BATCH-014` debe contener **PDF 56–58** únicamente.
- PDF 59–60 deben tratarse después como separador/página vacía y no mezclarse con la sección técnica.
- PDF 61 inicia una nueva sección y queda fuera de BATCH-014.

## Contenido técnico visible en p56–57

- La carpintería tradicional parte del árbol y pasa por tala, descortezado, desorillado, selección, corte en tablas/tablones/listones y secado.
- Después se cantea y cepilla, se realizan uniones o “pegas”, se fabrican piezas y se aplican lijado, protección y acabados.
- El autor plantea la evolución hacia materiales preelaborados por razones de eficiencia, precisión, tiempo y costo.
- Enumera tres familias: aglomerado, alistonado y contrachapado.
- Defiende conservar la carpintería tradicional/ebanistería como conocimiento cultural y artesanal.
- Señala nuevos retos con tableros: muebles más compactos, más funciones, nuevos sistemas y herrajes, y mobiliario adaptable.
- Ejemplo: cama que también funciona como escritorio y se pliega contra la pared.
- La fuente contrasta viviendas antiguas de 80–120 m² con viviendas actuales de 15–45 m². Estas cifras se preservan como afirmaciones del autor y no se convierten automáticamente en estándar dimensional.

## Orden al reanudar

1. Verificar que `feat/knowledge-f1` descienda de este checkpoint.
2. Crear `BATCH-014` con PDF 56–58.
3. Extraer p56–57 en bloques conceptuales y de recomendación sin convertirlos en reglas ejecutables.
4. Crear FigureSpec de la infografía de p58.
5. Actualizar test de lote y cobertura a **66/295**, pendientes **229**, si las tres páginas quedan completas.
6. Publicar por fast-forward con lease.
7. Esperar CI GREEN antes de procesar p59–61 y el inicio de `Mi primer Ensamble`.

## Reglas KISS vigentes

- Extraer el libro es el objetivo principal; no crear infraestructura que no sea necesaria.
- `pdf_pages` es la identidad estable del lote.
- FigureSpec solo para visuales con semántica reutilizable.
- No corregir ni reconciliar silenciosamente afirmaciones del libro.
- No promover recomendaciones, cifras o propiedades a `VALIDATED`/`EXECUTABLE` sin fase posterior de validación.
- No declarar un lote terminado sin CI GREEN.

**Decisión:** continuar con `BATCH-014 = PDF 56–58`.