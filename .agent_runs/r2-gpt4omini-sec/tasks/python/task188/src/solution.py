import ast
from typing import List, Tuple

def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    untyped_functions = []

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            # Check for return annotation
            has_return_annotation = node.returns is not None
            
            # Check for parameter annotations
            has_param_annotations = all(
                isinstance(arg.annotation, ast.AST) for arg in node.args.args
            )
            
            # Check for the exemption of 'self' or 'cls'
            is_method = isinstance(node.parent, ast.ClassDef)
            exempt_first_param = is_method and len(node.args.args) > 0 and node.args.args[0].arg in ('self', 'cls')
            
            # If the first parameter is exempt, we check the rest
            if exempt_first_param:
                has_param_annotations = all(
                    isinstance(arg.annotation, ast.AST) for arg in node.args.args[1:]
                )
            
            # If either return or parameter annotations are missing, record the function
            if not has_return_annotation or not has_param_annotations:
                untyped_functions.append((node.name, node.lineno))
            
            self.generic_visit(node)

    # Set parent attribute for each node
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    FunctionVisitor().visit(tree)

    # Sort the results by line number and function name
    untyped_functions.sort(key=lambda x: (x[1], x[0]))
    return untyped_functions
