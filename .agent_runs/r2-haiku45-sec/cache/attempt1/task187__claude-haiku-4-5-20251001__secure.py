import ast
from typing import List


def find_bare_excepts(source: str) -> List[int]:
    """
    Parse Python source code and return line numbers of bare except clauses.
    
    A bare except clause is an ast.ExceptHandler with type attribute set to None.
    
    Args:
        source: A string containing Python source code
        
    Returns:
        A sorted list of 1-based line numbers where bare except clauses appear
        
    Raises:
        ValueError: If source is not valid Python
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    bare_except_lines = []
    
    # Walk through all nodes in the AST
    for node in ast.walk(tree):
        # Check if this node is a Try statement
        if isinstance(node, ast.Try):
            # Examine all exception handlers in this try block
            for handler in node.handlers:
                # A bare except has type attribute set to None
                if handler.type is None:
                    bare_except_lines.append(handler.lineno)
    
    # Return sorted list of line numbers
    return sorted(bare_except_lines)
