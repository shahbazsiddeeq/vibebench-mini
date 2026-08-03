import ast
from typing import List, Tuple

def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    untyped_functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_name = node.name
            lineno = node.lineno
            has_return_annotation = node.returns is not None
            parameters = node.args.args
            has_untyped_parameters = False

            # Check if the function is a method
            is_method = any(isinstance(parent, ast.ClassDef) for parent in ast.iter_parent_nodes(node))

            for i, param in enumerate(parameters):
                if i == 0 and is_method and param.arg in ('self', 'cls'):
                    continue  # Skip the first parameter if it's self or cls
                if param.annotation is None:
                    has_untyped_parameters = True
                    break

            if has_untyped_parameters or not has_return_annotation:
                untyped_functions.append((function_name, lineno))

    return sorted(untyped_functions)
