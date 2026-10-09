# Política de validación técnica

Los valores técnicos recorren estados separados. Una cifra extraída puede pasar a `VISUALLY_VERIFIED` solo tras comparar directamente con la página fuente. F0 no convierte cifras en autoridad de fabricación: `VALIDATED` requiere una revisión técnica posterior y evidencia explícita.

Las reglas del piloto permanecen `CANDIDATE` o `REVIEWED`; ninguna se marca `EXECUTABLE`. Las contradicciones entre páginas se conservan como conflicto, no se resuelven por inferencia.

La validación automática verifica schemas, IDs, procedencia, referencias cruzadas, regiones, coherencia con el mapa de páginas y frescura de los Markdown generados. La validación automática no sustituye la revisión humana de la veracidad técnica.
