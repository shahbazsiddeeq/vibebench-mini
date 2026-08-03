import ast
from typing import List, Tuple

def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.complexities = []

        def visit_FunctionDef(self, node: ast.FunctionDef):
            complexity = 1  # Base complexity
            self.current_lineno = node.lineno
            self.generic_visit(node)
            self.complexities.append((node.name, self.current_lineno, complexity))

        def visit_If(self, node: ast.If):
            self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + 1)
            self.generic_visit(node)

        def visit_For(self, node: ast.For):
            self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + 1)
            self.generic_visit(node)

        def visit_While(self, node: ast.While):
            self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + 1)
            self.generic_visit(node)

        def visit_ExceptHandler(self, node: ast.ExceptHandler):
            self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + 1)
            self.generic_visit(node)

        def visit_BoolOp(self, node: ast.BoolOp):
            complexity_increase = len(node.values) - 1
            self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + complexity_increase)
            self.generic_visit(node)

        def visit_IfExp(self, node: ast.IfExp):
            self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + 1)
            self.generic_visit(node)

        def visit_ListComp(self, node: ast.ListComp):
            if node.ifs:
                self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + len(node.ifs))
            self.generic_visit(node)

        def visit_SetComp(self, node: ast.SetComp):
            if node.ifs:
                self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + len(node.ifs))
            self.generic_visit(node)

        def visit_DictComp(self, node: ast.DictComp):
            if node.ifs:
                self.complexities[-1] = (self.complexities[-1][0], self.complexities[-1][1], self.complexities[-1][2] + len(node.ifs))
            self.generic_visit(node)

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    return sorted(visitor.complexities, key=lambda x: (x[1], x[0]))
