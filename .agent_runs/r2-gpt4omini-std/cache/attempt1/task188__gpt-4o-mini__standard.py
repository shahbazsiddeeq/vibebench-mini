import ast

def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    untyped_functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not is_fully_annotated(node):
                untyped_functions.append((node.name, node.lineno))

    return sorted(untyped_functions)

def is_fully_annotated(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not ast.get_docstring(node):
        return False

    # Check return annotation
    if node.returns is None:
        return False

    # Check parameters
    for i, arg in enumerate(node.args.args):
        if i == 0 and is_method(node) and arg.arg in ('self', 'cls'):
            continue  # Skip self or cls for the first parameter
        if arg.annotation is None:
            return False

    # Check *args and **kwargs
    if node.args.vararg and node.args.vararg.annotation is None:
        return False
    if node.args.kwarg and node.args.kwarg.annotation is None:
        return False

    return True

def is_method(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return isinstance(node.parent, ast.ClassDef)

# To allow access to the parent node
def set_parents(node):
    for child in ast.iter_child_nodes(node):
        child.parent = node
        set_parents(child)

# Set parent references for the AST nodes
def parse_with_parents(source: str):
    tree = ast.parse(source)
    set_parents(tree)
    return tree
