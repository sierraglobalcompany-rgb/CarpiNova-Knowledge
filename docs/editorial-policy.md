# Política editorial de CarpiNova Knowledge

## Tres capas separadas

1. `source_transcription`: conserva lo que afirma la fuente, sin añadir conocimiento externo.
2. `normalized_text`: corrige ortografía, puntuación, unidades y redacción sin alterar el significado técnico.
3. `learning_text`: explica la misma idea con lenguaje más sencillo para principiantes; cada bloque debe declarar de qué ContentSpec deriva.

No se corrige silenciosamente una afirmación técnica del libro. Si una afirmación parece dudosa, se conserva con su procedencia y se marca para revisión. El enriquecimiento externo se almacena como `external_enrichment` con una fuente independiente.

## Unidades

La transcripción respeta las unidades de la fuente. Las representaciones estructuradas normalizan dimensiones lineales a milímetros cuando se convierten en MeasurementSpec, sin perder el texto original.

## Lenguaje pedagógico

La versión de aprendizaje prioriza frases cortas, explica qué se hace y para qué, y evita presentar recomendaciones del libro como normas universales si la fuente no lo sostiene.
