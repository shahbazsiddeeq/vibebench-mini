import ast

def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """
    Parses a string of Python source with the ast module and returns, for every
    function definition that has at least one parameter whose default value is
    a mutable literal display, a tuple (function_name, lineno) where lineno is
    the 1-based line of the def/async def statement.

    A default counts as mutable if and only if its AST node is a list display
    ([...]/[]), a dict display ({...}/{}), or a set display ({1, 2}); tuple
    defaults, string/number/None/bool constants, and calls like list() or
    dict() do NOT count.

    Every def and async def is inspected, including methods inside classes and
    nested inner functions; lambdas are ignored. Both ordinary defaults and
    keyword-only defaults are checked. A function is reported at most once even
    if it has several mutable defaults.

    Occurrences of def(...) inside string literals or comments must be ignored
    (real parsing, not text search). The result is sorted ascending by
    (lineno, function_name).

    Raises ValueError if source is not valid Python (ast.parse raises SyntaxError).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source") from e

    mutable_defaults_found = set()
    results = []

    class MutableDefaultDetector(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            self._check_function_defaults(node)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            self._check_function_defaults(node)
            self.generic_visit(node)

        def _check_function_defaults(self, node):
            has_mutable_default = False
            for arg in node.args.defaults:
                if self._is_mutable_literal_display(arg):
                    has_mutable_default = True
                    break
            for arg in node.args.kw_defaults:
                if arg is not None and self._is_mutable_literal_display(arg):
                    has_mutable_default = True
                    break

            if has_mutable_default:
                # Use a tuple (name, lineno) for the set to ensure uniqueness
                # and allow sorting later.
                if (node.name, node.lineno) not in mutable_defaults_found:
                    mutable_defaults_found.add((node.name, node.lineno))
                    results.append((node.name, node.lineno))

        def _is_mutable_literal_display(self, node):
            return isinstance(node, (ast.List, ast.Dict, ast.Set))

    detector = MutableDefaultDetector()
    detector.visit(tree)

    results.sort(key=lambda x: (x[1], x[0]))
    return results
