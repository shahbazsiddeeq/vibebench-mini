import ast

def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    untyped_functions = []

    class FunctionVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_class = None

        def visit_ClassDef(self, node):
            self.current_class = node
            self.generic_visit(node)
            self.current_class = None

        def visit_FunctionDef(self, node):
            if not self.is_fully_annotated(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            if not self.is_fully_annotated(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def is_fully_annotated(self, node):
            # Check return annotation
            if node.returns is None:
                return False

            # Check parameter annotations
            for i, arg in enumerate(node.args.args):
                if i == 0 and self.current_class and arg.arg in {'self', 'cls'}:
                    continue
                if arg.annotation is None:
                    return False

            # Check positional-only parameters
            for arg in node.args.posonlyargs:
                if arg.annotation is None:
                    return False

            # Check varargs (*args)
            if node.args.vararg and node.args.vararg.annotation is None:
                return False

            # Check keyword-only parameters
            for arg in node.args.kwonlyargs:
                if arg.annotation is None:
                    return False

            # Check kwargs (**kwargs)
            if node.args.kwarg and node.args.kwarg.annotation is None:
                return False

            return True

    FunctionVisitor().visit(tree)
    return sorted(untyped_functions, key=lambda x: (x[1], x[0]))
