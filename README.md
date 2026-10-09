# CarpiNova Knowledge

Canonical structured knowledge base and validation toolchain for CarpiNova Designer and CarpiNova Cell.

The source book PDF is intentionally kept outside Git. This repository stores traceable structured knowledge, schemas, generated review views, validation tooling, FigureSpec records, LessonSpec records, and deterministic consumer bundles.

## F0 status

Knowledge `0.1.0` validates the pilot covering printed pages 88–95 (physical PDF pages 110–117). See `audits/f0-pilot-acceptance.md`.

## Core commands

```bash
python -m carpinova_knowledge validate --root .
python -m carpinova_knowledge build-dist --root . --batch BATCH-000-PILOT --out dist/pilot
python -m carpinova_knowledge report-pilot --root . --batch BATCH-000-PILOT
```

## Safety rules

- Never commit the source PDF.
- Keep physical PDF page and printed page separate.
- JSON is canonical; `source.md`, `normalized.md`, and `learning.md` are generated views.
- Technical measurements require visual verification and are not fabrication authority in F0.
- RuleSpec records remain non-executable until a later technical validation gate.
