import ast
from typing import List, Tuple

def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source code") from e

    def is_function_node(node):
        return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))

    def calculate_complexity(node):
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in child.generators:
                    if generator.ifs:
                        complexity += len(generator.ifs)
        return complexity

    def process_node(node):
        if is_function_node(node):
            complexity = calculate_complexity(node)
            results.append((node.name, node.lineno, complexity))
        for child in ast.iter_child_nodes(node):
            if is_function_node(child):
                process_node(child)

    results = []
    for node in tree.body:
        process_node(node)

    return sorted(results, key=lambda x: (x[1], x[0]))

# Example usage:
# source_code = 'def f(a):\n    if a > 0:\n        for i in range(a):\n            if i % 2 == 0 and i > 1:\n                print(i)\n    return a'
# print(compute_complexity(source_code))
