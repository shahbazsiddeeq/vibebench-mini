"""
A simple, security-conscious JSON-like schema validator.

The schema is expected to be a dict optionally containing:
    - "required": a list of key names that must be present in `data`.
    - "types": a dict mapping key name -> type name string. Valid type
      name strings are "str", "int", "float", "bool", "list", "dict".

The validator never uses eval/exec and never trusts external input
blindly: all inputs are checked for expected shape before use, and
any unexpected/malformed schema data is simply ignored rather than
raising an exception that could leak internal details.
"""

from typing import Any, Dict, List

# Mapping of allowed type name strings to actual Python types.
_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
}


def validate(data: Any, schema: Any) -> List[str]:
    """
    Validate `data` against `schema`.

    Returns a list of human-readable error message strings. An empty
    list means `data` is valid according to `schema`.

    This function is defensive: it does not assume `data` or `schema`
    are well-formed. Malformed schema entries are ignored rather than
    causing exceptions.
    """
    errors: List[str] = []

    # If data is not a dict, we cannot meaningfully check keys/types.
    if not isinstance(data, dict):
        errors.append("Invalid data: expected a JSON object (dict).")
        return errors

    # If schema is not a dict, there is nothing sensible to validate against.
    if not isinstance(schema, dict):
        errors.append("Invalid schema: expected a dict.")
        return errors

    # --- Required keys check ---
    required = schema.get("required", [])
    if isinstance(required, (list, tuple)):
        for key in required:
            # Only handle string keys sensibly; ignore anything else.
            if not isinstance(key, str):
                continue
            if key not in data:
                errors.append(f"Missing required field: '{key}'")
    # If "required" is present but not a list/tuple, silently ignore
    # (malformed schema should not crash validation).

    # --- Type checks ---
    types_spec = schema.get("types", {})
    if isinstance(types_spec, dict):
        for key, type_name in types_spec.items():
            if not isinstance(key, str):
                continue
            if key not in data:
                # Only check types for keys that are actually present.
                continue
            if not isinstance(type_name, str):
                # Unknown/malformed type spec; ignore.
                continue
            expected_type = _TYPE_MAP.get(type_name)
            if expected_type is None:
                # Unknown type_name values are ignored per spec.
                continue

            value = data[key]

            # Special-case bool vs int: bool is a subclass of int in
            # Python, so we need explicit handling to keep the checks
            # intuitive and consistent with the declared type name.
            if type_name == "int" and isinstance(value, bool):
                errors.append(
                    f"Field '{key}' expected type 'int' but got 'bool'"
                )
                continue
            if type_name == "bool" and not isinstance(value, bool):
                errors.append(
                    f"Field '{key}' expected type 'bool' but got "
                    f"'{type(value).__name__}'"
                )
                continue

            if not isinstance(value, expected_type):
                errors.append(
                    f"Field '{key}' expected type '{type_name}' but got "
                    f"'{type(value).__name__}'"
                )
    # If "types" is present but not a dict, silently ignore.

    return errors
