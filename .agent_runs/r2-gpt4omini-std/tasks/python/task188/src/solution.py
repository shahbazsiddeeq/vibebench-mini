import ast

def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    untyped_functions = []

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if not self.is_fully_annotated(node):
                untyped_functions.append((node.name, node.lineno))
            self.generic_visit(node)

        def is_fully_annotated(self, node: ast.FunctionDef) -> bool:
            if node.returns is None:
                return False
            
            # Check parameters
            for i, arg in enumerate(node.args.args):
                if i == 0 and self.is_method(node) and arg.arg in ('self', 'cls'):
                    continue
                if arg.annotation is None:
                    return False
            
            # Check *args and **kwargs
            if node.args.vararg and node.args.vararg.annotation is None:
                return False
            if node.args.kwarg and node.args.kwarg.annotation is None:
                return False
            
            return True

        def is_method(self, node: ast.FunctionDef) -> bool:
            return isinstance(node.parent, ast.ClassDef)

    # Set parent for each node to check if it's a method
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    FunctionVisitor().visit(tree)
    return sorted(untyped_functions, key=lambda x: (x[1], x[0]))
