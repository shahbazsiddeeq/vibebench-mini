# src/solution.py

import ast

def find_markers(source: str):
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Input must be a string.")
    
    results = []
    try:
        # Tokenize the source code
        tree = ast.parse(source)
        
        # Walk through the AST to find comments
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                # Skip string literals
                continue
            
            if hasattr(node, 'lineno'):
                line_number = node.lineno
                # Get the line of code
                line = source.splitlines()[line_number - 1]
                
                # Find the last '#' in the line to isolate the comment
                comment_index = line.find('#')
                if comment_index != -1:
                    comment = line[comment_index:]
                    if 'TODO' in comment:
                        results.append((line_number, 'TODO'))
                    elif 'FIXME' in comment:
                        results.append((line_number, 'FIXME'))
    
    except SyntaxError:
        # If there's a syntax error, we still return results found before the error
        pass
    
    # Filter results to ensure only the first marker per line is returned
    filtered_results = []
    seen_lines = set()
    for line_number, marker in results:
        if line_number not in seen_lines:
            filtered_results.append((line_number, marker))
            seen_lines.add(line_number)
    
    return filtered_results
