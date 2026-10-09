# CarpiNova Knowledge — Diseño F0/F1

## Propósito

CarpiNova Knowledge es la fuente canónica y reutilizable de conocimiento para CarpiNova Designer y CarpiNova Cell. El PDF fuente no se versiona en Git. El repositorio conserva conocimiento estructurado, procedencia, reglas candidatas, FigureSpec, LessonSpec y distribuciones determinísticas.

## Principios

- `pdf_page` identifica la página física del PDF y es la clave canónica de trazabilidad.
- `printed_page` es independiente y puede ser `null`.
- Cada bloque conserva `source_transcription`, `normalized_text` y `learning_text`.
- El texto pedagógico nunca reemplaza la fuente y debe conservar procedencia explícita.
- Ningún número técnico pasa a autoridad de fabricación por OCR o extracción automática.
- FigureSpec es un objeto de primera clase: describe región fuente, entidades, etiquetas, relaciones, medidas, precisión geométrica, modo de reconstrucción y secuencia educativa.
- Diagramas técnicos, tablas, cotas y QR se reconstruyen de forma determinística siempre que sea posible.
- Reglas de F0/F1 son `CANDIDATE` o `REVIEWED`; `EXECUTABLE` queda reservado para una validación técnica posterior.
- Activos de terceros se registran y se marcan con restricciones de uso; no se convierten silenciosamente en material reutilizable.

## Capas

1. **Book source map:** manifiesto, SHA-256, auditoría física, mapa físico/impreso e índice.
2. **Canonical records:** PageSpec, ContentSpec, FigureSpec, MeasurementSpec, RuleSpec, ConceptSpec, LessonSpec y BatchSpec.
3. **Review views:** Markdown generado desde JSON canónico.
4. **Validation:** schemas, IDs, referencias, procedencia, estados numéricos, restricciones visuales y frescura de vistas generadas.
5. **Distribution:** bundles determinísticos consumibles por Designer y Cell.

## F0

Validar el sistema con páginas impresas 88–95, físicas 110–117. El piloto debe cubrir texto, diagramas, tabla, QR, reglas, medidas y una lección reutilizable. Criterio de salida: reporte `GO` y Knowledge `0.1.0`.

## F1

Extraer el resto del libro en lotes adaptativos: normalmente 5–6 páginas, 3–4 en páginas técnicas densas y hasta 8 en páginas sencillas. Cada lote debe cerrar con validación automática y revisión periódica de taxonomía, conflictos, unidades y duplicados. El objetivo final es Knowledge `1.0`.
