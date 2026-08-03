import ast
from typing import Any


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    """
    Parse Python source and find duplicate constant keys in dict literals.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of (line_number, key_value) tuples for duplicate keys,
        sorted by (line_number, repr(key_value))
        
    Raises:
        ValueError: If source is not valid Python
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    results = []
    
    # Walk through all nodes in the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            # Process this dict literal
            duplicates = _find_duplicates_in_dict(node)
            results.extend(duplicates)
    
    # Sort by (lineno, repr(key_value))
    results.sort(key=lambda x: (x[0], repr(x[1])))
    
    return results


def _find_duplicates_in_dict(dict_node: ast.Dict) -> list[tuple[int, Any]]:
    """
    Find duplicate constant keys within a single dict node.
    
    Args:
        dict_node: An ast.Dict node
        
    Returns:
        List of (line_number, key_value) tuples for duplicates in this dict
    """
    # Track keys by (type, value) to ensure type-sensitive comparison
    # Map from (type, value) to count
    key_counts: dict[tuple[type, Any], int] = {}
    
    # Track which keys are duplicates (by their actual value)
    duplicate_keys: set[tuple[type, Any]] = set()
    
    for key_node in dict_node.keys:
        # Skip None keys (from **mapping unpacking)
        if key_node is None:
            continue
        
        # Only consider ast.Constant nodes
        if not isinstance(key_node, ast.Constant):
            continue
        
        key_value = key_node.value
        key_type = type(key_value)
        
        # Create a hashable key that includes type information
        # We need to handle unhashable types carefully
        try:
            type_value_key = (key_type, key_value)
            
            # Count occurrences
            if type_value_key in key_counts:
                key_counts[type_value_key] += 1
                duplicate_keys.add(type_value_key)
            else:
                key_counts[type_value_key] = 1
        except TypeError:
            # If the value is unhashable (e.g., list, dict), skip it
            # Constants in ast.Constant should be hashable, but be defensive
            continue
    
    # Build result list with line numbers
    results = []
    for (key_type, key_value) in duplicate_keys:
        # Use the line number of the dict node itself
        lineno = dict_node.lineno
        results.append((lineno, key_value))
    
    return results
