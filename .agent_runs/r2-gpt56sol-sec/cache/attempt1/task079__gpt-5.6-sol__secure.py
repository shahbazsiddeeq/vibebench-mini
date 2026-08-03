"""A small, dependency-free JSON-style schema validator."""

from typing import Any

_TYPE_MAP: dict[str, type] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
}


def _safe_name(value: Any, limit: int = 200) -> str:
    """Return a bounded, printable description without invoking custom repr."""
    if isinstance(value, str):
        text = value
    elif type(value) in (int, float, bool):
        text = str(value)
    elif value is None:
        text = "None"
    else:
        text = f"<{type(value).__name__}>"

    text = "".join(char if char.isprintable() else "?" for char in text)
    return text if len(text) <= limit else text[:limit] + "..."


def _matches_type(value: Any, expected: type) -> bool:
    # bool is an int subclass, but schemas distinguish "bool" from "int".
    if expected is int:
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, expected)


def validate(data: Any, schema: Any) -> list[str]:
    """Validate a dictionary against required-key and type constraints."""
    errors: list[str] = []

    if not isinstance(schema, dict):
        return ["Schema must be a dict."]
    if not isinstance(data, dict):
        return ["Data must be a dict."]

    required = schema.get("required", [])
    if not isinstance(required, list):
        errors.append("Schema field 'required' must be a list.")
    else:
        seen: set[Any] = set()
        for key in required:
            try:
                if key in seen:
                    continue
                seen.add(key)
                present = key in data
            except (TypeError, ValueError):
                errors.append("Schema contains an invalid required key.")
                continue

            if not present:
                errors.append(f"Missing required key: {_safe_name(key)}")

    type_rules = schema.get("types", {})
    if not isinstance(type_rules, dict):
        errors.append("Schema field 'types' must be a dict.")
    else:
        for key, type_name in type_rules.items():
            expected = _TYPE_MAP.get(type_name) if isinstance(type_name, str) else None
            if expected is None or key not in data:
                continue

            value = data[key]
            if not _matches_type(value, expected):
                errors.append(
                    f"Key {_safe_name(key)} must be of type {type_name}; "
                    f"got {type(value).__name__}."
                )

    return errors
