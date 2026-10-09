from __future__ import annotations

import json
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"
BASE_URI = "https://carpinova.local/schemas/"


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / f"{name}.schema.json"
    if not path.is_file():
        raise KeyError(f"unknown schema: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _registry() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        contents = json.loads(path.read_text(encoding="utf-8"))
        uri = contents.get("$id") or f"{BASE_URI}{path.name}"
        registry = registry.with_resource(uri, Resource.from_contents(contents))
    return registry


def validate_instance(schema_name: str, instance: Mapping[str, Any]) -> list[str]:
    validator = Draft202012Validator(load_schema(schema_name), registry=_registry())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]
