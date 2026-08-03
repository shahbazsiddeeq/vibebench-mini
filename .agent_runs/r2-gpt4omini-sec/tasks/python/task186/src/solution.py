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
            self.generic_visit(node)  # Visit the body to calculate complexity
            self.complexities.append((node.name, node.lineno, complexity))

        def visit_If(self, node: ast.If):
            nonlocal complexity
            complexity += 1  # Count the if
            self.generic_visit(node)  # Visit the body of the if
            for elif_node in node.orelse:
                if isinstance(elif_node, ast.If):
                    complexity += 1  # Count elif

        def visit_For(self, node: ast.For):
            nonlocal complexity
            complexity += 1  # Count the for loop
            self.generic_visit(node)

        def visit_AsyncFor(self, node: ast.AsyncFor):
            nonlocal complexity
            complexity += 1  # Count the async for loop
            self.generic_visit(node)

        def visit_While(self, node: ast.While):
            nonlocal complexity
            complexity += 1  # Count the while loop
            self.generic_visit(node)

        def visit_Try(self, node: ast.Try):
            nonlocal complexity
            complexity += len(node.handlers)  # Count the number of except handlers
            self.generic_visit(node)

        def visit_IfExp(self, node: ast.IfExp):
            nonlocal complexity
            complexity += 1  # Count the ternary if

        def visit_ListComp(self, node: ast.ListComp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if clause in comprehension
            self.generic_visit(node)

        def visit_SetComp(self, node: ast.SetComp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if clause in comprehension
            self.generic_visit(node)

        def visit_GeneratorExp(self, node: ast.GeneratorExp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if clause in comprehension
            self.generic_visit(node)

        def visit_BoolOp(self, node: ast.BoolOp):
            nonlocal complexity
            complexity += len(node.values) - 1  # Count the number of operands - 1
            self.generic_visit(node)

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    # Sort by line number and function name
    visitor.complexities.sort(key=lambda x: (x[1], x[0]))
    return visitor.complexities
