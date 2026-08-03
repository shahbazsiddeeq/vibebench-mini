import ast
from typing import List

def unused_imports(source: str) -> List[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    imported_names = {}
    used_names = set()

    class ImportVisitor(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                imported_names[alias.asname or alias.name.split('.')[0]] = node.lineno

        def visit_ImportFrom(self, node):
            if node.module and node.names[0].name != '*':
                for alias in node.names:
                    imported_names[alias.asname or alias.name] = node.lineno

    class NameVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            used_names.add(node.id)

    ImportVisitor().visit(tree)
    NameVisitor().visit(tree)

    unused = [name for name in imported_names if name not in used_names]
    unused.sort(key=lambda name: imported_names[name])
    return unused
