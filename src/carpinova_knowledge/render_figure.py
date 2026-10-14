from __future__ import annotations

from html import escape
from typing import Any

_CANVAS = 1000


def _coord(value: Any) -> str:
    return f"{float(value) * _CANVAS:g}"


def _attribute(value: Any) -> str:
    return escape(str(value), quote=True)


def _render_entity(entity: dict[str, Any]) -> str:
    entity_id = _attribute(entity.get("id", ""))
    geometry = entity.get("geometry") or {}
    primitive = geometry.get("primitive")

    if primitive == "rect":
        bounds = geometry["bounds"]
        return (
            f'<rect data-entity-id="{entity_id}" '
            f'x="{_coord(bounds["x"])}" y="{_coord(bounds["y"])}" '
            f'width="{_coord(bounds["width"])}" height="{_coord(bounds["height"])}" '
            'fill="none" stroke="currentColor" stroke-width="2" />'
        )

    if primitive == "line":
        first, second = geometry["points"]
        return (
            f'<line data-entity-id="{entity_id}" '
            f'x1="{_coord(first["x"])}" y1="{_coord(first["y"])}" '
            f'x2="{_coord(second["x"])}" y2="{_coord(second["y"])}" '
            'stroke="currentColor" stroke-width="2" />'
        )

    if primitive == "polyline":
        points = " ".join(
            f'{_coord(point["x"])},{_coord(point["y"])}' for point in geometry["points"]
        )
        return (
            f'<polyline data-entity-id="{entity_id}" points="{points}" '
            'fill="none" stroke="currentColor" stroke-width="2" />'
        )

    raise ValueError(f"unsupported normalized-2d-v1 primitive: {primitive}")


def _render_annotation(annotation: dict[str, Any]) -> str:
    annotation_id = _attribute(annotation.get("id", ""))
    placement = annotation["placement"]
    text = escape(str(annotation.get("text", "")))
    return (
        f'<text data-annotation-id="{annotation_id}" '
        f'x="{_coord(placement["x"])}" y="{_coord(placement["y"])}" '
        f'font-family="sans-serif" font-size="18" fill="currentColor">{text}</text>'
    )


def render_normalized_2d_svg(figure: dict[str, Any]) -> str:
    reconstruction = figure.get("reconstruction") or {}
    if reconstruction.get("render_contract") != "normalized-2d-v1":
        raise ValueError("figure must declare render_contract normalized-2d-v1")

    entities = {
        str(entity["id"]): entity
        for entity in figure.get("entities", [])
        if isinstance(entity, dict) and entity.get("id")
    }
    annotations = {
        str(annotation["id"]): annotation
        for annotation in figure.get("annotations", [])
        if isinstance(annotation, dict) and annotation.get("id")
    }

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img">'
    ]
    layers = sorted(
        figure.get("layers", []),
        key=lambda layer: (int(layer.get("order", 0)), str(layer.get("id", ""))),
    )

    for layer in layers:
        layer_id = _attribute(layer.get("id", ""))
        order = int(layer.get("order", 0))
        lines.append(f'<g data-layer-id="{layer_id}" data-order="{order}">')

        for entity_id in layer.get("entity_ids", []):
            entity = entities.get(str(entity_id))
            if entity is None:
                raise ValueError(f"unknown entity reference: {entity_id}")
            lines.append(_render_entity(entity))

        for annotation_id in layer.get("annotation_ids", []):
            annotation = annotations.get(str(annotation_id))
            if annotation is None:
                raise ValueError(f"unknown annotation reference: {annotation_id}")
            lines.append(_render_annotation(annotation))

        lines.append("</g>")

    lines.append("</svg>")
    return "\n".join(lines) + "\n"
