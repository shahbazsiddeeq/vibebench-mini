import ast
from typing import List, Tuple

def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source") from e

    untyped_functions = []

    class FunctionVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_class = None

        def visit_ClassDef(self, node: ast.ClassDef):
            previous_class = self.current_class
            self.current_class = node
            self.generic_visit(node)
            self.current_class = previous_class

        def visit_FunctionDef(self, node: ast.FunctionDef):
            if not self.is_fully_annotated(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            if not self.is_fully_annotated(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def is_fully_annotated(self, node: ast.FunctionDef) -> bool:
            # Check return annotation
            if node.returns is None:
                return False

            # Check parameter annotations
            for arg in node.args.args:
                if arg.annotation is None:
                    # Exempt 'self' or 'cls' in methods
                    if self.current_class and arg == node.args.args[0] and arg.arg in {'self', 'cls'}:
                        continue
                    return False

            # Check positional-only parameters
            for arg in node.args.posonlyargs:
                if arg.annotation is None:
                    return False

            # Check keyword-only parameters
            for arg in node.args.kwonlyargs:
                if arg.annotation is None:
                    return False

            # Check *args
            if node.args.vararg and node.args.vararg.annotation is None:
                return False

            # Check **kwargs
            if node.args.kwarg and node.args.kwarg.annotation is None:
                return False

            return True

    visitor = FunctionVisitor()
    visitor.visit(tree)

    return sorted(untyped_functions, key=lambda x: (x[1], x[0]))
