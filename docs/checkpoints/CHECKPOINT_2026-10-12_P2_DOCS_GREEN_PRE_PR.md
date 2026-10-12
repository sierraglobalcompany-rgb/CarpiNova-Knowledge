# CHECKPOINT — P2 DOCS GREEN / PRE-PR

Fecha: 2026-10-12  
Proyecto: CarpiNova Knowledge F1  
Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`

## Estado canónico

Rama canónica F1: `feat/knowledge-f1`  
SHA canónico antes de integrar P2: `0dccc4840d47c83b748322f5684dfefbeba38feb`

P1.5 BUNDLE REPRODUCIBLE: **CLOSED**

Evidencia P1.5:
- PR #19 integrado a `feat/knowledge-f1`.
- SHA canónico post-merge: `0dccc4840d47c83b748322f5684dfefbeba38feb`.
- CI post-merge: `38273481372` — SUCCESS completo.
- Bundle full-book determinista para 295 páginas.
- CLI canónico: `build-book-dist`.
- `main` no fue tocado.

## P2 — README + CHANGELOG + release notes

Rama activa de trabajo: `feat/knowledge-f1-release-docs-20261012`  
HEAD final P2: `197abc8a97cf9ca0cf09488853f4fa0b7b68efc3`

Diff vs `0dccc484...` limitado a:
- `README.md`
- `CHANGELOG.md`
- `docs/releases/1.0.0-rc.1.md`

No se modificaron:
- schemas;
- datos canónicos del libro;
- source transcription;
- batches;
- workflows;
- código de bundle;
- `main`.

Contenido P2 ya preparado:
- diferencia explícita entre release estable validada `0.1.0` y candidato `1.0.0-rc.1`;
- comando reproducible de full-book bundle;
- source fingerprint canónico;
- aclaración de que bundle generado no es source-of-truth;
- CHANGELOG F1;
- release notes `1.0.0-rc.1`;
- technical/editorial review plan;
- orden de gates alineado con V8A: P2 → P2.5 → P3;
- sin afirmar publicación GitHub no probada;
- sin exigir que la revisión humana esté terminada antes de P2.5.

### QA del HEAD final P2

Run: `38274862939`  
Resultado: **SUCCESS**

Pasaron:
- tests;
- Ruff;
- repository validator;
- F0 pilot acceptance.

## Handoff V8A reconfirmado

Orden operativo vigente:

1. P0.1 VALIDATOR GAP — CLOSED
2. P0.2 P0121 DIMENSION REVIEW — CLOSED
3. P1 GLOBAL F1 AUDIT — CLOSED
4. P1.5 BUNDLE REPRODUCIBLE — CLOSED
5. P2 README + CHANGELOG + release notes — **GREEN EN CANDIDATE; PENDIENTE PR/MERGE A F1**
6. P2.5 PRE-MAIN COMPARE / INTEGRATION AUDIT — NEXT DESPUÉS DE INTEGRAR P2
7. P3 PR F1 → `main` + HUMAN GATE
8. POST: branch hygiene, branch protection, release 1.0

Reglas críticas:
- `continua` autoriza promociones recurrentes candidate/PR → `feat/knowledge-f1` solo si gates están GREEN y el siguiente merge fue explicado.
- No extrapolar `continua` a F1 → `main`, release, deploy o cleanup destructivo.
- No force, no bypass CI, no rebase cosmético de `main`.
- `UNRESOLVED > INVENTED`.
- GitHub vivo + CI vivo mandan para estado.
- PDF exacto 2025 manda para contenido.

## Siguiente paso exacto al reanudar

1. Confirmar live HEAD de `feat/knowledge-f1` sigue en `0dccc484...` o auditar drift si cambió.
2. Confirmar live HEAD de `feat/knowledge-f1-release-docs-20261012` sigue en `197abc8a...`.
3. Reconfirmar run `38274862939` SUCCESS.
4. Auditar diff final de solo tres documentos.
5. Abrir PR desde `feat/knowledge-f1-release-docs-20261012` hacia `feat/knowledge-f1`.
6. Revisar mergeability, reviews/threads y lease.
7. Si todo sigue GREEN, squash merge bajo el contrato recurrente de `continua`.
8. Verificar CI post-merge en `feat/knowledge-f1`.
9. Solo después iniciar P2.5: compare `main` ↔ F1 e integración pre-main.
10. No tocar `main` sin el gate humano explícito de P3.

## Estado de pausa

No se abrió PR de P2 todavía.  
No se hizo merge de P2 todavía.  
No se inició P2.5.  
No se tocó `main`.  
No se creó release.
