import ast
from typing import Any


def find_duplicate_dict_keys(source: str) -> list[tuple[int, Any]]:
    """
    Parse Python source code and find duplicate constant keys in dict literals.
    
    Returns a list of tuples (lineno, key_value) for each duplicate key found,
    sorted by (lineno, repr(key_value)).
    
    Raises ValueError if source is not valid Python.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    duplicates = []
    
    class DictVisitor(ast.NodeVisitor):
        def visit_Dict(self, node: ast.Dict) -> None:
            # Track keys in this dict: (type, value) -> count
            key_counts = {}
            # Track keys in this dict: (type, value) -> lineno
            key_lineno = {}
            
            for key_node in node.keys:
                # Skip None keys (from **mapping unpacking)
                if key_node is None:
                    continue
                
                # Only consider Constant nodes
                if not isinstance(key_node, ast.Constant):
                    continue
                
                key_value = key_node.value
                key_type = type(key_value)
                key_id = (key_type, key_value)
                
                if key_id not in key_counts:
                    key_counts[key_id] = 0
                    key_lineno[key_id] = node.lineno
                
                key_counts[key_id] += 1
            
            # Collect duplicates from this dict
            for (key_type, key_value), count in key_counts.items():
                if count > 1:
                    lineno = key_lineno[(key_type, key_value)]
                    duplicates.append((lineno, key_value))
            
            # Continue visiting nested nodes
            self.generic_visit(node)
    
    visitor = DictVisitor()
    visitor.visit(tree)
    
    # Sort by (lineno, repr(key_value))
    duplicates.sort(key=lambda x: (x[0], repr(x[1])))
    
    return duplicates
