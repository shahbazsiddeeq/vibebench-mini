import ast


def estimate_complexity(func_source: str) -> dict:
    """
    Parse a Python function source and return complexity metrics.
    
    Returns a dict with:
    - "lines": number of non-blank lines
    - "branches": number of decision points (If, For, While, ExceptHandler nodes)
    - "returns": number of return statements
    
    Raises ValueError if source is empty, unparseable, or doesn't define exactly one function.
    """
    
    # Check if source is empty
    if not func_source or not func_source.strip():
        raise ValueError("Source code is empty")
    
    # Try to parse the source
    try:
        tree = ast.parse(func_source)
    except SyntaxError:
        raise ValueError("Source code cannot be parsed")
    
    # Check that there's exactly one top-level function definition
    top_level_functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    
    if len(top_level_functions) != 1:
        raise ValueError("Source must define exactly one top-level function")
    
    func_def = top_level_functions[0]
    
    # Count non-blank lines
    lines = [line for line in func_source.split('\n') if line.strip()]
    line_count = len(lines)
    
    # Count branches and returns by walking the function body
    branch_count = 0
    return_count = 0
    
    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.branches = 0
            self.returns = 0
        
        def visit_If(self, node):
            self.branches += 1
            self.generic_visit(node)
        
        def visit_For(self, node):
            self.branches += 1
            self.generic_visit(node)
        
        def visit_While(self, node):
            self.branches += 1
            self.generic_visit(node)
        
        def visit_ExceptHandler(self, node):
            self.branches += 1
            self.generic_visit(node)
        
        def visit_Return(self, node):
            self.returns += 1
            self.generic_visit(node)
    
    visitor = ComplexityVisitor()
    visitor.visit(func_def)
    
    return {
        "lines": line_count,
        "branches": visitor.branches,
        "returns": visitor.returns
    }
