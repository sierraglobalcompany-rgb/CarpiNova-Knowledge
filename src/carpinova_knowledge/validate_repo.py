from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .ids import page_id as canonical_page_id
from .render_docs import _render
from .schema_loader import validate_instance


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _error(errors: list[dict[str, Any]], code: str, path: Path, object_id: str | None, message: str, field: str | None = None) -> None:
    item: dict[str, Any] = {"code": code, "file": str(path), "message": message}
    if object_id:
        item["object_id"] = object_id
    if field:
        item["field"] = field
    errors.append(item)


def _source_bounds_ok(source: dict[str, Any]) -> bool:
    region = source.get("region") or {}
    try:
        x = float(region["x"]); y = float(region["y"])
        w = float(region["width"]); h = float(region["height"])
    except (KeyError, TypeError, ValueError):
        return False
    return 0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1 and x + w <= 1 and y + h <= 1


def _iter_sources(kind: str, record: dict[str, Any]) -> Iterable[dict[str, Any]]:
    if kind in {"content", "figure", "measurement"} and isinstance(record.get("source"), dict):
        yield record["source"]
    if kind == "rule":
        for source in record.get("sources", []):
            if isinstance(source, dict):
                yield source


def _validate_semantic_table(
    record: dict[str, Any],
    path: Path,
    errors: list[dict[str, Any]],
) -> None:
    reconstruction = record.get("reconstruction")
    if not isinstance(reconstruction, dict) or reconstruction.get("render_contract") != "semantic-table-v1":
        return

    oid = record.get("figure_id")
    if record.get("type") != "table":
        _error(errors, "semantic_table_incoherent_figure_type", path, oid, "semantic-table-v1 requires type=table", "type")
    if reconstruction.get("preferred_renderer") != "html":
        _error(errors, "semantic_table_incoherent_preferred_renderer", path, oid, "semantic-table-v1 requires preferred_renderer=html", "reconstruction.preferred_renderer")
    if reconstruction.get("deterministic_required") is not True:
        _error(errors, "semantic_table_must_be_deterministic", path, oid, "semantic-table-v1 requires deterministic_required=true", "reconstruction.deterministic_required")
    if reconstruction.get("generative_image_allowed") is not False:
        _error(errors, "semantic_table_generative_image_disallowed", path, oid, "semantic-table-v1 requires generative_image_allowed=false", "reconstruction.generative_image_allowed")

    raw_entities = record.get("entities")
    if not isinstance(raw_entities, list):
        return
    entities = [entity for entity in raw_entities if isinstance(entity, dict)]
    seen_ids: set[str] = set()
    for entity in entities:
        entity_id = entity.get("id")
        if not isinstance(entity_id, str) or not entity_id:
            continue
        if entity_id in seen_ids:
            _error(errors, "semantic_table_duplicate_entity_id", path, oid, f"entity id {entity_id} is duplicated", "entities.id")
        seen_ids.add(entity_id)

    sections = [entity for entity in entities if entity.get("type") == "checklist_section"]
    for text_type in ("title_block", "table_title", "instruction_note"):
        if sum(entity.get("type") == text_type for entity in entities) > 1:
            _error(errors, "semantic_table_duplicate_text_entity", path, oid, f"semantic-table-v1 allows at most one {text_type}", "entities")
    if not sections:
        _error(errors, "semantic_table_missing_section", path, oid, "semantic-table-v1 requires at least one checklist_section", "entities")
    for section in sections:
        headers = section.get("headers")
        if not isinstance(headers, list) or not headers or any(not isinstance(header, str) or not header for header in headers):
            continue
        rows = section.get("rows")
        if not isinstance(rows, list):
            continue
        for row_number, row in enumerate(rows, start=1):
            if isinstance(row, list) and len(row) != len(headers):
                _error(
                    errors,
                    "semantic_table_row_width_mismatch",
                    path,
                    oid,
                    f"checklist_section {section.get('id')} row {row_number} has {len(row)} cells; expected {len(headers)}",
                    "entities.rows",
                )



def _validate_semantic_form(
    record: dict[str, Any], path: Path, errors: list[dict[str, Any]],
) -> None:
    reconstruction = record.get("reconstruction")
    if not isinstance(reconstruction, dict) or reconstruction.get("render_contract") != "semantic-form-v1":
        return
    # The schema owns types, flags and source order; these cross-field rules
    # cannot be expressed with JSON Schema's uniqueItems or fixed row lengths.
    entities = record.get("entities")
    if not isinstance(entities, list):
        return
    seen: set[str] = set()
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        entity_id = entity.get("id")
        if isinstance(entity_id, str):
            if entity_id in seen:
                _error(errors, "semantic_form_duplicate_entity_id", path, record.get("figure_id"), f"Duplicate entity id: {entity_id}", "entities.id")
            seen.add(entity_id)
        if entity.get("type") != "checklist_table":
            continue
        headers, rows = entity.get("headers"), entity.get("rows")
        if isinstance(headers, list) and isinstance(rows, list):
            for index, row in enumerate(rows):
                if isinstance(row, list) and len(row) != len(headers):
                    _error(errors, "semantic_form_row_width_mismatch", path, record.get("figure_id"), f"Row {index + 1} must contain {len(headers)} cells", "entities.rows")


def _validate_semantic_sheet(
    record: dict[str, Any], path: Path, errors: list[dict[str, Any]],
) -> None:
    reconstruction = record.get("reconstruction")
    if not isinstance(reconstruction, dict) or reconstruction.get("render_contract") != "semantic-sheet-v1":
        return

    oid = record.get("figure_id")
    if record.get("type") not in {"form", "table"}:
        _error(errors, "semantic_sheet_incoherent_figure_type", path, oid, "semantic-sheet-v1 requires type=form or type=table", "type")
    if reconstruction.get("preferred_renderer") != "html":
        _error(errors, "semantic_sheet_incoherent_preferred_renderer", path, oid, "semantic-sheet-v1 requires preferred_renderer=html", "reconstruction.preferred_renderer")
    if reconstruction.get("deterministic_required") is not True:
        _error(errors, "semantic_sheet_must_be_deterministic", path, oid, "semantic-sheet-v1 requires deterministic_required=true", "reconstruction.deterministic_required")
    if reconstruction.get("generative_image_allowed") is not False:
        _error(errors, "semantic_sheet_generative_image_disallowed", path, oid, "semantic-sheet-v1 requires generative_image_allowed=false", "reconstruction.generative_image_allowed")

    entities = record.get("entities")
    if not isinstance(entities, list):
        return
    seen_ids: set[str] = set()
    titles = 0
    tables = 0
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        entity_id = entity.get("id")
        if isinstance(entity_id, str):
            if entity_id in seen_ids:
                _error(errors, "semantic_sheet_duplicate_entity_id", path, oid, f"Duplicate sheet entity id: {entity_id}", "entities.id")
            seen_ids.add(entity_id)
        if entity.get("type") == "sheet_title":
            titles += 1
        if entity.get("type") != "sheet_table":
            continue
        tables += 1
        headers = entity.get("headers")
        sections = entity.get("sections")
        if not isinstance(headers, list) or not headers or any(not isinstance(header, str) for header in headers):
            continue
        if not isinstance(sections, list):
            continue

        groups = entity.get("column_groups", [])
        covered_columns: list[int] = []
        groups_valid = True
        for group in groups if isinstance(groups, list) else []:
            if not isinstance(group, dict):
                groups_valid = False
                continue
            start = group.get("start_column")
            span = group.get("span")
            if not isinstance(start, int) or not isinstance(span, int) or start < 1 or span < 1 or start + span > len(headers):
                _error(errors, "semantic_sheet_column_group_out_of_bounds", path, oid, f"Column group in {entity.get('id')} is outside its {len(headers)} columns", "entities.column_groups")
                groups_valid = False
                continue
            columns = list(range(start, start + span))
            if any(column in covered_columns for column in columns):
                _error(errors, "semantic_sheet_column_group_overlap", path, oid, f"Column groups overlap in {entity.get('id')}", "entities.column_groups")
                groups_valid = False
            covered_columns.extend(columns)
        if groups and groups_valid and sorted(covered_columns) != list(range(1, len(headers))):
            _error(errors, "semantic_sheet_column_groups_incomplete", path, oid, f"Column groups in {entity.get('id')} must cover every non-row-header column once", "entities.column_groups")

        for section in sections:
            if not isinstance(section, dict):
                continue
            section_id = section.get("id")
            if isinstance(section_id, str):
                if section_id in seen_ids:
                    _error(errors, "semantic_sheet_duplicate_entity_id", path, oid, f"Duplicate sheet entity id: {section_id}", "entities.sections.id")
                seen_ids.add(section_id)
            rows = section.get("rows")
            if not isinstance(rows, list):
                continue
            row_merges: dict[int, list[tuple[int, int]]] = {}
            for merge in section.get("merged_cells", []):
                if not isinstance(merge, dict):
                    continue
                row_index = merge.get("row")
                start = merge.get("start_column")
                span = merge.get("colspan")
                if not isinstance(row_index, int) or not isinstance(start, int) or not isinstance(span, int) or row_index >= len(rows) or start + span > len(headers):
                    _error(errors, "semantic_sheet_merge_out_of_bounds", path, oid, f"Merged cell in section {section_id} is outside its table", "entities.sections.merged_cells")
                    continue
                row_merges.setdefault(row_index, []).append((start, span))
            for row_index, row in enumerate(rows):
                if not isinstance(row, list):
                    continue
                if len(row) != len(headers):
                    _error(errors, "semantic_sheet_row_width_mismatch", path, oid, f"Table {entity.get('id')} section {section_id} row {row_index + 1} has {len(row)} cells; expected {len(headers)}", "entities.sections.rows")
                    continue
                occupied: set[int] = set()
                for start, span in row_merges.get(row_index, []):
                    merged_columns = set(range(start, start + span))
                    if occupied & merged_columns:
                        _error(errors, "semantic_sheet_merge_overlap", path, oid, f"Merged cells overlap in section {section_id} row {row_index + 1}", "entities.sections.merged_cells")
                    occupied |= merged_columns
                    if any(row[column] != "" for column in range(start + 1, start + span)):
                        _error(errors, "semantic_sheet_merge_discards_source_cell", path, oid, f"Cells covered by a merge must be blank in section {section_id} row {row_index + 1}", "entities.sections.merged_cells")

    if titles != 1:
        _error(errors, "semantic_sheet_title_count", path, oid, "semantic-sheet-v1 requires exactly one sheet_title", "entities")
    if tables == 0:
        _error(errors, "semantic_sheet_missing_table", path, oid, "semantic-sheet-v1 requires at least one sheet_table", "entities")


def _validate_render_contract(
    record: dict[str, Any],
    path: Path,
    errors: list[dict[str, Any]],
    refs: list[tuple[str, Path, str | None, str]],
) -> None:
    reconstruction = record.get("reconstruction") or {}
    if reconstruction.get("render_contract") != "normalized-2d-v1":
        return

    oid = record.get("figure_id")
    entities = [item for item in record.get("entities", []) if isinstance(item, dict)]
    annotations = [item for item in record.get("annotations", []) if isinstance(item, dict)]
    layers = [item for item in record.get("layers", []) if isinstance(item, dict)]

    entity_ids = {item.get("id") for item in entities if item.get("id")}
    annotation_ids: set[str] = set()
    for annotation in annotations:
        annotation_id = annotation.get("id")
        if not annotation_id:
            continue
        if annotation_id in annotation_ids:
            _error(
                errors,
                "render_contract_duplicate_annotation_id",
                path,
                oid,
                f"annotation id {annotation_id} is duplicated",
                "annotations.id",
            )
        annotation_ids.add(annotation_id)

    visible_annotation_ids: set[str] = set()
    layer_members: set[tuple[str, str]] = set()
    for layer in layers:
        for entity_id in layer.get("entity_ids", []):
            if entity_id not in entity_ids:
                _error(
                    errors,
                    "render_contract_unknown_layer_entity",
                    path,
                    oid,
                    f"layer references unknown entity {entity_id}",
                    "layers.entity_ids",
                )
            member = ("entity", entity_id)
            if member in layer_members:
                _error(
                    errors,
                    "render_contract_duplicate_layer_member",
                    path,
                    oid,
                    f"entity {entity_id} appears in more than one layer",
                    "layers.entity_ids",
                )
            layer_members.add(member)

        for annotation_id in layer.get("annotation_ids", []):
            if annotation_id not in annotation_ids:
                _error(
                    errors,
                    "render_contract_unknown_layer_annotation",
                    path,
                    oid,
                    f"layer references unknown annotation {annotation_id}",
                    "layers.annotation_ids",
                )
            visible_annotation_ids.add(annotation_id)
            member = ("annotation", annotation_id)
            if member in layer_members:
                _error(
                    errors,
                    "render_contract_duplicate_layer_member",
                    path,
                    oid,
                    f"annotation {annotation_id} appears in more than one layer",
                    "layers.annotation_ids",
                )
            layer_members.add(member)

    for annotation in annotations:
        annotation_id = annotation.get("id")
        if annotation_id in visible_annotation_ids and not isinstance(annotation.get("placement"), dict):
            _error(
                errors,
                "render_contract_visible_annotation_missing_placement",
                path,
                oid,
                f"visible annotation {annotation_id} requires placement",
                "annotations.placement",
            )

        entity_id = annotation.get("entity_id")
        if entity_id and entity_id not in entity_ids:
            _error(
                errors,
                "unresolved_reference",
                path,
                oid,
                f"reference {entity_id} does not resolve",
                "annotations.entity_id",
            )

        measurement_id = annotation.get("measurement_id")
        if measurement_id:
            refs.append((measurement_id, path, oid, "annotations.measurement_id"))

    for entity in entities:
        geometry = entity.get("geometry") or {}
        if geometry.get("primitive") != "rect" or not isinstance(geometry.get("bounds"), dict):
            continue
        bounds = geometry["bounds"]
        try:
            x = float(bounds["x"])
            y = float(bounds["y"])
            width = float(bounds["width"])
            height = float(bounds["height"])
        except (KeyError, TypeError, ValueError):
            continue
        if x + width > 1 or y + height > 1:
            _error(
                errors,
                "render_contract_bounds_out_of_view",
                path,
                oid,
                f"rect entity {entity.get('id')} leaves normalized viewport",
                "entities.geometry.bounds",
            )


def validate_repository(root: Path) -> dict[str, Any]:
    root = Path(root)
    errors: list[dict[str, Any]] = []
    ids: dict[str, Path] = {}
    refs: list[tuple[str, Path, str | None, str]] = []
    figure_interaction_targets: dict[str, tuple[bool, set[str], set[str]]] = {}

    page_maps: dict[str, dict[int, dict[str, Any]]] = {}
    for path in root.glob("books/*/page-map.json"):
        data = _load(path)
        book_id = str(data.get("book_id", path.parent.name))
        pages = data.get("pages", [])
        page_maps[book_id] = {int(p["pdf_page"]): p for p in pages}
        verified_printed: dict[int, list[dict[str, Any]]] = {}
        for page in pages:
            if page.get("mapping_status") == "verified" and page.get("printed_page") is not None:
                verified_printed.setdefault(int(page["printed_page"]), []).append(page)
        for printed_page, matches in verified_printed.items():
            if len(matches) > 1:
                _error(
                    errors,
                    "duplicate_verified_printed_page",
                    path,
                    None,
                    f"printed page {printed_page} has {len(matches)} verified physical mappings",
                )

    for path in sorted(root.glob("books/*/batches/*.json")):
        batch = _load(path)
        oid = batch.get("batch_id")
        for message in validate_instance("batch", batch):
            _error(errors, "schema_error", path, oid, message)

    for page_dir in sorted(root.glob("books/*/pages/p*")):
        if not page_dir.is_dir():
            continue
        page_path = page_dir / "page.json"
        if not page_path.exists():
            _error(errors, "missing_page_record", page_dir, None, "page.json is required")
            continue
        page = _load(page_path)
        pid = page.get("page_id")
        for message in validate_instance("page", page):
            _error(errors, "schema_error", page_path, pid, message)
        try:
            expected_pid = canonical_page_id(str(page["book_id"]), int(page["pdf_page"]))
            if pid != expected_pid:
                _error(errors, "page_identity_mismatch", page_path, pid, f"expected {expected_pid}")
        except (KeyError, TypeError, ValueError) as exc:
            _error(errors, "page_identity_mismatch", page_path, pid, str(exc))

        if pid in ids:
            _error(errors, "duplicate_id", page_path, pid, f"already defined in {ids[pid]}")
        elif pid:
            ids[pid] = page_path

        book_map = page_maps.get(str(page.get("book_id")), {})
        mapped = book_map.get(int(page.get("pdf_page", 0) or 0))
        if mapped is not None:
            for key in ("page_id", "printed_page", "mapping_status"):
                if mapped.get(key) != page.get(key):
                    _error(errors, "page_map_mismatch", page_path, pid, f"{key} differs from page-map", key)

        groups = [
            ("content", page_dir / "content.json", "content"),
            ("measurement", page_dir / "measurements.json", "measurement"),
            ("rule", page_dir / "rules.json", "rule"),
        ]
        records_by_kind: dict[str, list[dict[str, Any]]] = {}
        for kind, path, schema in groups:
            if not path.exists():
                _error(errors, "missing_required_file", path, pid, f"{path.name} is required")
                records_by_kind[kind] = []
                continue
            records = _load(path)
            if not isinstance(records, list):
                _error(errors, "schema_error", path, pid, "top-level value must be a list")
                records = []
            records_by_kind[kind] = records
            id_field = {"content": "content_id", "measurement": "measurement_id", "rule": "rule_id"}[kind]
            for record in records:
                oid = record.get(id_field)
                for message in validate_instance(schema, record):
                    _error(errors, "schema_error", path, oid, message)
                if oid in ids:
                    _error(errors, "duplicate_id", path, oid, f"already defined in {ids[oid]}")
                elif oid:
                    ids[oid] = path
                if record.get("page_id") != pid:
                    _error(errors, "page_identity_mismatch", path, oid, "record page_id differs from owning page")
                for source in _iter_sources(kind, record):
                    if source.get("pdf_page") != page.get("pdf_page") or source.get("book_id") != page.get("book_id"):
                        _error(errors, "source_page_mismatch", path, oid, "source does not point to owning page")
                    if not _source_bounds_ok(source):
                        _error(errors, "source_region_out_of_bounds", path, oid, "source region must fit within [0,1] page bounds")
                if kind == "content":
                    for ref in record.get("derived_from_content_ids", []):
                        refs.append((ref, path, oid, "derived_from_content_ids"))
                if kind == "measurement" and record.get("status") == "VALIDATED" and not record.get("visual_verification"):
                    _error(errors, "measurement_visual_verification_required", path, oid, "VALIDATED technical measurement requires visual verification evidence")

        figures_dir = page_dir / "figures"
        if figures_dir.exists():
            for path in sorted(figures_dir.glob("*.json")):
                record = _load(path)
                oid = record.get("figure_id")
                for message in validate_instance("figure", record):
                    _error(errors, "schema_error", path, oid, message)
                if oid in ids:
                    _error(errors, "duplicate_id", path, oid, f"already defined in {ids[oid]}")
                elif oid:
                    ids[oid] = path
                if record.get("page_id") != pid:
                    _error(errors, "page_identity_mismatch", path, oid, "figure page_id differs from owning page")
                for source in _iter_sources("figure", record):
                    if source.get("pdf_page") != page.get("pdf_page") or source.get("book_id") != page.get("book_id"):
                        _error(errors, "source_page_mismatch", path, oid, "source does not point to owning page")
                    if not _source_bounds_ok(source):
                        _error(errors, "source_region_out_of_bounds", path, oid, "source region must fit within [0,1] page bounds")
                reconstruction = record.get("reconstruction") or {}
                if reconstruction.get("deterministic_required") and reconstruction.get("preferred_renderer") == "image" and reconstruction.get("generative_image_allowed"):
                    _error(errors, "deterministic_figure_generative_only", path, oid, "deterministic figure cannot rely only on generative image rendering")
                if oid:
                    entity_ids = {
                        entity.get("id")
                        for entity in record.get("entities", [])
                        if isinstance(entity, dict) and entity.get("id")
                    }
                    measurement_ids = {
                        annotation.get("measurement_id")
                        for annotation in record.get("annotations", [])
                        if isinstance(annotation, dict) and annotation.get("measurement_id")
                    }
                    figure_interaction_targets[oid] = (
                        reconstruction.get("render_contract") == "normalized-2d-v1",
                        entity_ids,
                        measurement_ids,
                    )
                _validate_semantic_table(record, path, errors)
                _validate_semantic_form(record, path, errors)
                _validate_semantic_sheet(record, path, errors)
                _validate_render_contract(record, path, errors, refs)
                for ref in record.get("measurements", []):
                    refs.append((ref, path, oid, "measurements"))

        content_records = records_by_kind.get("content", [])
        generated = {
            "source.md": _render(content_records, "source_transcription", "Source transcription"),
            "normalized.md": _render(content_records, "normalized_text", "Normalized text"),
            "learning.md": _render(content_records, "learning_text", "Learning text"),
        }
        for filename, expected in generated.items():
            path = page_dir / filename
            actual = path.read_text(encoding="utf-8") if path.exists() else None
            if actual != expected:
                _error(errors, "stale_generated_markdown", path, pid, "generated Markdown does not match canonical content.json")

    for path in sorted(root.glob("lessons/**/*.json")):
        lesson = _load(path)
        oid = lesson.get("lesson_id")
        for message in validate_instance("lesson", lesson):
            _error(errors, "schema_error", path, oid, message)
        if oid in ids:
            _error(errors, "duplicate_id", path, oid, f"already defined in {ids[oid]}")
        elif oid:
            ids[oid] = path
        for ref in lesson.get("source_content_ids", []):
            refs.append((ref, path, oid, "source_content_ids"))
        for step in lesson.get("steps", []):
            step_content_ids = set(step.get("content_ids", []))
            step_figure_ids = list(step.get("figure_ids", []))
            for ref in step_content_ids:
                refs.append((ref, path, oid, "steps.content_ids"))
            for ref in step_figure_ids:
                refs.append((ref, path, oid, "steps.figure_ids"))

            interaction = step.get("interaction")
            if not isinstance(interaction, dict):
                continue

            interaction_type = interaction.get("type")
            allowed_entities: set[str] = set()
            allowed_measurements: set[str] = set()
            for figure_id in step_figure_ids:
                figure_targets = figure_interaction_targets.get(figure_id)
                if figure_targets is None:
                    continue
                render_ready, entity_ids, measurement_ids = figure_targets
                if render_ready:
                    allowed_entities.update(entity_ids)
                    allowed_measurements.update(measurement_ids)

            if interaction_type == "highlight":
                for target in interaction.get("target_entity_ids", []):
                    if target not in allowed_entities:
                        _error(
                            errors,
                            "interaction_unresolved_entity_target",
                            path,
                            oid,
                            f"interaction target {target} does not resolve in a render-ready step figure",
                            "steps.interaction.target_entity_ids",
                        )
            elif interaction_type == "highlight_measurements":
                for ref in interaction.get("measurement_ids", []):
                    refs.append((ref, path, oid, "steps.interaction.measurement_ids"))
                    if ref not in allowed_measurements:
                        _error(
                            errors,
                            "interaction_unresolved_measurement_target",
                            path,
                            oid,
                            f"interaction measurement {ref} does not resolve in a render-ready step figure",
                            "steps.interaction.measurement_ids",
                        )
            elif interaction_type == "identify_parts":
                source_content_id = interaction.get("source_content_id")
                if source_content_id:
                    refs.append((source_content_id, path, oid, "steps.interaction.source_content_id"))
                    if source_content_id not in step_content_ids:
                        _error(
                            errors,
                            "interaction_source_content_not_in_step",
                            path,
                            oid,
                            f"interaction source content {source_content_id} is not part of the lesson step",
                            "steps.interaction.source_content_id",
                        )
            elif interaction_type == "guided_sequence":
                seen_orders: set[int] = set()
                for item in interaction.get("sequence", []):
                    order = item.get("order")
                    if order in seen_orders:
                        _error(
                            errors,
                            "interaction_duplicate_sequence_order",
                            path,
                            oid,
                            f"guided sequence order {order} is duplicated",
                            "steps.interaction.sequence.order",
                        )
                    elif isinstance(order, int):
                        seen_orders.add(order)

                    content_id = item.get("content_id")
                    if content_id:
                        refs.append((content_id, path, oid, "steps.interaction.sequence.content_id"))
                        if content_id not in step_content_ids:
                            _error(
                                errors,
                                "interaction_sequence_content_not_in_step",
                                path,
                                oid,
                                f"guided sequence content {content_id} is not part of the lesson step",
                                "steps.interaction.sequence.content_id",
                            )
                    for ref in item.get("measurement_ids", []):
                        refs.append((ref, path, oid, "steps.interaction.sequence.measurement_ids"))

    for ref, path, oid, field in refs:
        if ref not in ids:
            _error(errors, "unresolved_reference", path, oid, f"reference {ref} does not resolve", field)

    for index_path in root.glob("books/*/index.json"):
        index = _load(index_path)
        book_id = str(index.get("book_id", index_path.parent.name))
        mapped_pages = set(page_maps.get(book_id, {}))
        for section in index.get("sections", []):
            pr = section.get("physical_range") or {}
            start, end = pr.get("start"), pr.get("end")
            if not isinstance(start, int) or not isinstance(end, int) or start > end or start not in mapped_pages or end not in mapped_pages:
                _error(errors, "index_range_invalid", index_path, section.get("section_id"), "physical range is invalid or outside page map")

    return {"valid": not errors, "error_count": len(errors), "errors": errors}
