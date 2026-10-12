# CarpiNova — Checkpoint 2026-10-12

## Estado canónico

Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`

Rama de integración F1: `feat/knowledge-f1`

HEAD canónico actual:

`d21682e92ac839bcbf48448babf16eb1bc8c3a2e`

PR #18 `Complete global F1 audit gate` fue squash-merged correctamente.

CI post-merge canónico:

- Run: `38270335268`
- Resultado: `SUCCESS`
- Tests: PASS
- Ruff: PASS
- Repository validator: PASS
- F0 pilot acceptance: PASS

## GLOBAL-F1-AUDIT

Estado: **CLOSED**

Se integró:

- auditoría programática global F1;
- clasificación de source gaps;
- auditoría de visuales significativos;
- inventario y findings QR;
- candidatos de seguridad;
- revisión humana documentada de candidatos de seguridad;
- correcciones puntuales de preservación de significado de seguridad en P0259–P0263;
- gate automático con `automatic_blockers=[]`;
- coverage 295/295 mantenida.

No se modificó `main`.

## Fase activa al pausar

**P1.5 — BUNDLE REPRODUCIBLE**

Rama activa:

`feat/knowledge-f1-full-bundle-20261012`

Base exacta:

`d21682e92ac839bcbf48448babf16eb1bc8c3a2e`

### RED

Commit:

`762520ceae77d8c1d4e1f7a984f1adb2e0bffbd5`

Mensaje:

`test(f1): require deterministic full-book bundle`

CI RED:

- Run: `38270776461`
- Fallo esperado y correcto: `ImportError` porque `build_book_distribution` todavía no existía.
- No se detectó fallo colateral.

Contrato RED añadido:

- bundle completo de 295 páginas;
- determinismo byte-a-byte;
- mismos 4 artefactos: `knowledge.bundle.json`, `figures.bundle.json`, `lessons.bundle.json`, `manifest.json`;
- `scope=BOOK`;
- `book_id=cpnc-2025`;
- versión candidata `1.0.0-rc.1`;
- source fingerprint exacto;
- ninguna rule `EXECUTABLE`;
- no rutas locales, `source-books` ni PDF embebido.

### GREEN mínimo implementado

Commit actual de la rama:

`a60b24dca3694a284f5e8d67678490b51d315bba`

Mensaje:

`feat(f1): build deterministic full-book bundle`

Scope actual contra la base canónica:

- `src/carpinova_knowledge/build_dist.py`
- `tests/test_build_dist.py`

Solo 2 archivos.

No hay cambios de schemas, workflows, datos canónicos, batches ni `main`.

Implementación:

- reutiliza serialización estable y hashes existentes;
- conserva comportamiento del builder de lote;
- añade `build_book_distribution()`;
- resuelve directamente las páginas 1..295 desde el manifest del libro;
- reutiliza los mismos recolectores de content/measurements/rules/figures/lessons;
- genera manifest de scope `BOOK`;
- versión candidata `1.0.0-rc.1`, sin declarar todavía release final 1.0.

### CI del GREEN al momento del checkpoint

Run:

`38270911368`

Estado al pausar:

`IN_PROGRESS`

Último estado observado:

- setup: PASS
- dependencies: PASS
- `Run tests`: IN_PROGRESS
- Ruff: pending
- Validate repository: pending
- Verify F0 pilot acceptance: pending

No se debe asumir GREEN hasta leer el resultado final de ese run.

## Próximo paso exacto al reanudar

1. Consultar `38270911368`.
2. Si falla, inspeccionar logs y corregir solo causa raíz.
3. Si pasa completo:
   - añadir un comando CLI mínimo `build-book-dist` para que el build reproducible tenga comando conocido;
   - cubrirlo con test;
   - correr CI completo;
   - auditar diff y lease de `feat/knowledge-f1`;
   - abrir PR hacia `feat/knowledge-f1`;
   - merge recurrente solo si todos los gates quedan GREEN.
4. Después: README + CHANGELOG + release notes.
5. Luego: PRE-MAIN compare/integration audit.
6. **NO** hacer F1→`main`, release ni cleanup destructivo sin aprobación humana explícita.

## Reglas que siguen vigentes

- GitHub vivo manda para estado del proyecto.
- JSON canónico manda sobre Markdown derivado.
- Fuente exacta 2025 manda para contenido.
- `UNRESOLVED > INVENTED`.
- KISS / simple / optimizado / estable / mantenible / eficiente.
- `DELETE → SIMPLIFY → REUSE → MERGE → EXTEND → ADD`.
- causa raíz antes de parche.
- RED → GREEN → refactor mínimo.
- 1 commit ≈ 1 propósito.
- no sobrearquitectura.
- no PDF fuente completo en Git.
- no merge a `main` sin aprobación humana explícita.
