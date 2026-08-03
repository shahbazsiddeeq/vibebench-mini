import ast

def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    """
    Parses a string of Python source with the ast module and returns, for every
    dict display literal ({...}), the constant keys that appear more than once
    inside that same dict.

    Only literal constant keys are considered (ast.Constant: numbers, strings,
    bytes, None, True, False); keys that are variables, attribute accesses,
    calls, tuples, or any other computed expression are ignored, and
    `**mapping` unpacking entries (whose key node is None) are skipped.

    Two keys are treated as duplicates only when their constant values are
    equal under Python `==` AND have the same Python type, so within one dict
    the keys 1 (int), 1.0 (float), and True (bool) are all considered distinct
    and are NOT duplicates of each other.

    For each dict, every key that is duplicated is reported exactly once as a
    tuple (lineno, key_value) where lineno is the 1-based line of the
    enclosing dict display and key_value is the literal value of the key.

    Dicts nested inside other dicts, lists, function bodies, or comprehensions
    are each analysed on their own. Detection is by real parsing, so a dict
    written inside a string literal or comment is ignored.

    The result is sorted ascending by (lineno, repr(key_value)).

    Raises ValueError if source is not valid Python (ast.parse raises SyntaxError).

    Example:
    find_duplicate_dict_keys("d = {'a': 1, 'b': 2, 'a': 3}") -> [(1, 'a')]
    because the key 'a' occurs twice on line 1.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Source is not valid Python") from e

    duplicates = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            seen_keys = {}  # Stores (value, type) -> count
            current_dict_duplicates = set() # Stores (value, type) for keys already identified as duplicates

            for i, key_node in enumerate(node.keys):
                if key_node is None:  # Skip **mapping unpacking entries
                    continue

                if isinstance(key_node, ast.Constant):
                    key_value = key_node.value
                    key_type = type(key_value)
                    key_identifier = (key_value, key_type)

                    if key_identifier in seen_keys:
                        if key_identifier not in current_dict_duplicates:
                            duplicates.append((node.lineno, key_value))
                            current_dict_duplicates.add(key_identifier)
                    else:
                        seen_keys[key_identifier] = 1

    # Sort the results as required: ascending by (lineno, repr(key_value))
    duplicates.sort(key=lambda x: (x[0], repr(x[1])))

    return duplicates
