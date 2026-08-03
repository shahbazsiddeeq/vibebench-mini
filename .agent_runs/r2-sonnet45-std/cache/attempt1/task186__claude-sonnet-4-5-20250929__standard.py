import ast


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    """
    Compute cyclomatic complexity for all functions in Python source code.
    
    Returns a list of tuples (function_name, lineno, complexity) sorted by
    (lineno, function_name).
    
    Raises ValueError if source is not valid Python.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    # Find all function definitions
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            lineno = node.lineno
            complexity = calculate_function_complexity(node)
            results.append((name, lineno, complexity))
    
    # Sort by (lineno, name)
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results


def calculate_function_complexity(func_node):
    """
    Calculate complexity for a single function node.
    Only counts nodes in the function's own body, excluding nested definitions.
    """
    complexity = 1  # Base complexity
    
    # Walk through the function body, but exclude nested function/class/lambda bodies
    for node in walk_function_body(func_node):
        # if statement (including elif which is also ast.If)
        if isinstance(node, ast.If):
            complexity += 1
        # for and async for loops
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            complexity += 1
        # while loop
        elif isinstance(node, ast.While):
            complexity += 1
        # except handler
        elif isinstance(node, ast.ExceptHandler):
            complexity += 1
        # ternary expression (IfExp)
        elif isinstance(node, ast.IfExp):
            complexity += 1
        # boolean operations (and/or)
        elif isinstance(node, ast.BoolOp):
            # Add (number of operands - 1)
            complexity += len(node.values) - 1
        # comprehension if-clauses
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            # Count if clauses in comprehensions
            for generator in node.generators:
                complexity += len(generator.ifs)
    
    return complexity


def walk_function_body(func_node):
    """
    Walk through nodes in a function's body, excluding nested function/class/lambda bodies.
    """
    # We need to traverse the function body but stop at nested definitions
    
    def should_exclude(node):
        """Check if this node defines a new scope we should exclude."""
        return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef))
    
    def walk_excluding_nested(node, in_nested=False):
        """
        Recursively walk the AST, yielding nodes that belong to the current function.
        Skip bodies of nested functions, classes, and lambdas.
        """
        # If we're at a nested definition (but not the root function), don't traverse it
        if in_nested and should_exclude(node):
            return
        
        # Yield the current node (unless it's the function itself)
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or in_nested:
            yield node
        
        # Traverse children
        for child in ast.iter_child_nodes(node):
            # If child is a nested definition, don't go into its body
            if should_exclude(child):
                # Still yield the definition node itself if needed, but don't recurse into it
                if not isinstance(child, ast.Lambda):  # Don't yield lambdas
                    yield child
                # Don't recurse into nested definitions
            else:
                # Recurse into other nodes
                yield from walk_excluding_nested(child, in_nested=True)
    
    # Start walking from the function body
    for stmt in func_node.body:
        yield from walk_excluding_nested(stmt, in_nested=True)
