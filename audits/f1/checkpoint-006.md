# F1 Checkpoint 006 — reanudación segura

**Corte:** después de `BATCH-015`, antes del bloque técnico `Mi primer Ensamble`.

## Estado canónico

- Repositorio: `sierraglobalcompany-rgb/CarpiNova-Knowledge`
- Rama: `feat/knowledge-f1`
- Último commit funcional: `c3981c35502d7a0a29175ca4931d917cc058738d`
- Último lote cerrado: `BATCH-015`
- Knowledge QA run: `38015629634`
- CI: **GREEN**
  - tests: success
  - Ruff: success
  - validate repository: success
  - F0 pilot acceptance: success

## Cobertura

- Total físico canónico: 295
- Completas: 69
- Pendientes: 226
- Duplicados entre lotes: 0
- F1 secuencial completado hasta PDF física 61

## Lotes recientes

- `BATCH-014`: GO — PDF 56–58 / impresas 34–36 — `La evolución de la carpintería`.
- `BATCH-015`: GO — PDF 59–61 / impresas 37–39 — separador, página en blanco y portada `Mi primer Ensamble`.

## Hallazgos de BATCH-014

- La fuente describe el proceso tradicional desde árbol → secado → canteado/cepillado → uniones → lijado/protección/acabado.
- Introduce tableros preelaborados como evolución por eficiencia y precisión.
- Enumera aglomerado, alistonado y contrachapado.
- Defiende preservar ebanistería/madera sólida como saber artesanal.
- Relaciona tableros con nuevos retos de mobiliario multifuncional, sistemas y herrajes.
- Conserva como afirmaciones del autor las bandas de vivienda 80–120 m² frente a 15–45 m²; no son estándares validados.
- p58 contiene FigureSpec de `LA EVOLUCIÓN DE LA CARPINTERÍA`.

## Convención confirmada para páginas sin contenido

- Páginas decorativas o vacías usan `content.json = []`.
- `source.md`, `normalized.md` y `learning.md` conservan únicamente el encabezado generado.
- `visual-inventory.json` documenta por qué el visual no es reutilizable.

## Siguiente bloque inspeccionado

### BATCH-016 propuesto — PDF 62–67 / impresas 40–45

Bloque coherente `Mi primer Ensamble`:

- p62: introducción al primer ensamble, recomendación de ver videos de apoyo y QR.
- p63: objetivo: armar una mesa de noche en tablero aglomerado de 15 mm laminado; cajón con riel/corredera telescópica; puerta batiente inferior; dos bisagras y correderas telescópicas. Incluye lista de herramientas/materiales manuales y eléctricos, identifica módulo de práctica de 40×40×32 cm, explica compra/despiece y verificación de medidas; QR para adquirir módulo.
- p64: vista del módulo, tabla de despiece con piezas y tapacantos, y lista de herrajes: 1 corredera telescópica 30 cm, 1 par de bisagras parche 35 mm, tornillos de ensamble/pulgadas y 5/8.
- p65: ensamble de base y dos laterales; base 400×320 mm, laterales 370×320 mm; ubicación de tapacantos y perforación/atornillado.
- p66: montaje de correas a los laterales; dimensión visible 370 mm y referencias de 70 mm en la ilustración.
- p67: posicionamiento de corredera telescópica en el lateral; referencia visible de 37 mm al borde frontal y 100 mm vertical, con explicación de Sistema 37/32 y primer tornillo a 37 mm del borde del mueble.

## Reglas para BATCH-016

- Extraer fuente, normalización y learning sin completar huecos con conocimiento externo.
- Crear `measurements.json` para medidas explícitas, pero mantener estado de autoridad como fuente/candidato, nunca `VALIDATED` automáticamente.
- `rules.json` solo si el texto formula una instrucción suficientemente explícita; debe permanecer como regla candidata de fuente, no ejecutable.
- FigureSpec obligatorio para ilustraciones técnicas de p64–67 porque contienen geometría y cotas reutilizables.
- QR: conservar destino/función si es legible; no ingerir automáticamente contenido externo.
- Mantener las unidades exactamente como fuente y normalizar a mm solo en campos estructurados si el esquema existente lo permite.
- No declarar lote terminado sin CI GREEN.

## Orden al reanudar

1. Verificar HEAD y descendencia de este checkpoint.
2. Crear `BATCH-016 = PDF 62–67`.
3. Procesar p62–63 primero, separando contenido pedagógico de medidas/hardware.
4. Procesar p64–67 con FigureSpec y medidas explícitas.
5. Actualizar cobertura a **75/295**, pendientes **220**, si las seis páginas quedan completas.
6. Publicar con fast-forward + lease.
7. Esperar CI GREEN antes de continuar.

**Decisión:** continuar con `BATCH-016`.