import ast


def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    """Return functions missing a return or parameter annotation."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    results: list[tuple[str, int]] = []

    class AnnotationVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[ast.AST] = []

        def visit(self, node: ast.AST):
            self.stack.append(node)
            try:
                return super().visit(node)
            finally:
                self.stack.pop()

        def inspect_function(
            self, node: ast.FunctionDef | ast.AsyncFunctionDef
        ) -> None:
            parent = self.stack[-2] if len(self.stack) >= 2 else None
            is_direct_method = isinstance(parent, ast.ClassDef)

            positional = node.args.posonlyargs + node.args.args
            missing_annotation = node.returns is None

            for index, argument in enumerate(positional):
                exempt = (
                    is_direct_method
                    and index == 0
                    and argument.arg in {"self", "cls"}
                )
                if not exempt and argument.annotation is None:
                    missing_annotation = True

            for argument in node.args.kwonlyargs:
                if argument.annotation is None:
                    missing_annotation = True

            if node.args.vararg is not None and node.args.vararg.annotation is None:
                missing_annotation = True

            if node.args.kwarg is not None and node.args.kwarg.annotation is None:
                missing_annotation = True

            if missing_annotation:
                results.append((node.name, node.lineno))

            self.generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.inspect_function(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.inspect_function(node)

    AnnotationVisitor().visit(tree)
    return sorted(results, key=lambda item: (item[1], item[0]))
