import ast

def find_markers(source: str):
    results = []
    try:
        # Parse the source code into an AST
        tree = ast.parse(source)
    except SyntaxError:
        # If there's a syntax error, we will process the lines we can
        lines = source.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if '#' in line:
                comment = line.split('#', 1)[1].strip()
                if 'TODO' in comment:
                    results.append((line_number, 'TODO'))
                elif 'FIXME' in comment:
                    results.append((line_number, 'FIXME'))
        return results

    # If parsing is successful, we can analyze the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            # Skip string literals
            continue
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Check for comments in the line of the assignment
                    line_number = target.lineno
                    line = source.splitlines()[line_number - 1]
                    if '#' in line:
                        comment = line.split('#', 1)[1].strip()
                        if 'TODO' in comment:
                            results.append((line_number, 'TODO'))
                            break  # Only the first marker counts
                        elif 'FIXME' in comment:
                            results.append((line_number, 'FIXME'))
                            break  # Only the first marker counts
    return results
