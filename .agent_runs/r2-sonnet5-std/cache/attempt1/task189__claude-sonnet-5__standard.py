"""
Duplicate Dict Key Detector
"""

import ast


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    """
    Parse `source` as Python code and find, for every dict display literal,
    the constant keys that appear more than once (using == and type equality).

    Returns a sorted list of (lineno, key_value) tuples.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python source: {exc}") from exc

    results: list[tuple[int, object]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        lineno = node.lineno
        seen_keys = []  # list of (type, value) tuples in order encountered
        counts = {}  # (type, value) -> count
        # We need to map back to a representative value for output.
        key_repr = {}  # (type, value) -> original key_value

        for key_node in node.keys:
            if key_node is None:
                # **mapping unpacking, skip
                continue
            if not isinstance(key_node, ast.Constant):
                continue

            value = key_node.value
            key_type = type(value)
            sig = (key_type, value)

            counts[sig] = counts.get(sig, 0) + 1
            if sig not in key_repr:
                key_repr[sig] = value

        for sig, count in counts.items():
            if count > 1:
                results.append((lineno, key_repr[sig]))

    results.sort(key=lambda item: (item[0], repr(item[1])))
    return results
