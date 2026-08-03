import json
import math
import os
from typing import Any, Union

import yaml


def _normalize_non_json_values(value: Any) -> Any:
    """Convert values without a native JSON representation to strings."""
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)

    if isinstance(value, list):
        return [_normalize_non_json_values(item) for item in value]

    if isinstance(value, dict):
        return {
            key: _normalize_non_json_values(item)
            for key, item in value.items()
        }

    return str(value)


def yaml_to_json(path: Union[str, os.PathLike[str]]) -> str:
    """Read a UTF-8 YAML file and return its compact, sorted JSON form."""
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or path-like object")

    with open(path, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)

    return json.dumps(
        _normalize_non_json_values(data),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
