# CarpiNova — Checkpoint B117 RED START — 2026-10-12

## Estado congelado

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama canónica F1: `feat/knowledge-f1`
- HEAD canónico F1: `6703f67a67b5d955bffcf619dae98dad92e2e764`
- `main`: **NO tocado** en esta secuencia.
- Convención autorizada por el usuario: cuando diga `continua`, acepta los merges recurrentes hacia `feat/knowledge-f1`; esto **no** autoriza mutar `main`.

## BATCH-116 — CERRADO / PROMOVIDO

- PR #13: `Batch 116: recover exact-source page 202`
- Commit candidato limpio: `559fe99f039729db3e01448c931ee7510ce2300e`
- Merge commit canónico: `6703f67a67b5d955bffcf619dae98dad92e2e764`
- Fuente recuperada: P0202 / impresa 180 — sección `Clósets`.
- Cobertura canónica esperada tras B116: `292 / 295`.
- Pendientes: `[207, 213, 223]`.
- Duplicados: `[]`.
- CI candidato B116 `38207153788`: GREEN.
  - `184 passed`
  - Ruff PASS
  - repository validator: `valid=true`, `error_count=0`
  - F0 pilot: `GO`
- CI canónico post-merge B116 `38207367007`: GREEN.
  - `184 passed`
  - Ruff PASS
  - repository validator: `valid=true`, `error_count=0`
  - F0 pilot: `GO`

## Incidencia B116 ya resuelta

El primer candidato B116 (`48f3d092...`) falló el validator porque `normalized.md` y `learning.md` usaban títulos manuales `Normalized content` / `Learning content`, mientras el renderer canónico exige `Normalized text` / `Learning text`. Se investigó la causa raíz, se corrigió regenerando conforme a `render_docs.py`, y el candidato corregido `559fe99f...` quedó GREEN. El candidato fallido queda cuarentenado y no fue promovido.

## BATCH-117 — RED INICIADO / IMPLEMENTACIÓN NO INICIADA

- Objetivo: recuperar P0207 del PDF 2025 exacto.
- Mapeo esperado: PDF P0207 -> impresa 185.
- Rama RED: `feat/knowledge-f1-b117-red`
- Commit RED: `d654e56b38116e8e2b7a4e6c627c0ddd8daa66d0`
- Archivo RED añadido: `tests/test_batch_117.py`
- CI RED iniciado: run `38207700546`.
- Al crear este checkpoint, el run RED acababa de ser encolado/iniciado; **no se ha usado su resultado para implementar nada**.
- No existe aún implementación B117 ni PR B117.

## Especificación RED B117 congelada

La prueba RED exige para P0207:

- sección `Puertas`;
- puertas estándar instaladas a escuadra;
- vano ideal `80 cm x 210 cm`;
- referencia de accesibilidad para silla de ruedas;
- medir altura del vano a izquierda y derecha;
- medir ancho en tres puntos: superior, medio e inferior;
- tomar la medida menor y restar `1 cm` de tolerancia;
- diferencias muro/madera cubiertas con tapaluz o molduras;
- `4` measurements esperadas: `80 cm`, `210 cm`, `3 count`, `1 cm`;
- `VISUALLY_VERIFIED`;
- sin figura técnica significativa;
- `source-gap-p0207.md` RESOLVED;
- cobertura esperada tras GREEN/promoción: `293 / 295`;
- pendientes posteriores esperados: `[213, 223]`;
- duplicados: `[]`.

## Guardrails activos

- `content.json` es canónico; Markdown derivado debe coincidir exactamente con el renderer.
- `UNRESOLVED > INVENTED`.
- No inferir desde páginas adyacentes ni otras ediciones.
- `VISUALLY_VERIFIED` solo con inspección visual real de la página exacta.
- Visual técnico significativo => FigureSpec o exclusión explícita.
- No borrar archivos históricos `source-gap`; resolverlos conservando trazabilidad.
- No merge a `main`, release, deploy ni limpieza destructiva sin autorización específica.
- Sin force push ni reescritura destructiva de historia.

## Punto exacto de reanudación

1. Revisar el resultado de CI RED `38207700546` y confirmar que el fallo sea el esperado.
2. Verificar visualmente P0207 del PDF 2025 exacto antes de crear artefactos.
3. Implementar B117 con TDD mínimo y fidelidad de fuente.
4. Ejecutar CI completo y validator.
5. Crear candidato limpio / PR B117.
6. Si el usuario dice `continua`, queda autorizado el merge recurrente a `feat/knowledge-f1` después de GREEN y auditoría; `main` sigue fuera de alcance.

## Rama de checkpoint

- `checkpoint/b117-red-start-20261012`
- Base congelada: `d654e56b38116e8e2b7a4e6c627c0ddd8daa66d0`
