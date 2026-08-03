import ast

def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    try:
        # Parse the source code into an AST
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    mutable_defaults = []
    function_names = set()

    # Define a visitor class to inspect function definitions
    class FunctionDefVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            # Check for mutable defaults in the function's arguments
            for arg in node.args.args:
                if arg.default and isinstance(arg.default, (ast.List, ast.Dict, ast.Set)):
                    if (node.name, node.lineno) not in function_names:
                        mutable_defaults.append((node.name, node.lineno))
                        function_names.add((node.name, node.lineno))
            # Check for keyword-only arguments
            for kwarg in node.args.kwarg:
                if kwarg.default and isinstance(kwarg.default, (ast.List, ast.Dict, ast.Set)):
                    if (node.name, node.lineno) not in function_names:
                        mutable_defaults.append((node.name, node.lineno))
                        function_names.add((node.name, node.lineno))
            # Continue visiting other nodes
            self.generic_visit(node)

    # Create a visitor instance and visit the AST
    visitor = FunctionDefVisitor()
    visitor.visit(tree)

    # Sort the results by line number and function name
    mutable_defaults.sort(key=lambda x: (x[1], x[0]))
    return mutable_defaults
