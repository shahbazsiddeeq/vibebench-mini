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
            self.current_class = node
            self.generic_visit(node)
            self.current_class = None

        def visit_FunctionDef(self, node: ast.FunctionDef):
            if self.is_untyped_function(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            if self.is_untyped_function(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def is_untyped_function(self, node: ast.FunctionDef) -> bool:
            if node.returns is None:
                return True

            exempt_first_param = (
                self.current_class is not None and
                node.args.args and
                node.args.args[0].arg in {'self', 'cls'}
            )

            for i, arg in enumerate(node.args.args):
                if i == 0 and exempt_first_param:
                    continue
                if arg.annotation is None:
                    return True

            for arg in node.args.kwonlyargs:
                if arg.annotation is None:
                    return True

            if node.args.vararg and node.args.vararg.annotation is None:
                return True

            if node.args.kwarg and node.args.kwarg.annotation is None:
                return True

            return False

    visitor = FunctionVisitor()
    visitor.visit(tree)

    return sorted(untyped_functions, key=lambda x: (x[1], x[0]))
