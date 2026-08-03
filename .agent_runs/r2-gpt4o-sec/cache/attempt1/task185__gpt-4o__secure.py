import ast
from typing import List, Tuple

def find_mutable_defaults(source: str) -> List[Tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source") from e

    mutable_nodes = (ast.List, ast.Dict, ast.Set)
    results = []

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if self.has_mutable_default(node):
                results.append((node.name, node.lineno))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            if self.has_mutable_default(node):
                results.append((node.name, node.lineno))
            self.generic_visit(node)

        def has_mutable_default(self, node):
            for default in node.args.defaults + node.args.kw_defaults:
                if isinstance(default, mutable_nodes):
                    return True
            return False

    FunctionVisitor().visit(tree)
    return sorted(results, key=lambda x: (x[1], x[0]))
