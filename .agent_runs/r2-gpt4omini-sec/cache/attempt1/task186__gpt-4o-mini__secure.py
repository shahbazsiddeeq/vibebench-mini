import ast
from typing import List, Tuple

def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    complexities = []

    class ComplexityVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            complexity = 1  # Base complexity
            self.generic_visit(node)  # Visit the body to calculate complexity
            complexities.append((node.name, node.lineno, complexity))

        def visit_If(self, node: ast.If):
            nonlocal complexity
            complexity += 1  # Count the if statement
            self.generic_visit(node)  # Visit the body of the if
            for elif_node in node.orelse:
                if isinstance(elif_node, ast.If):
                    complexity += 1  # Count elif as an if

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
            for handler in node.handlers:
                complexity += 1  # Count each except handler
            self.generic_visit(node)

        def visit_IfExp(self, node: ast.IfExp):
            nonlocal complexity
            complexity += 1  # Count the ternary if
            self.generic_visit(node)

        def visit_ListComp(self, node: ast.ListComp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if-clause in comprehension
            self.generic_visit(node)

        def visit_SetComp(self, node: ast.SetComp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if-clause in comprehension
            self.generic_visit(node)

        def visit_DictComp(self, node: ast.DictComp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if-clause in comprehension
            self.generic_visit(node)

        def visit_GeneratorExp(self, node: ast.GeneratorExp):
            nonlocal complexity
            for if_clause in node.ifs:
                complexity += 1  # Count each if-clause in comprehension
            self.generic_visit(node)

        def visit_BoolOp(self, node: ast.BoolOp):
            nonlocal complexity
            complexity += len(node.values) - 1  # Count operands - 1
            self.generic_visit(node)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = 1  # Reset complexity for each function
            ComplexityVisitor().visit(node)

    return sorted(complexities, key=lambda x: (x[1], x[0]))
