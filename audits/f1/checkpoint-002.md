# F1 Checkpoint 002 — reanudación segura

**Corte:** después de `BATCH-006`, antes de iniciar `BATCH-007`.

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama activa: `feat/knowledge-f1`
- HEAD confirmado antes de este checkpoint: `2b6ca38b34de2cda48914b8d18ee533a64695233`
- Último commit funcional: `knowledge: complete batch-006 index and support group`
- Workflow de verificación: `Knowledge QA`, run `38011297001`
- Resultado CI: **GREEN**
  - tests: success
  - Ruff: success
  - validate repository: success
  - F0 pilot acceptance: success

## Cobertura F1

- Páginas físicas canónicas: 295
- Páginas completas: 34
- Páginas pendientes: 261
- Duplicados entre lotes: 0
- Cobertura F1 secuencial terminada hasta PDF física 26
- Piloto F0 permanece en físicas 110–117

## Lotes cerrados

- `BATCH-000-pilot`: GO
- `BATCH-001`: GO
- `BATCH-002`: GO
- `BATCH-003`: GO
- `BATCH-004`: GO
- `BATCH-005`: GO
- `BATCH-006`: GO

### BATCH-006

- PDF físicas: 23–26
- Impresas: 1–4
- Propósito: índice + grupo de apoyo
- Página 25 conserva el destino decodificado del QR del grupo de apoyo en WhatsApp.
- Página 25 incluye FigureSpec pedagógico del teléfono/chat/QR.
- Página 26 no contiene conocimiento técnico reutilizable; solo branding/numeración.

## Incidencia de continuidad resuelta

Durante la ejecución anterior se creó un árbol Git parcial de `BATCH-006` que no llegó a commit ni a mover la rama. No hubo corrupción de historia ni fallo del código. La rama seguía en el checkpoint previo. El lote se reconstruyó completo, se creó el commit `2b6ca38...` y se avanzó la rama por fast-forward con lease. CI quedó GREEN.

**Ruling:** no reutilizar árboles huérfanos como autoridad de estado; el estado válido es siempre el HEAD de `feat/knowledge-f1` más CI verde.

## Siguiente punto exacto de reanudación

### BATCH-007 — aún NO publicado

Corte natural ya identificado:

- PDF físicas: **27–29**
- Impresas: **5–7**
- Tema: **Carpintero Digital**
- p27–28 desarrollan el concepto.
- p29 contiene la infografía de cinco pasos:
  1. Medición
  2. Diseño
  3. Selección de materiales
  4. Armado / instalación
  5. Solución
- p29 debe recibir FigureSpec reutilizable porque la secuencia visual aporta semántica.
- p30 inicia un tema nuevo: **“Voy a enseñar a hacer muebles”** y NO debe incluirse en `BATCH-007`.

## Orden de trabajo al reanudar

1. Verificar HEAD actual de `feat/knowledge-f1` y que descienda de este checkpoint.
2. Inspeccionar visualmente p27–29 antes de escribir contenido canónico.
3. Crear `batch-007.json` con físicas 27–29.
4. Extraer/normalizar/learning para p27–29.
5. Crear FigureSpec solo para p29 si la inspección confirma la infografía ya identificada.
6. Añadir prueba `BATCH-007 = GO` y actualizar cobertura a **37/295**, pendientes **258**, siempre que las tres páginas pasen QA.
7. Publicar en un solo commit por fast-forward con lease.
8. Esperar CI completo GREEN antes de comenzar el lote siguiente.
9. Crear nuevo checkpoint después de varios lotes o antes de cualquier cambio de arquitectura.

## Reglas KISS vigentes

- F1 extrae conocimiento; no construir planner, WaveSpec, motor de consolidación ni infraestructura nueva sin necesidad demostrada.
- Utilidades repetitivas suficientes: `report-batch` y `report-coverage`.
- FigureSpec solo para visuales con semántica reutilizable.
- Branding y decoraciones se registran como no significativos, no se modelan innecesariamente.
- QR: conservar destino decodificado; no ingerir automáticamente contenido externo.
- No promover medidas a `VALIDATED` automáticamente.
- No convertir reglas del libro en autoridad ejecutable de fabricación sin fase de validación posterior.
- Mantener RED → GREEN cuando se modifica comportamiento o pruebas.
- No declarar lote terminado sin CI completo GREEN.

**Decisión:** continuar F1 lote por lote desde `BATCH-007`, sin rediseñar la arquitectura.
