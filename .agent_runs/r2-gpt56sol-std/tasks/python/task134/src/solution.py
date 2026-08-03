import ast
import re

_SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")


def non_snake_case_functions(source: str) -> list[str]:
    """Return non-snake-case function names in source order."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(str(exc)) from exc

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    functions.sort(key=lambda node: (node.lineno, node.col_offset))

    return [
        node.name
        for node in functions
        if _SNAKE_CASE.fullmatch(node.name) is None
    ]
