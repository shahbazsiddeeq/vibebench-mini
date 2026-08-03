import ast

def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    def calculate_complexity(node):
        complexity = 1  # Start with base complexity of 1

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in child.generators:
                    if generator.ifs:
                        complexity += len(generator.ifs)

        return complexity

    def visit_function_defs(node, results):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = calculate_complexity(child)
                results.append((child.name, child.lineno, complexity))
                # Do not recurse into the function body
            else:
                visit_function_defs(child, results)

    results = []
    visit_function_defs(tree, results)
    results.sort(key=lambda x: (x[1], x[0]))
    return results
