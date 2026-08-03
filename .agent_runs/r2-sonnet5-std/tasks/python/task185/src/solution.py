import ast


def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")

    results = []

    def is_mutable(node):
        return isinstance(node, (ast.List, ast.Dict, ast.Set))

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            self._check(node)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            self._check(node)
            self.generic_visit(node)

        def _check(self, node):
            defaults = list(node.args.defaults) + list(node.args.kw_defaults)
            for d in defaults:
                if d is not None and is_mutable(d):
                    results.append((node.name, node.lineno))
                    break

    Visitor().visit(tree)

    results.sort(key=lambda x: (x[1], x[0]))
    return results
