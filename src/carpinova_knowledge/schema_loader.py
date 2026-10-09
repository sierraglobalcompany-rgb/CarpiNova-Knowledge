from __future__ import annotations
import copy
import json
from pathlib import Path
from typing import Any, Mapping
from jsonschema import Draft202012Validator

SCHEMA_NAMES = ('source','page','content','figure','measurement','rule','concept','lesson','batch')


def _schema_dir() -> Path:
    return Path(__file__).resolve().parents[2] / 'schemas'


def load_schema(name: str) -> dict[str, Any]:
    if name not in SCHEMA_NAMES and name != 'common':
        raise KeyError(name)
    return json.loads((_schema_dir() / f'{name}.schema.json').read_text(encoding='utf-8'))


def _resolve_local_refs(node: Any) -> Any:
    if isinstance(node, dict):
        if set(node) == {'$ref'} and node['$ref'] == 'source.schema.json':
            resolved=copy.deepcopy(load_schema('source'))
            resolved.pop('$schema',None)
            return resolved
        return {k:_resolve_local_refs(v) for k,v in node.items()}
    if isinstance(node, list):
        return [_resolve_local_refs(v) for v in node]
    return node


def validate_instance(name: str, instance: Mapping[str, Any]) -> list[str]:
    schema = _resolve_local_refs(load_schema(name))
    errors = [e.message for e in Draft202012Validator(schema).iter_errors(dict(instance))]
    if name == 'measurement' and instance.get('status') == 'VALIDATED':
        vv = instance.get('visual_verification')
        if not isinstance(vv, Mapping) or vv.get('verified') is not True:
            errors.append('VALIDATED measurement requires visual_verification')
    if name == 'content':
        if instance.get('kind') == 'external_enrichment':
            if not instance.get('external_source'):
                errors.append('external_enrichment requires external_source')
        elif not instance.get('derived_from_content_ids'):
            errors.append('learning_text requires derived_from_content_ids')
    if name == 'figure':
        geometry = instance.get('geometry') or {}
        if geometry.get('precision') == 'unknown' and geometry.get('dimensions'):
            errors.append('unknown geometry cannot claim exact dimensions')
    return sorted(set(errors))
