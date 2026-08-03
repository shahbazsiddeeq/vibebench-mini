import ast

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexities = []
        self.current_complexity = 0
        self.in_function_body = 0

    def visit_FunctionDef(self, node):
        self.in_function_body += 1
        original_complexity = self.current_complexity
        self.current_complexity = 1  # Base complexity for the function

        for item in node.body:
            self.visit(item)

        self.complexities.append((node.name, node.lineno, self.current_complexity))
        self.current_complexity = original_complexity
        self.in_function_body -= 1

    def visit_AsyncFunctionDef(self, node):
        self.in_function_body += 1
        original_complexity = self.current_complexity
        self.current_complexity = 1  # Base complexity for the function

        for item in node.body:
            self.visit(item)

        self.complexities.append((node.name, node.lineno, self.current_complexity))
        self.current_complexity = original_complexity
        self.in_function_body -= 1

    def visit_If(self, node):
        if self.in_function_body > 0:
            self.current_complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        if self.in_function_body > 0:
            self.current_complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        if self.in_function_body > 0:
            self.current_complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        if self.in_function_body > 0:
            self.current_complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if self.in_function_body > 0:
            self.current_complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        if self.in_function_body > 0:
            self.current_complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if self.in_function_body > 0:
            self.current_complexity += (len(node.values) - 1)
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self._handle_comprehension(node)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self._handle_comprehension(node)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        self._handle_comprehension(node)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self._handle_comprehension(node)
        self.generic_visit(node)

    def _handle_comprehension(self, node):
        if self.in_function_body > 0:
            for generator in node.generators:
                for if_clause in generator.ifs:
                    self.current_complexity += 1
        # Do not call generic_visit here, as it's called by the specific visit_ methods.
        # We only want to count the if-clauses, not recurse into the comprehension's
        # body for other complexity points, as it's not part of the function's *own* body.

    # Override generic_visit to prevent recursion into nested functions/classes/lambdas
    def generic_visit(self, node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            # For FunctionDef/AsyncFunctionDef, we handle them specifically in their visit methods.
            # For ClassDef/Lambda, we don't want to recurse into their bodies for the *current* function's complexity.
            # However, we still need to visit the nested function/async function definitions themselves
            # to report their complexities.
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                super().generic_visit(node)
            return

        # Special handling for comprehensions: only visit generators to find if-clauses,
        # but don't recurse into the elements/keys/values themselves for complexity.
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for field, value in ast.iter_fields(node):
                if field == 'generators':
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, ast.AST):
                                self.visit(item)
                # Do not visit other fields like 'elt', 'key', 'value' for complexity.
            return

        super().generic_visit(node)


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}") from e

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    # Sort the results
    visitor.complexities.sort(key=lambda x: (x[1], x[0]))

    return visitor.complexities
