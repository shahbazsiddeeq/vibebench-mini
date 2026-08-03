import ast

def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    functions = []

    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node):
            self._visit_function(node)

        def visit_AsyncFunctionDef(self, node):
            self._visit_function(node)

        def _visit_function(self, node):
            if self.current_function is not None:
                # Skip nested functions
                return

            self.current_function = node
            complexity = 1  # Base complexity

            # Visit the body of the function
            for stmt in node.body:
                complexity += self._calculate_complexity(stmt)

            functions.append((node.name, node.lineno, complexity))
            self.current_function = None

        def _calculate_complexity(self, node):
            complexity = 0
            if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.IfExp):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in node.generators:
                    if generator.ifs:
                        complexity += len(generator.ifs)

            # Recursively calculate complexity for child nodes
            for child in ast.iter_child_nodes(node):
                complexity += self._calculate_complexity(child)

            return complexity

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    return sorted(functions, key=lambda x: (x[1], x[0]))
