import ast


def find_bare_excepts(source: str) -> list[int]:
    """
    Parse Python source code and return line numbers of bare except clauses.
    
    A bare except clause is an ast.ExceptHandler with type attribute None,
    written as `except:` without specifying an exception type.
    
    Args:
        source: String containing Python source code
        
    Returns:
        Sorted list of 1-based line numbers where bare except clauses occur
        
    Raises:
        ValueError: If source is not valid Python syntax
    """
    # Validate input type
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    # Collect line numbers of bare except handlers
    bare_except_lines = []
    
    # Walk the AST to find all ExceptHandler nodes
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            # Check if this is a bare except (type is None)
            if node.type is None:
                bare_except_lines.append(node.lineno)
    
    # Return sorted list
    return sorted(bare_except_lines)
