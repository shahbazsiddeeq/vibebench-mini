import ast
from collections import defaultdict

def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    duplicates = []

    class DictKeyVisitor(ast.NodeVisitor):
        def visit_Dict(self, node):
            key_count = defaultdict(int)
            for key in node.keys:
                if isinstance(key, ast.Constant):
                    key_count[(key.value, type(key.value))] += 1

            for (key_value, key_type), count in key_count.items():
                if count > 1:
                    duplicates.append((node.lineno, key_value))

            self.generic_visit(node)

    DictKeyVisitor().visit(tree)

    return sorted(duplicates, key=lambda x: (x[0], repr(x[1])))

# The module is self-contained and does not include any I/O operations.
