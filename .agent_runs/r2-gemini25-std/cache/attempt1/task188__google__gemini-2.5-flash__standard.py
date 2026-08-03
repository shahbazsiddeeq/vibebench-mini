import ast
import collections

def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    """
    Parses a string of Python source with the ast module and returns, for every
    function definition that is missing at least one required annotation, a tuple
    (function_name, lineno) where lineno is the 1-based line of the def/async def.

    A function is fully annotated only when it has a return annotation (the `-> T`
    after the parameter list) AND every one of its parameters is annotated, counting
    positional-only parameters, ordinary parameters, keyword-only parameters, the
    *args parameter, and the **kwargs parameter. The single exception is that the
    FIRST positional parameter of a method (a function defined directly in a class body)
    is exempt when it is named exactly `self` or `cls`; this exemption never applies
    to module-level functions or to functions nested inside other functions.
    Parameters that have default values still require annotations. Every def and
    async def is inspected, including methods, dunder methods, and nested inner functions;
    lambdas are ignored. A function is reported at most once even if several
    annotations are missing. Detection is by real parsing, so text inside strings
    or comments is irrelevant. The result is sorted ascending by (lineno, function_name).

    Raises ValueError if source is not valid Python (ast.parse raises SyntaxError).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source code") from e

    untyped_functions = collections.defaultdict(bool)

    class AnnotationChecker(ast.NodeVisitor):
        def __init__(self):
            self.class_stack = []

        def visit_FunctionDef(self, node):
            self._check_function_def(node)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            self._check_function_def(node)
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            self.class_stack.append(node.name)
            self.generic_visit(node)
            self.class_stack.pop()

        def _check_function_def(self, node):
            is_method = bool(self.class_stack) and len(self.class_stack) == 1
            is_untyped = False

            # Check return annotation
            if node.returns is None:
                is_untyped = True

            # Check parameters
            if not is_untyped:
                for i, arg in enumerate(node.args.posonlyargs):
                    if arg.annotation is None:
                        # Exemption for 'self' or 'cls' in methods
                        if not (is_method and i == 0 and arg.arg in ('self', 'cls')):
                            is_untyped = True
                            break
                if not is_untyped:
                    for i, arg in enumerate(node.args.args):
                        if arg.annotation is None:
                            # Exemption for 'self' or 'cls' in methods
                            # This covers ordinary parameters, which can include the first one
                            # if it's not positional-only.
                            # We need to count positional-only args to determine if it's the first *overall* parameter.
                            if not (is_method and (len(node.args.posonlyargs) + i) == 0 and arg.arg in ('self', 'cls')):
                                is_untyped = True
                                break
                if not is_untyped and node.args.vararg and node.args.vararg.annotation is None:
                    is_untyped = True
                if not is_untyped:
                    for arg in node.args.kwonlyargs:
                        if arg.annotation is None:
                            is_untyped = True
                            break
                if not is_untyped and node.args.kwarg and node.args.kwarg.annotation is None:
                    is_untyped = True

            if is_untyped:
                untyped_functions[(node.name, node.lineno)] = True

    checker = AnnotationChecker()
    checker.visit(tree)

    result = sorted([item for item, _ in untyped_functions.items()])
    return result
