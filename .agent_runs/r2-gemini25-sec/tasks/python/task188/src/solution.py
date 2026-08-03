import ast
import collections

def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    """
    Parses a string of Python source with the ast module and returns, for every
    function definition that is missing at least one required annotation, a tuple
    (function_name, lineno) where lineno is the 1-based line of the def/async def.

    A function is fully annotated only when it has a return annotation (the `-> T`
    after the parameter list) AND every one of its parameters is annotated, counting
    positional-only parameters, ordinary parameters, keyword-only parameters,
    the *args parameter, and the **kwargs parameter. The single exception is that
    the FIRST positional parameter of a method (a function defined directly in a
    class body) is exempt when it is named exactly `self` or `cls`; this exemption
    never applies to module-level functions or to functions nested inside other
    functions. Parameters that have default values still require annotations.
    Every def and async def is inspected, including methods, dunder methods, and
    nested inner functions; lambdas are ignored. A function is reported at most
    once even if several annotations are missing. Detection is by real parsing,
    so text inside strings or comments is irrelevant. The result is sorted
    ascending by (lineno, function_name).

    Raises ValueError if source is not valid Python (ast.parse raises SyntaxError).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}") from e

    untyped_functions = []

    class AnnotationDetector(ast.NodeVisitor):
        def __init__(self):
            self.function_stack = collections.deque() # Stores (function_name, is_method)
            self.untyped_functions_set = set() # To avoid duplicates

        def visit_ClassDef(self, node: ast.ClassDef):
            # Push a dummy function onto the stack to indicate we are inside a class
            # This helps in determining if a function is a method.
            self.function_stack.append((None, True))
            self.generic_visit(node)
            self.function_stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef):
            self._check_function_annotations(node)
            self.function_stack.append((node.name, False)) # Not a method for nested functions
            self.generic_visit(node)
            self.function_stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            self._check_function_annotations(node)
            self.function_stack.append((node.name, False)) # Not a method for nested functions
            self.generic_visit(node)
            self.function_stack.pop()

        def _check_function_annotations(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
            is_method = False
            if self.function_stack:
                # Check if the immediate parent is a class (indicated by (None, True))
                # This means the current function is a method.
                if self.function_stack[-1][1]:
                    is_method = True

            missing_annotation = False

            # Check return annotation
            if node.returns is None:
                missing_annotation = True

            # Check parameter annotations
            if not missing_annotation:
                for i, arg in enumerate(node.args.posonlyargs):
                    if arg.annotation is None:
                        # Exemption for 'self' or 'cls' in methods
                        if is_method and i == 0 and arg.arg in ('self', 'cls'):
                            continue
                        missing_annotation = True
                        break
                if not missing_annotation:
                    for i, arg in enumerate(node.args.args):
                        if arg.annotation is None:
                            # Exemption for 'self' or 'cls' in methods
                            # This applies to the first positional parameter, which could be in args
                            # if there are no posonlyargs.
                            if is_method and i == 0 and not node.args.posonlyargs and arg.arg in ('self', 'cls'):
                                continue
                            missing_annotation = True
                            break
                if not missing_annotation:
                    if node.args.vararg and node.args.vararg.annotation is None:
                        missing_annotation = True
                if not missing_annotation:
                    for arg in node.args.kwonlyargs:
                        if arg.annotation is None:
                            missing_annotation = True
                            break
                if not missing_annotation:
                    if node.args.kwarg and node.args.kwarg.annotation is None:
                        missing_annotation = True

            if missing_annotation:
                # Use a tuple (name, lineno) for the set to ensure uniqueness
                # and correct sorting later.
                self.untyped_functions_set.add((node.name, node.lineno))

    detector = AnnotationDetector()
    detector.visit(tree)

    # Convert set to list and sort
    untyped_functions = sorted(list(detector.untyped_functions_set), key=lambda x: (x[1], x[0]))
    return untyped_functions
