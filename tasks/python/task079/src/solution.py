from __future__ import annotations

_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
}


def validate(data: dict, schema: dict) -> list[str]:
    errors = []
    for key in schema.get("required", []):
        if key not in data:
            errors.append(f"missing required key: '{key}'")
    for key, type_name in schema.get("types", {}).items():
        if key in data:
            expected = _TYPE_MAP.get(type_name)
            if expected and not isinstance(data[key], expected):
                errors.append(
                    f"'{key}' expected {type_name}, got {type(data[key]).__name__}"
                )
    return errors
