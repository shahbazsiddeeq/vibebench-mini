import ast
from collections import defaultdict

def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source") from e

    duplicates = []

    class DictKeyVisitor(ast.NodeVisitor):
        def visit_Dict(self, node: ast.Dict):
            key_counts = defaultdict(int)
            key_lines = {}

            for key in node.keys:
                if isinstance(key, ast.Constant):
                    key_value = key.value
                    key_type = type(key_value)
                    key_counts[(key_value, key_type)] += 1
                    if (key_value, key_type) not in key_lines:
                        key_lines[(key_value, key_type)] = node.lineno

            for (key_value, key_type), count in key_counts.items():
                if count > 1:
                    duplicates.append((key_lines[(key_value, key_type)], key_value))

            self.generic_visit(node)

    DictKeyVisitor().visit(tree)

    return sorted(duplicates, key=lambda x: (x[0], repr(x[1])))

# The module is self-contained and does not include any I/O operations.
