import ast
import collections

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_complexities = collections.defaultdict(lambda: {'complexity': 1, 'lineno': 0, 'name': ''})
        self.current_function_key = None

    def _update_complexity(self, increment=1):
        if self.current_function_key:
            self.function_complexities[self.current_function_key]['complexity'] += increment

    def visit_FunctionDef(self, node):
        original_function_key = self.current_function_key
        function_key = (node.name, node.lineno)
        self.current_function_key = function_key
        self.function_complexities[function_key]['name'] = node.name
        self.function_complexities[function_key]['lineno'] = node.lineno

        for item in node.body:
            self.visit(item)

        self.current_function_key = original_function_key

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node) # Async functions are treated the same for complexity

    def visit_If(self, node):
        # Each if/elif counts as +1
        self._update_complexity(1)
        # No need to recurse into body here, ast.walk will handle it.
        # We only care about the 'if' itself, not its contents for this rule.
        self.generic_visit(node)

    def visit_For(self, node):
        self._update_complexity(1)
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self._update_complexity(1)
        self.generic_visit(node)

    def visit_While(self, node):
        self._update_complexity(1)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self._update_complexity(1)
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self._update_complexity(1)
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # Add (number of operands - 1)
        self._update_complexity(len(node.values) - 1)
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self._handle_comprehension_ifs(node.generators)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self._handle_comprehension_ifs(node.generators)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        self._handle_comprehension_ifs(node.generators)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self._handle_comprehension_ifs(node.generators)
        self.generic_visit(node)

    def _handle_comprehension_ifs(self, generators):
        for gen in generators:
            for _if_clause in gen.ifs:
                self._update_complexity(1)

    # Override generic_visit to prevent recursion into nested functions/classes/lambdas
    # when we are inside a function body.
    def generic_visit(self, node):
        if self.current_function_key:
            # If we are currently analyzing a function, we should not recurse into
            # nested FunctionDef, AsyncFunctionDef, ClassDef, or Lambda.
            # These will be visited as top-level nodes or handled by their own visit methods.
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                return
        super().generic_visit(node)

    # Special handling for top-level nodes to ensure all functions are visited
    def visit(self, node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # When we encounter a function definition, we want to process it
            # as a new, separate entry.
            self.visit_FunctionDef(node) if isinstance(node, ast.FunctionDef) else self.visit_AsyncFunctionDef(node)
        elif isinstance(node, ast.ClassDef):
            # For class definitions, we need to visit its body to find methods
            original_function_key = self.current_function_key
            self.current_function_key = None # Temporarily clear to ensure methods are treated as new functions
            for item in node.body:
                self.visit(item)
            self.current_function_key = original_function_key
        else:
            # For all other nodes, proceed with generic visiting logic
            super().visit(node)


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    if not isinstance(source, str):
        raise ValueError("Input 'source' must be a string.")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source code: {e}") from e

    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)

    results = []
    for key, data in analyzer.function_complexities.items():
        results.append((data['name'], data['lineno'], data['complexity']))

    # Sort by lineno, then by function_name
    results.sort(key=lambda x: (x[1], x[0]))

    return results
