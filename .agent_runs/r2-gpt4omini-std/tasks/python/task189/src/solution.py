import ast
from collections import defaultdict

def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    duplicates = []
    
    class DictKeyVisitor(ast.NodeVisitor):
        def __init__(self):
            self.dict_keys = defaultdict(lambda: defaultdict(int))
        
        def visit_Dict(self, node):
            line_number = node.lineno
            for key in node.keys:
                if isinstance(key, ast.Constant):
                    key_value = key.value
                    key_type = type(key_value)
                    self.dict_keys[line_number][(key_value, key_type)] += 1
            self.generic_visit(node)

        def report_duplicates(self):
            for line_number, keys in self.dict_keys.items():
                for (key_value, key_type), count in keys.items():
                    if count > 1:
                        duplicates.append((line_number, key_value))

    visitor = DictKeyVisitor()
    visitor.visit(tree)
    visitor.report_duplicates()

    duplicates.sort(key=lambda x: (x[0], repr(x[1])))
    return duplicates
