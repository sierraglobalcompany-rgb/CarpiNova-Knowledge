# CarpiNova — Checkpoint BATCH-110 RED

Fecha: 2026-10-12

## Estado canónico previo

- Rama F1 canónica: `feat/knowledge-f1`.
- HEAD canónico: `b2eb4d1041b842a86c9d35c79524e9d8d06744d7`.
- BATCH-109 ya fue promovido a F1.
- PR #6 figura cerrado/merged.
- CI canónico post-promoción de BATCH-109: run `38197082434`, `SUCCESS`.
- La cobertura contractual vigente tras BATCH-109 es 281/295, 14 páginas pendientes, duplicados `[]`.
- `main` no fue tocada.

## BATCH-110

Objetivo actual: recuperar desde la fuente PDF 2025 exacta las páginas físicas P0172, P0173 y P0174, correspondientes a impresas 150, 151 y 152, sin inferir contenido faltante.

### Estado TDD

- Rama RED: `feat/knowledge-f1-b110-red`.
- Commit RED: `4cd74cd36a0e309be580966e8a24aec8a9626de9`.
- Único cambio funcional del RED hasta este checkpoint: `tests/test_batch_110.py`.
- El test define como contrato de recuperación:
  - lote `batch-110` con 3 páginas;
  - P0172 y P0174 sin contenido textual canónico cuando la página exacta no contiene texto útil;
  - P0173 con contenido explícito que incluye `PASO 4`, `DESPIECE`, `OPTIMIZACIÓN` y `HÁGALO EN CASA`;
  - una FigureSpec significativa en P0173;
  - resolución de los tres `source-gap-p0172.md`, `source-gap-p0173.md`, `source-gap-p0174.md`;
  - cobertura objetivo 284/295, pendientes 11, duplicados `[]`.

### CI RED

- Run: `38197399491`.
- Estado al congelar este checkpoint: **IN PROGRESS**.
- Última observación: el job `qa` estaba ejecutando `Run tests`; no se esperó su conclusión porque el usuario pidió crear checkpoint y detenerse.

## Próxima reanudación exacta

1. Leer nuevamente `feat/knowledge-f1` y confirmar que sigue en `b2eb4d1041b842a86c9d35c79524e9d8d06744d7`; si cambió, detenerse y reconciliar antes de cualquier mutación.
2. Revisar el resultado final del CI RED `38197399491` y confirmar que falla únicamente por la ausencia de BATCH-110 / páginas aún no implementadas y por la cobertura aún en 281/295.
3. No modificar el test para hacerlo pasar salvo que la fuente PDF exacta contradiga el contrato; si lo contradice, corregir primero el test con evidencia exacta.
4. Implementar el GREEN mínimo en una rama limpia derivada del HEAD canónico confirmado, preservando fuente exacta, `UNRESOLVED > INVENTED`, sin cambios de schema/arquitectura/workflows/README/CHANGELOG/cleanup.
5. Regenerar Markdown derivado desde `content.json`, ejecutar suite completa, Ruff, validator y F0 pilot.
6. Auditar diff contra F1; solo después abrir PR draft. No merge sin aprobación explícita del usuario.

## Guardrails

- No tocar `main`.
- No force push.
- No ampliar el scope fuera de P0172-P0174 salvo evidencia estrictamente necesaria y documentada.
- PDF 2025 exacto es autoridad de contenido.
- GitHub vivo + CI vivo son autoridad de estado operacional.
- No asumir que una página sin texto extraíble es una página en blanco: la clasificación debe provenir de inspección visual exacta.
