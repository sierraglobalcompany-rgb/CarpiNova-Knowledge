# Política de FigureSpec

Toda figura significativa se inventaría visualmente antes de reescribir la página. Cada figura conserva región de origen, entidades importantes, relaciones, anotaciones, medidas vinculadas y estrategia de reconstrucción.

- Planos, cotas, tablas y diagramas funcionales: reconstrucción determinística (`svg`, `html`, `3d` o `hybrid`).
- Ilustraciones conceptuales: pueden permitir generación visual solo si etiquetas, medidas y relaciones permanecen determinísticas.
- Códigos QR y marcas: se preservan como referencia visual; no se regeneran con IA.
- Geometría no demostrable por la fuente se marca `approximate` o `unknown`; nunca se inventa precisión.

`educational_sequence` describe cómo una futura interfaz puede revelar o destacar partes de la figura. No obliga a implementar la animación en F0.
