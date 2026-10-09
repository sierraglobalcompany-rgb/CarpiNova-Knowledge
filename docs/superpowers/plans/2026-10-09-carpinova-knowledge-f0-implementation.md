# CarpiNova Knowledge F0 — Plan ejecutable

**Meta:** construir y validar el primer pipeline reutilizable de CarpiNova Knowledge antes de iniciar la extracción masiva.

## Restricciones globales

- Repositorio canónico privado: `sierraglobalcompany-rgb/CarpiNova-Knowledge`.
- El PDF fuente no se sube a Git.
- Página física y página impresa se modelan por separado.
- JSON es la fuente canónica; Markdown es vista generada.
- Medidas técnicas requieren verificación visual antes de `VISUALLY_VERIFIED` y no alcanzan `VALIDATED` en F0.
- Las reglas permanecen no ejecutables.
- F1 no comienza hasta que el piloto reporte `GO`.

## Tareas

1. Bootstrap del repositorio y CLI.
2. Schemas JSON e IDs canónicos.
3. Auditoría física del PDF y manifiesto SHA-256.
4. Mapa página PDF ↔ página impresa.
5. Índice estructural y taxonomía inicial.
6. Scaffold de lote y Markdown generado.
7. Validador integral del repositorio.
8. Extracción profunda del piloto 88–95 con FigureSpec, medidas, reglas y LessonSpec.
9. Bundles determinísticos para consumidores.
10. Auditoría de aceptación y congelación de Knowledge `0.1.0`.

## Definición de terminado

F0 está terminado cuando el libro tiene auditoría física completa, el mapa de páginas es explícito, el piloto tiene 8 páginas sin ambigüedad, todos los schemas y referencias validan, cada visual significativo tiene FigureSpec, las medidas están trazadas y verificadas visualmente, las reglas no son ejecutables, existe al menos una LessonSpec reutilizable, los bundles son determinísticos y `audits/f0-pilot-acceptance.md` reporta `GO`.
