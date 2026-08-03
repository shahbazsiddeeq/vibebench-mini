import ast
from typing import List, Tuple

def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    functions = []

    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node: ast.FunctionDef):
            self._process_function(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            self._process_function(node)

        def _process_function(self, node):
            if self.current_function is not None:
                # Skip nested functions
                return

            self.current_function = node
            complexity = 1  # Base complexity
            complexity += self._calculate_complexity(node)
            functions.append((node.name, node.lineno, complexity))
            self.current_function = None

        def _calculate_complexity(self, node):
            complexity = 0
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
                elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                    complexity += sum(1 for gen in child.generators if gen.ifs)
                elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                    continue  # Skip nested functions, lambdas, and classes
                complexity += self._calculate_complexity(child)
            return complexity

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    return sorted(functions, key=lambda x: (x[1], x[0]))
