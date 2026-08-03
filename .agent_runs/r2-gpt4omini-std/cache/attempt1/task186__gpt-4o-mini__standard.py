import ast

def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source code") from e

    complexities = []

    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None
            self.complexity = 0

        def visit_FunctionDef(self, node: ast.FunctionDef):
            self.current_function = (node.name, node.lineno)
            self.complexity = 1  # Start with base complexity
            self.generic_visit(node)
            complexities.append((self.current_function[0], self.current_function[1], self.complexity))

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            self.current_function = (node.name, node.lineno)
            self.complexity = 1  # Start with base complexity
            self.generic_visit(node)
            complexities.append((self.current_function[0], self.current_function[1], self.complexity))

        def visit_If(self, node: ast.If):
            self.complexity += 1
            self.generic_visit(node)

        def visit_For(self, node: ast.For):
            self.complexity += 1
            self.generic_visit(node)

        def visit_AsyncFor(self, node: ast.AsyncFor):
            self.complexity += 1
            self.generic_visit(node)

        def visit_While(self, node: ast.While):
            self.complexity += 1
            self.generic_visit(node)

        def visit_Try(self, node: ast.Try):
            self.generic_visit(node)

        def visit_ExceptHandler(self, node: ast.ExceptHandler):
            self.complexity += 1
            self.generic_visit(node)

        def visit_IfExp(self, node: ast.IfExp):
            self.complexity += 1
            self.generic_visit(node)

        def visit_ListComp(self, node: ast.ListComp):
            self.complexity += len(node.ifs)
            self.generic_visit(node)

        def visit_SetComp(self, node: ast.SetComp):
            self.complexity += len(node.ifs)
            self.generic_visit(node)

        def visit_DictComp(self, node: ast.DictComp):
            self.complexity += len(node.ifs)
            self.generic_visit(node)

        def visit_GeneratorExp(self, node: ast.GeneratorExp):
            self.complexity += len(node.ifs)
            self.generic_visit(node)

        def visit_BoolOp(self, node: ast.BoolOp):
            self.complexity += len(node.values) - 1
            self.generic_visit(node)

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    return sorted(complexities, key=lambda x: (x[1], x[0]))
