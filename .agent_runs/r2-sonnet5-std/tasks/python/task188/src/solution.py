"""
Missing Type Annotation Detector
"""

import ast


def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}") from e

    results: list[tuple[str, int]] = []
    # stack holds 'class' or 'function' markers for enclosing scopes
    stack: list[str] = []

    def is_fully_annotated(node: ast.AST, is_method: bool) -> bool:
        args = node.args

        # Return annotation required
        if node.returns is None:
            return False

        posonly = list(args.posonlyargs)
        regular = list(args.args)
        combined_positional = posonly + regular

        first_param = combined_positional[0] if combined_positional else None

        for arg in combined_positional:
            if (
                is_method
                and arg is first_param
                and arg.arg in ("self", "cls")
            ):
                continue
            if arg.annotation is None:
                return False

        for arg in args.kwonlyargs:
            if arg.annotation is None:
                return False

        if args.vararg is not None:
            if args.vararg.annotation is None:
                return False

        if args.kwarg is not None:
            if args.kwarg.annotation is None:
                return False

        return True

    def visit(node: ast.AST) -> None:
        if isinstance(node, ast.ClassDef):
            stack.append("class")
            for child in ast.iter_child_nodes(node):
                visit(child)
            stack.pop()
            return

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            is_method = bool(stack) and stack[-1] == "class"
            if not is_fully_annotated(node, is_method):
                results.append((node.name, node.lineno))

            stack.append("function")
            for child in ast.iter_child_nodes(node):
                visit(child)
            stack.pop()
            return

        # For all other nodes, just recurse into children
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)

    results.sort(key=lambda item: (item[1], item[0]))
    return results
