import ast

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.function_complexities = []
        self.current_complexity = 0

    def visit_FunctionDef(self, node):
        self._visit_function_or_async_function(node)

    def visit_AsyncFunctionDef(self, node):
        self._visit_function_or_async_function(node)

    def _visit_function_or_async_function(self, node):
        # Save current complexity state
        original_complexity = self.current_complexity
        self.current_complexity = 1  # Base complexity for the function

        # Visit the body of the function
        for item in node.body:
            self.visit(item)

        self.function_complexities.append((node.name, node.lineno, self.current_complexity))

        # Restore complexity state for the parent scope
        self.current_complexity = original_complexity

    def visit_If(self, node):
        # Each if/elif counts as +1
        self.current_complexity += 1
        # Visit test and body, but not orelse (else block doesn't add complexity)
        self.visit(node.test)
        for item in node.body:
            self.visit(item)
        # If there's an elif, it's a new If node in orelse, handled by its own visit_If
        # If there's a plain else, it's in orelse, but doesn't add complexity
        # We need to explicitly visit orelse to catch nested structures,
        # but ensure it doesn't add complexity for the 'else' itself.
        for item in node.orelse:
            self.visit(item)

    def visit_For(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        # Check for if-clauses in comprehensions
        for if_clause in node.ifs:
            self.current_complexity += 1
            self.visit(if_clause) # Visit the if-clause itself
        self.generic_visit(node) # Continue visiting other parts of the comprehension

    def visit_BoolOp(self, node):
        # Each boolean expression adds (number of operands - 1)
        self.current_complexity += len(node.values) - 1
        self.generic_visit(node)

    # Override generic_visit to prevent visiting nested functions/lambdas/classes
    # within the current function's body, as they are handled separately.
    def generic_visit(self, node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            # Do not visit nested function/lambda/class bodies here.
            # They will be visited as top-level functions if they are.
            # For FunctionDef/AsyncFunctionDef, their visit methods handle their own complexity.
            # For Lambda/ClassDef, they are explicitly excluded from complexity reporting.
            return
        super().generic_visit(node)


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}") from e

    visitor = ComplexityVisitor()
    
    # Iterate through the top-level nodes to find function definitions
    # This ensures that nested functions are also found and processed
    # as separate entries, but their bodies are not counted towards
    # the complexity of their enclosing function.
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Only visit if it's a function definition.
            # The visitor's visit_FunctionDef/visit_AsyncFunctionDef will
            # handle the complexity calculation for that specific function
            # and prevent recursing into further nested functions/lambdas/classes
            # within its own body for complexity calculation purposes.
            visitor.visit(node)

    # Sort the results as required
    visitor.function_complexities.sort(key=lambda x: (x[1], x[0]))

    return visitor.function_complexities
