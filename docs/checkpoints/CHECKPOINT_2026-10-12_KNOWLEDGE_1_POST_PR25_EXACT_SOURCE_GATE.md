# CHECKPOINT — CarpiNova Knowledge 1.0 post-PR25 / exact-source gate

Fecha: 2026-10-12

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama canónica: `main`
- SHA de `main`: `f543f8fdb18ed986bdcac1fd1fbb3d7b48bf0cb8`
- Merge más reciente: PR #25 — `Document Knowledge 1.0 post-merge final review gate`
- PR #25 fue mergeado normalmente con lease exacto desde head `53887abdefa7c486e1d3b4f749bcbfaf9163b079`.

## CI / QA

Post-merge Knowledge QA de `main`:

- run: `38283017056`
- head SHA: `f543f8fdb18ed986bdcac1fd1fbb3d7b48bf0cb8`
- resultado: `SUCCESS`
- tests: PASS
- Ruff: PASS
- repository validator: PASS
- F0 pilot acceptance: PASS

QA previo del commit correctivo `3ebd91ee46777d4d71cd397b5313dc002c416f1d`:

- run `38282568686`: SUCCESS
- `202 passed`
- Ruff PASS
- validator `valid: true`, `error_count: 0`
- F0 pilot: `GO`

QA del PR #25:

- run `38282678212`: SUCCESS

## Estado de release

- `1.0.0` FINAL: **NO CREADO**
- `1.0.0-rc.1`: sigue siendo candidato, no release final.
- No debe declararse `1.0.0` hasta completar evidencia humana real de revisión técnica/editorial con la fuente canónica exacta.

## Único gate restante

Issue #24: `Knowledge 1.0 final gate — exact-source technical/editorial review`

Estado: OPEN
Asignado a: `sierraglobalcompany-rgb`

Fuente canónica requerida:

- `book_id`: `cpnc-2025`
- páginas físicas: `295`
- SHA-256: `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`

La copia actualmente accesible `LibroFinal.pdf` NO es válida para cerrar el gate:

- páginas: `256`
- SHA-256: `dbff03699899e3946c8af714f8f6fb9dbda78e582785dee95b303373870b15cb`

No sustituir la fuente canónica por otra edición, memoria, web o inferencia.

## Informe final versionado

Existe en `main`:

- `docs/releases/1.0.0-review.md`

Estado interno del informe:

- `BLOCKED_BY_EXACT_SOURCE_REVIEW`
- no afirma revisión humana completada;
- contiene checklist técnico/editorial;
- requiere revisores, fecha, hash exacto, hallazgos y disposiciones;
- `UNRESOLVED` puede permanecer si es explícito y trazable;
- solo puede pasar a `PASS_FOR_1.0.0` con evidencia real.

También quedó actualizado:

- `docs/releases/1.0.0-rc.1.md`

con el estado post-merge real, PR #23, CI de `main`, Issue #24 y el bloqueo de fuente exacta.

## Incidente documental registrado

Durante la preparación del informe final se creó accidentalmente en `main` `docs/releases/1.0.0-review.md` con contenido literal `placeholder` en commit:

- `ce1c0c3971f7c1a30c9d73c687f376fa85b770f1`

El error se detectó inmediatamente y el mismo archivo fue reemplazado por el informe bloqueante real en:

- `3ebd91ee46777d4d71cd397b5313dc002c416f1d`

No se alteraron código, schemas, conocimiento canónico, workflows ni archivos fuente. El incidente quedó documentado también en Issue #24.

## GitHub protection / hygiene

- `main` aparece actualmente con `protected: false`.
- Intento de consultar/configurar rulesets del repositorio privado devolvió HTTP 403 indicando que esa función requiere GitHub Pro o repositorio público.
- No se debe afirmar protección activa ni simularla.
- La higiene destructiva de ramas no se ejecutó en este checkpoint.

## Reglas operativas vigentes

- KISS / simple / optimizado / estable / mantenible / eficiente.
- `DELETE → SIMPLIFY → REUSE → MERGE → EXTEND → ADD`.
- Evidencia > suposiciones.
- JSON canónico > Markdown derivado.
- `UNRESOLVED > INVENTED`.
- No force / no bypass CI / no schema drift por conveniencia.
- No repetir auditorías globales ya cerradas sin nueva evidencia.
- `continua` del propietario equivale a autorización para ejecutar los pasos pendientes legítimamente ejecutables, incluidos merges y releases, salvo excepción explícita.
- Esa autorización no sustituye evidencia humana que materialmente aún no existe.

## Próximo punto exacto al reanudar

1. Verificar que `main` siga en `f543f8fdb18ed986bdcac1fd1fbb3d7b48bf0cb8` o auditar cualquier drift.
2. Recuperar/re-adjuntar el PDF canónico exacto de 295 páginas y verificar SHA-256 `318ceb94569608bfe062e3e50c7032edee79febf06102f7eec760769a6dfd90c`.
3. Ejecutar la revisión técnica/editorial requerida por Issue #24.
4. Versionar hallazgos reales en `docs/releases/1.0.0-review.md` mediante rama + PR normal.
5. Resolver o disponer `NEEDS_CHANGE`; mantener `UNRESOLVED` explícitos.
6. Cambiar el informe a `PASS_FOR_1.0.0` solo si la evidencia lo soporta.
7. Crear release/tag final `1.0.0` y verificar estado final.
8. Revisar higiene/protección de ramas solo dentro de las capacidades reales del plan de GitHub.

## Estado de parada

Checkpoint creado. No continuar trabajo después de este punto hasta nueva instrucción del propietario.
