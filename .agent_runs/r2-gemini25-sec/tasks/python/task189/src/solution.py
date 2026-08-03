import ast
from collections import defaultdict


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    """
    Parses a string of Python source with the ast module and returns, for every dict
    display literal ({...}), the constant keys that appear more than once inside that
    same dict.

    Only literal constant keys are considered (ast.Constant: numbers, strings, bytes,
    None, True, False); keys that are variables, attribute accesses, calls, tuples,
    or any other computed expression are ignored, and `**mapping` unpacking entries
    (whose key node is None) are skipped.

    Two keys are treated as duplicates only when their constant values are equal under
    Python `==` AND have the same Python type, so within one dict the keys 1 (int),
    1.0 (float), and True (bool) are all considered distinct and are NOT duplicates
    of each other.

    For each dict, every key that is duplicated is reported exactly once as a tuple
    (lineno, key_value) where lineno is the 1-based line of the enclosing dict display
    and key_value is the literal value of the key.

    Dicts nested inside other dicts, lists, function bodies, or comprehensions are
    each analysed on their own. Detection is by real parsing, so a dict written inside
    a string literal or comment is ignored.

    The result is sorted ascending by (lineno, repr(key_value)).

    Raises ValueError if source is not valid Python (ast.parse raises SyntaxError).

    Args:
        source: The Python source code as a string.

    Returns:
        A list of tuples, where each tuple contains the 1-based line number of the
        dict display and the literal value of the duplicated key.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}") from e

    duplicates: list[tuple[int, object]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            # Use a defaultdict to store counts of (value, type) tuples
            # This correctly handles 1 (int), 1.0 (float), True (bool) as distinct
            key_counts: defaultdict[tuple[object, type], int] = defaultdict(int)
            reported_keys_for_this_dict: set[tuple[object, type]] = set()

            for key_node in node.keys:
                if key_node is None:  # Skip **mapping unpacking entries
                    continue

                if isinstance(key_node, ast.Constant):
                    key_value = key_node.value
                    key_type = type(key_value)
                    key_tuple = (key_value, key_type)

                    key_counts[key_tuple] += 1

                    if key_counts[key_tuple] > 1 and key_tuple not in reported_keys_for_this_dict:
                        duplicates.append((node.lineno, key_value))
                        reported_keys_for_this_dict.add(key_tuple)

    # Sort the results as required: ascending by (lineno, repr(key_value))
    duplicates.sort(key=lambda x: (x[0], repr(x[1])))

    return duplicates
