# CarpiNova — Checkpoint 2026-10-12

## Estado canónico al pausar

Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`

Rama de integración F1: `feat/knowledge-f1`

HEAD canónico:

`0dccc4840d47c83b748322f5684dfefbeba38feb`

Este SHA corresponde al squash merge del PR #19:

`Add reproducible full-book F1 bundle`

`main` sigue sin tocarse.

## Estado de P1.5 — bundle reproducible

Estado funcional: **MERGED EN feat/knowledge-f1**

PR #19:

- base: `feat/knowledge-f1`
- head final: `70c2c6afca8f96cbac376ff6e65439c6f70c0eec`
- mergeable: true antes del merge
- reviews: 0
- review threads: 0
- merge method: squash
- merge result SHA: `0dccc4840d47c83b748322f5684dfefbeba38feb`

### Lo integrado

- `build_book_distribution()` para bundle completo del libro;
- exactamente 295 páginas canónicas desde `books/cpnc-2025/manifest.json`;
- mismos 4 artefactos derivados:
  - `knowledge.bundle.json`
  - `figures.bundle.json`
  - `lessons.bundle.json`
  - `manifest.json`
- manifest de scope `BOOK`;
- `book_id=cpnc-2025`;
- versión candidata `1.0.0-rc.1`;
- source fingerprint exacto `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`;
- determinismo byte-a-byte probado construyendo dos veces y comparando hashes;
- cero reglas `EXECUTABLE` exigidas por test;
- no rutas locales ni PDF fuente embebido;
- comando CLI reproducible `build-book-dist`;
- test CLI real que genera el bundle completo.

### TDD confirmado

RED builder:

- commit `762520ceae77d8c1d4e1f7a984f1adb2e0bffbd5`
- run `38270776461`
- fallo esperado: `build_book_distribution` inexistente.

GREEN builder:

- commit `a60b24dca3694a284f5e8d67678490b51d315bba`
- run `38270911368`
- resultado: SUCCESS completo.

RED CLI:

- commit `5eb41b0490ceeed8296c64adc6e3281c39030e29`
- run `38272426205`
- 200 tests PASS;
- solo 2 fallos esperados porque `build-book-dist` aún no existía.

GREEN CLI:

- commit `70c2c6afca8f96cbac376ff6e65439c6f70c0eec`
- run `38272908508`
- resultado: SUCCESS completo:
  - tests PASS
  - Ruff PASS
  - repository validator PASS
  - F0 pilot PASS

## CI post-merge P1.5

Run:

`38273481372`

Estado exacto al crear este checkpoint:

`IN_PROGRESS`

Último detalle observado:

- setup: PASS
- checkout: PASS
- Python: PASS
- uv: PASS
- dependencies: PASS
- Run tests: IN_PROGRESS
- Ruff: pending
- Validate repository: pending
- Verify F0 pilot acceptance: pending

**No asumir P1.5 completamente cerrado hasta comprobar el resultado final de `38273481372`.**

## GLOBAL-F1-AUDIT

Permanece **CLOSED** desde el SHA previo `d21682e92ac839bcbf48448babf16eb1bc8c3a2e`.

Cobertura canónica: 295/295.

No reabrir extracción ni auditoría global salvo evidencia real nueva.

## Próximo paso exacto al reanudar

1. Consultar run `38273481372`.
2. Si `SUCCESS`, marcar P1.5 bundle reproducible como cerrado.
3. Abrir P2 únicamente después de ese GREEN post-merge:
   - README actualizado;
   - CHANGELOG actualizado;
   - release notes para candidato `1.0.0-rc.1`;
   - plan de revisión técnica/editorial separada.
4. Mantener esos cambios fuera de `main`.
5. Después hacer PRE-MAIN compare/integration audit.
6. F1→`main`, release final y cleanup destructivo siguen requiriendo aprobación humana explícita.

## Reglas vigentes

- GitHub vivo manda para estado del proyecto.
- JSON canónico > Markdown derivado.
- fuente exacta 2025 manda para contenido.
- `UNRESOLVED > INVENTED`.
- KISS / simple / optimizado / estable / mantenible / eficiente.
- `DELETE → SIMPLIFY → REUSE → MERGE → EXTEND → ADD`.
- causa raíz antes de parche.
- RED → GREEN → refactor mínimo.
- resultado probado > historia WIP.
- no sobrearquitectura.
- no PDF fuente completo en Git.
- no merge a `main` sin aprobación humana explícita.

## Rama de checkpoint

Este archivo vive en una rama separada para no alterar el CI canónico en curso:

`checkpoint/f1-p15-merged-postci-pending-20261012`
