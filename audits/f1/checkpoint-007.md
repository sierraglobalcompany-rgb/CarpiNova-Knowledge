# F1 Checkpoint 007 — reanudación segura

**Corte:** después de `BATCH-016`, antes de continuar `Mi primer Ensamble` desde PDF 68.

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama: `feat/knowledge-f1`
- Último commit funcional: `c0493e13bc129b833c00bd8f545be2abc0ad16d2`
- Último lote cerrado: `BATCH-016`
- Knowledge QA run: `38016229023`
- CI: **GREEN**
  - tests: success
  - Ruff: success
  - validate repository: success
  - F0 pilot acceptance: success

## Cobertura

- Total físico canónico: 295
- Completas: 75
- Pendientes: 220
- Duplicados entre lotes: 0
- F1 secuencial completado hasta PDF física 67

## BATCH-016 — PDF 62–67 / impresas 40–45

Bloque `Mi primer Ensamble` — primera parte de la mesa de noche de práctica.

### p62
- Introducción al primer ensamble.
- Videos de apoyo para prensado, guía de marcación, avellanador, taladro, bisagras y rieles.
- QR preservado como referencia, sin ingestión automática.

### p63
- Mesa de noche en tablero aglomerado laminado de 15 mm.
- Gaveta superior con corredera telescópica y puerta batiente inferior.
- Dos correas traseras de amarre.
- Sistema “T” invertida / gola.
- Herramientas listadas por fuente.
- Medidas impresas del módulo: 40×40×32 cm; ejes no inferidos.
- Consumo aproximado: 1/4 de tablero.
- QR comercial para Colombia decodificado como `https://wa.me/573154667314`; conservado solo como referencia.

### p64
- Tabla completa de despiece y tapacantos.
- Herrajes: corredera telescópica 30 cm, par de bisagras parche 35 mm y tornillería.
- 23 MeasurementSpecs visualmente verificados.
- FigureSpec determinista de referencia 3D + tabla.
- **Conflicto preservado:** p64 registra `BASE Cant=2`; p65 registra `BASE Cant=1`.

### p65
- Paso 1: base + dos laterales.
- Base 400×320 mm; laterales 370×320 mm.
- Fuente indica dos tornillos de 1½ pulgada por lado, cuatro en total.
- Tapacantos orientados hacia el frente.
- Reglas candidatas, no ejecutables.

### p66
- Paso 2: dos correas traseras de 370×70 mm.
- Función declarada: amarrar módulo, dar escuadra y estabilidad.
- Dos tornillos de 1½ pulgada por extremo; cuatro por correa.
- Fuente indica tornillos a 1,5 cm de los bordes.
- Reglas candidatas, no ejecutables.

### p67
- Paso 3: instalación inicial de corredera telescópica de 30 cm.
- Línea/base a 10 cm desde la parte superior (figura: 100 mm).
- Primer tornillo a 37 mm desde el borde frontal.
- Fuente escribe siguientes tornillos a 64 mm y simultáneamente denomina el patrón `sistema 37 y 32`.
- **Conflicto preservado:** 64 mm ↔ denominación 37/32. No se corrige ni se promueve a regla ejecutable.

## Reglas KISS vigentes

- Extraer primero; validar técnicamente después.
- `VISUALLY_VERIFIED` significa que la fuente fue leída/confirmada, no que la afirmación técnica sea universalmente correcta.
- Reglas derivadas de instrucciones del libro permanecen `CANDIDATE`.
- Conflictos internos de la fuente se preservan y se hacen visibles.
- FigureSpec técnico debe ser determinista y no generativo cuando hay cotas/geometría.
- No declarar un lote terminado sin CI GREEN.

## Siguiente punto exacto

- Próxima página física pendiente: **PDF 68 / impresa 46**.
- Continuar inspeccionando la secuencia `Mi primer Ensamble` y cortar el siguiente lote por límite técnico/temático real.

**Decisión:** continuar desde PDF 68.