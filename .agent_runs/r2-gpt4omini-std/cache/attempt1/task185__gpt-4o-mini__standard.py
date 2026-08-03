import ast

def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    mutable_defaults = []
    
    class MutableDefaultVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            has_mutable_default = False
            
            # Check all arguments for mutable defaults
            for arg in node.args.args:
                if arg.default and self.is_mutable(arg.default):
                    has_mutable_default = True
                    break
            
            # Check keyword-only arguments
            for kwarg in node.args.kwarg:
                if kwarg.default and self.is_mutable(kwarg.default):
                    has_mutable_default = True
                    break
            
            if has_mutable_default:
                mutable_defaults.append((node.name, node.lineno))
            
            self.generic_visit(node)

        def is_mutable(self, node):
            return isinstance(node, (ast.List, ast.Dict, ast.Set))

    visitor = MutableDefaultVisitor()
    visitor.visit(tree)

    # Sort results by line number and function name
    mutable_defaults.sort(key=lambda x: (x[1], x[0]))
    return mutable_defaults
