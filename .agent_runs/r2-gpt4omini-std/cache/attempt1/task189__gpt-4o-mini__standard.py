import ast
from collections import defaultdict

def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    duplicates = []
    
    class DictKeyVisitor(ast.NodeVisitor):
        def visit_dict(self, node: ast.Dict):
            key_counts = defaultdict(int)
            line_number = node.lineno
            
            for key in node.keys:
                if isinstance(key, ast.Constant):
                    key_counts[key.value] += 1
            
            for key_value, count in key_counts.items():
                if count > 1:
                    duplicates.append((line_number, key_value))
            
            self.generic_visit(node)

    DictKeyVisitor().visit(tree)
    
    return sorted(duplicates, key=lambda x: (x[0], repr(x[1])))
