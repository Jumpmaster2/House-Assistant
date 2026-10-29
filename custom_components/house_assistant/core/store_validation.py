"""Validation of stored records without coercion or changes to valid input."""

from __future__ import annotations

import math
from typing import Any


def number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def validate(value: Any, schema: Any) -> None:
    """Check only supplied fields; missing fields retain their existing defaults."""
    if isinstance(schema, dict):
        if not isinstance(value, dict):
            raise ValueError("Expected a mapping")
        if isinstance(schema, RecordSchema) and not schema.required <= value.keys():
            raise ValueError("Missing required stored fields")
        for key, item in value.items():
            if key in schema or "*" in schema:
                validate(item, schema.get(key, schema.get("*")))
            else:
                finite_tree(item)
    elif isinstance(schema, list):
        if not isinstance(value, list):
            raise ValueError("Expected a list")
        for item in value:
            validate(item, schema[0])
    elif isinstance(schema, tuple):
        if not isinstance(value, list) or len(value) != len(schema):
            raise ValueError("Invalid list dimensions")
        for item, spec in zip(value, schema, strict=True):
            validate(item, spec)
    elif not schema(value):
        raise ValueError("Invalid stored field")


def finite_tree(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            finite_tree(item)
    elif isinstance(value, list):
        for item in value:
            finite_tree(item)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Nonfinite stored number")


def optional(schema: Any):
    def check(value: Any) -> bool:
        if value is not None:
            validate(value, schema)
        return True

    return check


def text(value: Any) -> bool:
    return isinstance(value, str)


def boolean(value: Any) -> bool:
    return isinstance(value, bool)


def template(data: Any) -> Any:
    """Build checks from a serializer's defaults, never replace stored values."""
    if isinstance(data, dict):
        return {key: template(value) for key, value in data.items()}
    if isinstance(data, list):
        return (
            tuple(template(item) for item in data)
            if data
            else lambda value: isinstance(value, list)
        )
    if data is None:
        return optional(number)
    if isinstance(data, bool):
        return boolean
    if isinstance(data, str):
        return text
    return number


def typed_schema(annotation: Any) -> Any:
    """Validate persisted dataclass fields using their existing Python types."""
    import types
    from typing import get_args, get_origin

    origin, args = get_origin(annotation), get_args(annotation)
    if annotation is Any:

        def any_value(value):
            finite_tree(value)
            return True

        return any_value
    if origin is types.UnionType:

        def union(value):
            for arg in args:
                try:
                    validate(value, typed_schema(arg))
                    return True
                except (ValueError, TypeError):
                    pass
            return False

        return union
    if origin is dict:
        return {"*": typed_schema(args[1])}
    if origin is list:
        return [typed_schema(args[0])]
    if annotation is float:
        return number
    if annotation is int:
        return lambda v: type(v) is int
    if annotation is type(None):
        return lambda v: v is None
    if annotation is bool:
        return boolean
    if annotation is str:
        return text
    return dataclass_schema(annotation)


def dataclass_schema(cls: type) -> dict[str, Any]:
    from dataclasses import MISSING, fields
    from typing import get_type_hints

    hints = get_type_hints(cls)
    try:
        names = cls().as_dict()
    except TypeError:
        names = hints
    schema = RecordSchema(
        {f.name: typed_schema(hints[f.name]) for f in fields(cls) if f.name in names}
    )
    schema.required = {
        f.name
        for f in fields(cls)
        if f.name in names and f.default is MISSING and f.default_factory is MISSING
    }
    # RLS matrices have fixed dimensions, unlike history/event lists.
    if "theta" in schema and "p" in schema:
        schema["theta"] = (number, number, number)
        schema["p"] = ((number, number, number),) * 3
    return schema


def checked(data: Any, schema: Any) -> dict[str, Any]:
    """Pure fallback for standalone deserializers; callers retain rejected raw data."""
    if data is None:
        return {}
    try:
        validate(data, schema)
    except (ValueError, TypeError, OverflowError):
        return {}
    return data


class RecordSchema(dict):
    """Required constructor fields of an existing serialized dataclass."""

    required: set[str]


def checked_fields(data: Any, schema: dict[str, Any]) -> dict[str, Any]:
    """Keep usable independent parameter fields in standalone loaders."""
    if not isinstance(data, dict):
        return {}
    result = {}
    for key, value in data.items():
        if key not in schema:
            continue
        try:
            validate(value, schema[key])
        except (ValueError, TypeError, OverflowError):
            continue
        result[key] = value
    return result


def required_mapping(schema: dict[str, Any], *keys: str) -> RecordSchema:
    result = RecordSchema(schema)
    result.required = set(keys)
    return result
