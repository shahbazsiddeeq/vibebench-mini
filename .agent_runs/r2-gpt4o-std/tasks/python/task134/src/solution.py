import ast
import re

def non_snake_case_functions(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid syntax")

    non_snake_case_names = []
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            if not snake_case_pattern.match(node.name) and not node.name.startswith('__'):
                non_snake_case_names.append(node.name)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            if not snake_case_pattern.match(node.name) and not node.name.startswith('__'):
                non_snake_case_names.append(node.name)
            self.generic_visit(node)

    FunctionVisitor().visit(tree)
    return non_snake_case_names
