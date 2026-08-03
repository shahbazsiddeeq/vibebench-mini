import ast
from typing import Any


def find_duplicate_dict_keys(source: str) -> list[tuple[int, Any]]:
    """
    Parse Python source code and find duplicate constant keys in dict literals.
    
    Returns a sorted list of (lineno, key_value) tuples for each duplicate key found.
    Raises ValueError if source is not valid Python.
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    duplicates = []
    
    # Walk through all nodes in the AST
    for node in ast.walk(tree):
        # Only process Dict nodes
        if isinstance(node, ast.Dict):
            # Track keys by (type, value) to handle type-sensitive comparison
            key_counts = {}
            key_lines = {}
            
            for key_node in node.keys:
                # Skip None keys (from **mapping unpacking)
                if key_node is None:
                    continue
                
                # Only process Constant nodes
                if not isinstance(key_node, ast.Constant):
                    continue
                
                key_value = key_node.value
                # Create a type-sensitive key: (type, value)
                type_sensitive_key = (type(key_value), key_value)
                
                # Count occurrences
                if type_sensitive_key not in key_counts:
                    key_counts[type_sensitive_key] = 0
                    key_lines[type_sensitive_key] = node.lineno
                
                key_counts[type_sensitive_key] += 1
            
            # Find duplicates (count > 1)
            for (key_type, key_value), count in key_counts.items():
                if count > 1:
                    lineno = key_lines[(key_type, key_value)]
                    duplicates.append((lineno, key_value))
    
    # Sort by (lineno, repr(key_value))
    duplicates.sort(key=lambda x: (x[0], repr(x[1])))
    
    return duplicates
