# CHECKPOINT — CarpiNova Knowledge F1

**Fecha:** 2026-10-12  
**Estado:** P2 y P2.5 cerrados; detenido antes del gate humano F1 → `main`.

## 1. Estado canónico actual

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama canónica F1: `feat/knowledge-f1`
- SHA canónico F1: `c5c9797f144627953b7672c50ccc4d8ec84708c3`
- Tree F1: `469e2633e462ce6ee7f02e0c5bf6eeb8d7e51af6`
- `main`: `ac0a0440de11df9514d7ba59e9957dff833bd7b1`
- `main` permanece sin cambios de F1.

## 2. P1.5 — bundle reproducible

CERRADO previamente.

El bundle F1 completo del libro sigue siendo reproducible mediante `build-book-dist`, con:

- 295 páginas canónicas;
- `knowledge_version=1.0.0-rc.1`;
- `scope=BOOK`;
- `book_id=cpnc-2025`;
- SHA-256 de fuente canónica: `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`;
- sin PDF fuente almacenado en Git;
- sin reglas `EXECUTABLE`.

## 3. P2 — documentación de release candidate

**CERRADO.**

PR #20 integró en `feat/knowledge-f1`:

- README actualizado;
- CHANGELOG con `1.0.0-rc.1` como candidato no final;
- `docs/releases/1.0.0-rc.1.md`;
- plan de revisión humana técnica/editorial;
- comando y contrato del bundle reproducible;
- gates restantes hacia `main` y release final.

SHA post-P2: `3123ba913e7337f0c8c675e73af1bd4de6781e99`.

CI canónico post-P2:

- run `38275672599`
- tests: PASS
- Ruff: PASS
- validator: PASS
- F0 pilot acceptance: PASS
- conclusión: SUCCESS

## 4. P2.5 — auditoría pre-main

**CERRADO.**

Informe integrado:

`audits/f1/pre-main-integration-audit-2026-10-12.md`

PR #22 fue squash-merged a `feat/knowledge-f1`.

SHA canónico resultante:

`c5c9797f144627953b7672c50ccc4d8ec84708c3`

Hallazgos principales:

- compare `main` → F1: F1 estaba 360 commits ahead y 2 behind;
- los 2 commits exclusivos de `main` son únicamente `docs/.noop` y su revert;
- compare merge-base → `main`: cero archivos cambiados;
- tree actual de `main` == tree del merge-base: `25e0c5fbaf083cd02cf38846879f793cdeab2bcf`;
- por tanto, `main` no contiene contenido funcional exclusivo que deba recuperarse antes de integrar F1;
- estrategia correcta: PR normal F1 → `main`, sin rebase cosmético, sin force y sin bypass;
- manifest canónico sigue declarando 295 páginas y el SHA-256 correcto;
- árbol F1 no contiene PDF fuente ni `source-books/` versionado.

CI de la rama P2.5 antes del merge:

- run `38276162765`
- SUCCESS completo

CI canónico post-merge P2.5:

- run `38276571457`
- SHA: `c5c9797f144627953b7672c50ccc4d8ec84708c3`
- estado: COMPLETED
- conclusión: SUCCESS

Por tanto, **P2.5 queda cerrado**.

## 5. Incidente operativo registrado

Durante P2.5 se abrió accidentalmente el draft PR #21 con metadata placeholder al intentar preparar la rama.

Fue cerrado inmediatamente:

- estado: CLOSED
- merged: NO
- `main` no fue modificado.

El incidente ya está documentado en el informe P2.5 y no altera el resultado técnico.

## 6. Punto exacto de parada

El PR final `feat/knowledge-f1` → `main` **todavía no se ha abierto** después del cierre de P2.5.

No se ha realizado:

- merge F1 → `main`;
- release `1.0.0`;
- tag final;
- limpieza destructiva de ramas;
- bypass de CI;
- force push.

## 7. Próximo paso al continuar

1. Verificar que `feat/knowledge-f1` siga exactamente en `c5c9797f144627953b7672c50ccc4d8ec84708c3` y que `main` no haya cambiado externamente.
2. Abrir el PR final `feat/knowledge-f1` → `main`.
3. Verificar `mergeable=true`, diff global y CI del PR.
4. Presentar el PR y la evidencia al usuario.
5. **DETENERSE y exigir aprobación humana explícita antes de cualquier merge a `main`.**
6. Solo si el usuario aprueba: merge normal, sin bypass/force, y verificar CI post-merge de `main`.
7. Release/tag `1.0.0`, cierre de revisión humana y limpieza de ramas siguen siendo gates posteriores y requieren cumplir sus condiciones; no adelantarlos por inferencia.

## 8. Leyes vigentes

- KISS / simple / optimizado / estable / mantenible / eficiente.
- `DELETE → SIMPLIFY → REUSE → MERGE → EXTEND → ADD`.
- evidencia > suposiciones.
- GitHub live state = verdad operacional del proyecto.
- fuente 2025 exacta = verdad de contenido.
- `UNRESOLVED > INVENTED`.
- no convertir conflictos de fuente en una verdad inferida.
- no force, no bypass, no cambios destructivos sin aprobación.
- F1 → `main` permanece bajo gate humano explícito.

## 9. Resumen máquina

```text
P1.5_BUNDLE: CLOSED
P2_DOCS: CLOSED
P2_5_PRE_MAIN_AUDIT: CLOSED
CANONICAL_F1_SHA: c5c9797f144627953b7672c50ccc4d8ec84708c3
POST_P25_CI_RUN: 38276571457
POST_P25_CI: SUCCESS
MAIN_SHA: ac0a0440de11df9514d7ba59e9957dff833bd7b1
MAIN_MODIFIED_BY_F1: NO
FINAL_F1_TO_MAIN_PR: NOT_OPENED
HUMAN_GATE_REQUIRED_BEFORE_MAIN_MERGE: YES
FINAL_RELEASE_1_0_0: NOT_CREATED
```

**Checkpoint: listo para reanudar desde la apertura del PR final F1 → `main`, sin perder contexto y sin cruzar el gate humano automáticamente.**
