import ast

def find_markers(source):
    results = []
    try:
        # Parse the source code into an AST
        tree = ast.parse(source)
    except SyntaxError:
        # If there's a syntax error, we will only process the lines we can
        lines = source.splitlines()
        for line_number, line in enumerate(lines, start=1):
            comment_index = line.find('#')
            if comment_index != -1:
                comment = line[comment_index + 1:].strip()
                if 'TODO' in comment:
                    results.append((line_number, 'TODO'))
                    break
                elif 'FIXME' in comment:
                    results.append((line_number, 'FIXME'))
                    break
        return results

    # If the AST is successfully parsed, we can analyze the comments
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            # Skip string literals
            continue
        if hasattr(node, 'lineno'):
            line_number = node.lineno
            if hasattr(node, 'body'):
                for stmt in node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str):
                        continue
                    if hasattr(stmt, 'lineno'):
                        comment = source.splitlines()[line_number - 1]
                        comment_index = comment.find('#')
                        if comment_index != -1:
                            comment_text = comment[comment_index + 1:].strip()
                            if 'TODO' in comment_text:
                                results.append((line_number, 'TODO'))
                                break
                            elif 'FIXME' in comment_text:
                                results.append((line_number, 'FIXME'))
                                break
    return results
