import ast

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

def estimate_complexity(func_source: str) -> dict:
    if not func_source:
        raise ValueError("Source cannot be empty.")

    # Calculate lines
    lines = 0
    for line in func_source.splitlines():
        if line.strip():
            lines += 1

    try:
        tree = ast.parse(func_source)
    except SyntaxError as e:
        raise ValueError(f"Cannot parse source: {e}")

    function_nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)]

    if len(function_nodes) != 1:
        raise ValueError("Source must define exactly one top-level function.")

    visitor = ComplexityVisitor()
    visitor.visit(function_nodes[0])

    return {"lines": lines, "branches": visitor.branches, "returns": visitor.returns}
