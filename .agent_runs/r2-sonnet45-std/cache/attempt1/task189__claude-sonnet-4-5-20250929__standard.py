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
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    # Walk through all nodes in the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            # Process this dict literal
            duplicates = find_duplicates_in_dict(node)
            results.extend(duplicates)
    
    # Sort by (lineno, repr(key_value))
    results.sort(key=lambda x: (x[0], repr(x[1])))
    
    return results


def find_duplicates_in_dict(dict_node: ast.Dict) -> list[tuple[int, Any]]:
    """
    Find duplicate constant keys in a single dict node.
    
    Args:
        dict_node: An ast.Dict node
        
    Returns:
        List of (line_number, key_value) tuples for duplicate keys in this dict
    """
    # Track keys we've seen: map from (type, value) to count
    key_counts = {}
    
    for key in dict_node.keys:
        # Skip **mapping unpacking (key is None)
        if key is None:
            continue
        
        # Only consider constant keys
        if isinstance(key, ast.Constant):
            key_value = key.value
            key_type = type(key_value)
            
            # Use (type, value) as the identifier to ensure type-sensitive comparison
            key_id = (key_type, key_value)
            
            if key_id not in key_counts:
                key_counts[key_id] = 0
            key_counts[key_id] += 1
    
    # Find keys that appear more than once
    duplicates = []
    for (key_type, key_value), count in key_counts.items():
        if count > 1:
            # Report each duplicate key exactly once with the dict's line number
            duplicates.append((dict_node.lineno, key_value))
    
    return duplicates
