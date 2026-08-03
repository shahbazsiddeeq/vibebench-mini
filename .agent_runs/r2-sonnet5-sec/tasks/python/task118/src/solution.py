"""
src/solution.py

A small, security-conscious utility module implementing `flatten_dict`.

The function flattens a nested dictionary into a single-level dictionary
whose keys are the paths through the original structure, joined by a
separator string.

Design considerations for safety/robustness:
    * Strict input validation (types are checked explicitly).
    * No use of eval/exec or other dynamic code execution.
    * No I/O performed by this module.
    * Collisions between different nested paths that flatten to the same
      key raise a clear ValueError instead of silently overwriting data.
    * Recursion depth is bounded implicitly by Python's recursion limit;
      malformed/adversarial deeply nested structures will raise a
      RecursionError rather than corrupting state or hanging.
"""

from typing import Any, Dict


def flatten_dict(d: Dict[Any, Any], sep: str = ".") -> Dict[Any, Any]:
    """
    Flatten a nested dictionary into a single-level dictionary.

    Args:
        d: The dictionary to flatten. Must be a dict.
        sep: The separator string used to join nested keys. Must be a
             non-empty string.

    Returns:
        A new dictionary with flattened keys.

    Raises:
        TypeError: If `d` is not a dict or `sep` is not a string.
        ValueError: If `sep` is empty, or if two distinct paths in the
                    nested structure collapse to the same flattened key.
    """
    if not isinstance(d, dict):
        raise TypeError("flatten_dict expects a dict as the first argument")
    if not isinstance(sep, str):
        raise TypeError("sep must be a string")
    if sep == "":
        raise ValueError("sep must be a non-empty string")

    result: Dict[Any, Any] = {}

    def _flatten(current: Dict[Any, Any], prefix: str) -> None:
        # An empty dict is itself a leaf value once we've recursed into it.
        if not current:
            if prefix in result:
                raise ValueError(
                    f"Key collision detected while flattening: '{prefix}'"
                )
            result[prefix] = {}
            return

        for key, value in current.items():
            # Build the new key path; str() ensures joinability, but we
            # avoid silently coercing unusual key types beyond what's needed.
            key_str = str(key)
            new_key = f"{prefix}{sep}{key_str}" if prefix else key_str

            if isinstance(value, dict):
                _flatten(value, new_key)
            else:
                if new_key in result:
                    raise ValueError(
                        f"Key collision detected while flattening: '{new_key}'"
                    )
                result[new_key] = value

    if not d:
        return {}

    _flatten(d, "")
    return result
