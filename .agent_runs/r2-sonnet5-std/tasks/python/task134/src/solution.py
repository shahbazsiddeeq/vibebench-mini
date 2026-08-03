import ast
import re

_SNAKE_CASE_RE = re.compile(r"^[a-z_][a-z0-9_]*$")


def non_snake_case_functions(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(str(e))

    results = []

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            self._check(node)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            self._check(node)
            self.generic_visit(node)

        def _check(self, node):
            if not _SNAKE_CASE_RE.match(node.name):
                results.append((node.lineno, node.col_offset, node.name))

    Visitor().visit(tree)
    results.sort(key=lambda t: (t[0], t[1]))
    return [name for _, _, name in results]
