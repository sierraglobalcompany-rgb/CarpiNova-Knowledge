from __future__ import annotations

import copy

import pytest

from carpinova_knowledge.render_figure import render_normalized_2d_svg


def _figure() -> dict:
    return {
        "figure_id": "FIG-TEST-001",
        "entities": [
            {
                "id": "rect-1",
                "geometry": {
                    "primitive": "rect",
                    "precision": "approximate",
                    "bounds": {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
                },
            },
            {
                "id": "line-1",
                "geometry": {
                    "primitive": "line",
                    "precision": "approximate",
                    "points": [{"x": 0.1, "y": 0.1}, {"x": 0.9, "y": 0.1}],
                },
            },
            {
                "id": "poly-1",
                "geometry": {
                    "primitive": "polyline",
                    "precision": "approximate",
                    "points": [
                        {"x": 0.2, "y": 0.8},
                        {"x": 0.5, "y": 0.6},
                        {"x": 0.8, "y": 0.8},
                    ],
                },
            },
        ],
        "annotations": [
            {
                "id": "ann-1",
                "text": "A & B <C>",
                "placement": {"x": 0.25, "y": 0.9, "precision": "approximate"},
            }
        ],
        "layers": [
            {"id": "top", "order": 20, "entity_ids": ["poly-1"], "annotation_ids": ["ann-1"]},
            {"id": "base", "order": 10, "entity_ids": ["rect-1", "line-1"]},
        ],
        "camera": {
            "coordinate_space": "normalized_figure",
            "viewport": {"x": 0, "y": 0, "width": 1, "height": 1},
        },
        "reconstruction": {
            "preferred_renderer": "svg",
            "deterministic_required": True,
            "generative_image_allowed": False,
            "render_contract": "normalized-2d-v1",
        },
    }


def test_renderer_rejects_figure_without_normalized_contract() -> None:
    figure = _figure()
    figure["reconstruction"].pop("render_contract")

    with pytest.raises(ValueError, match="normalized-2d-v1"):
        render_normalized_2d_svg(figure)


def test_renderer_sorts_layers_and_renders_supported_primitives() -> None:
    svg = render_normalized_2d_svg(_figure())

    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"')
    assert svg.index('data-layer-id="base"') < svg.index('data-layer-id="top"')
    assert '<rect data-entity-id="rect-1" x="100" y="200" width="300" height="400"' in svg
    assert '<line data-entity-id="line-1" x1="100" y1="100" x2="900" y2="100"' in svg
    assert '<polyline data-entity-id="poly-1" points="200,800 500,600 800,800"' in svg


def test_renderer_renders_visible_annotation_as_escaped_text() -> None:
    svg = render_normalized_2d_svg(_figure())

    assert '<text data-annotation-id="ann-1" x="250" y="900"' in svg
    assert "A &amp; B &lt;C&gt;" in svg
    assert "A & B <C>" not in svg


def test_renderer_rejects_unknown_layer_reference() -> None:
    figure = _figure()
    figure["layers"][0]["entity_ids"] = ["missing"]

    with pytest.raises(ValueError, match="missing"):
        render_normalized_2d_svg(figure)


def test_renderer_is_byte_deterministic_for_same_input() -> None:
    figure = _figure()

    first = render_normalized_2d_svg(copy.deepcopy(figure))
    second = render_normalized_2d_svg(copy.deepcopy(figure))

    assert first == second
