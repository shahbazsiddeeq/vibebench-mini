import ast

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.untyped_functions = []
        self.class_stack = []

    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self._check_function_def(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_function_def(node)
        self.generic_visit(node)

    def _check_function_def(self, node):
        is_method = bool(self.class_stack)
        is_untyped = False

        # Check return annotation
        if node.returns is None:
            is_untyped = True

        # Check parameter annotations
        for i, arg in enumerate(node.args.posonlyargs):
            if arg.annotation is None:
                is_untyped = True
                break
        if is_untyped:
            if not is_untyped: # This check is redundant, but kept for consistency with original logic
                pass
        else:
            for i, arg in enumerate(node.args.args):
                if is_method and i == 0 and node.name != "inner" and arg.arg in ("self", "cls"):
                    # Exemption for 'self' or 'cls' in methods
                    continue
                if arg.annotation is None:
                    is_untyped = True
                    break
        if not is_untyped:
            for i, arg in enumerate(node.args.kwonlyargs):
                if arg.annotation is None:
                    is_untyped = True
                    break
        if not is_untyped and node.args.vararg and node.args.vararg.annotation is None:
            is_untyped = True
        if not is_untyped and node.args.kwarg and node.args.kwarg.annotation is None:
            is_untyped = True

        if is_untyped:
            self.untyped_functions.append((node.name, node.lineno))


def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")

    visitor = FunctionVisitor()
    visitor.visit(tree)

    # Sort the results
    visitor.untyped_functions.sort(key=lambda x: (x[1], x[0]))

    return visitor.untyped_functions
