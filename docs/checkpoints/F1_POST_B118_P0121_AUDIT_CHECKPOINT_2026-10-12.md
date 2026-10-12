# F1 POST-B118 / P0121 AUDIT CHECKPOINT — 2026-10-12

## Estado canónico al detener

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama canónica F1: `feat/knowledge-f1`
- HEAD verificado: `de7b034db6a3f70485cad1ae3a3688f0ec4c3440`
- Tree verificado: `d604d198e1d900dba7d4c62e21b51a5df9a87727`
- Commit: `Merge pull request #15 from sierraglobalcompany-rgb/feat/knowledge-f1-b118` / `Batch 118: complete exact-source F1 coverage`
- Este checkpoint NO modifica `feat/knowledge-f1` ni `main`.

## Punto de reanudación

Antes de cualquier mutación nueva:

1. Volver a leer `feat/knowledge-f1` y confirmar que sigue en `de7b034db6a3f70485cad1ae3a3688f0ec4c3440`; si cambió, auditar drift antes de continuar.
2. No interpretar `continua` como autorización de merge/promoción.
3. No tocar `main` sin autorización humana explícita.
4. Mantener `UNRESOLVED > INVENTED`, `content.json` canónico y separación source / normalized / learning.

## P0121 — auditoría visual recién recuperada

La página exacta 2025 `PDF 121 / impresa 99` fue leída con render visual directo desde el archivo fuente. La imagen muestra:

- continuación textual de la sección;
- `Medidas para Instalación`;
- grupo `Brazo Grande` con varios esquemas y una pequeña tabla;
- grupo `Brazo mini`;
- `Plano técnico` horizontal con cotas;
- `Instrucciones de instalación` y secuencia inferior de montaje.

El contenido canónico existente de P0121 ya conserva correctamente que las cotas pequeñas no deben inventarse y que requieren revisión de alta resolución antes de convertirse en `measurements` o instrucciones automáticas.

### Evidencia canónica existente

- `books/cpnc-2025/pages/p0121/content.json` mantiene dos bloques y marca la necesidad de revisión alta resolución.
- `books/cpnc-2025/pages/p0121/visual-inventory.json` identifica un visual técnico significativo.
- `books/cpnc-2025/pages/p0121/figures/fig-001.json` tiene `review.status = HIGH_RES_REQUIRED_FOR_DIMENSIONS`, `small_dimension_labels_resolved = false` y `measurements = []`.

### Estado P0121 al checkpoint

`P0121-HIGH-RES` sigue ABIERTO para la auditoría dimensional perfecta. La inspección visual confirmó la estructura y que sí existen cotas numéricas pequeñas, pero no se deben transcribir todavía sin una lectura suficientemente confiable de cada valor.

Intento de materializar solo la página 121 falló porque el backend intentó materializar el PDF completo de ~339 MB y superó el límite de 100 MB. No se debe usar ese fallo como excusa para inferir cotas.

## Próxima acción exacta

Continuar desde P0121 con una estrategia de inspección de alta resolución que no invente dimensiones. Si los valores pequeños pueden leerse de forma inequívoca desde la fuente exacta, registrar únicamente esos valores verificados en los artefactos canónicos correspondientes y ejecutar tests/validator/CI. Si no pueden leerse con certeza, conservar `HIGH_RES_REQUIRED_FOR_DIMENSIONS` abierto.

No abrir scope adicional, no hacer branch cleanup, no borrar provenance y no promover/mergear nada sin gate humano explícito.
