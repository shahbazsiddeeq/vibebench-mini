import ast

def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    mutable_defaults = []

    class FunctionDefVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            # Check for mutable defaults in the function's arguments
            for arg in node.args.args:
                if arg.default and isinstance(arg.default, (ast.List, ast.Dict, ast.Set)):
                    mutable_defaults.append((node.name, node.lineno))
                    break  # Only report once per function
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            # Similar check for async functions
            for arg in node.args.args:
                if arg.default and isinstance(arg.default, (ast.List, ast.Dict, ast.Set)):
                    mutable_defaults.append((node.name, node.lineno))
                    break  # Only report once per function
            self.generic_visit(node)

    visitor = FunctionDefVisitor()
    visitor.visit(tree)

    # Sort results by line number and function name
    mutable_defaults.sort(key=lambda x: (x[1], x[0]))
    return mutable_defaults
