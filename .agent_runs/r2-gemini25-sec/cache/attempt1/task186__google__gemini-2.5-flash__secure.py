import ast

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.current_complexity = 0
        self.in_target_function = False

    def visit_FunctionDef(self, node):
        self._handle_function_definition(node)

    def visit_AsyncFunctionDef(self, node):
        self._handle_function_definition(node)

    def _handle_function_definition(self, node):
        # Store previous state
        prev_in_target_function = self.in_target_function
        prev_complexity = self.current_complexity

        self.in_target_function = True
        self.current_complexity = 1  # Base complexity

        for item in node.body:
            self.visit(item)

        self.functions.append((node.name, node.lineno, self.current_complexity))

        # Restore previous state
        self.in_target_function = prev_in_target_function
        self.current_complexity = prev_complexity

        # If we are in a nested function, we still need to visit its body
        # but its complexity is already calculated and stored.
        # We don't want to double count its internal decision points for the outer function.
        # So, we just skip the generic_visit for the function node itself.
        # The body of the function has already been visited in the loop above.

    def generic_visit(self, node):
        if not self.in_target_function:
            return

        # Decision points
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.IfExp)):
            self.current_complexity += 1
        elif isinstance(node, ast.ExceptHandler):
            self.current_complexity += 1
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for gen in node.generators:
                for if_clause in gen.ifs:
                    self.current_complexity += 1
        elif isinstance(node, ast.BoolOp):
            self.current_complexity += len(node.values) - 1

        # Exclude nested function/class definitions from the current function's complexity
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            # Do not recurse into these for the *current* function's complexity calculation.
            # They will be handled by their own visit methods if they are function definitions.
            return

        super().generic_visit(node)


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    """
    Parses a string of Python source with the ast module and returns, for every
    function definition, a tuple (function_name, lineno, complexity).
    """
    if not isinstance(source, str):
        raise TypeError("Input 'source' must be a string.")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source code: {e}") from e

    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)

    # Sort by lineno, then by function_name
    analyzer.functions.sort(key=lambda x: (x[1], x[0]))

    return analyzer.functions
