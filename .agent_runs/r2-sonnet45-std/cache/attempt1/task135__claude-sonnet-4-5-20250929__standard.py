import ast


def unused_imports(source):
    """
    Parse source and return imported names that are never referenced.
    
    Returns a list of bound names from import statements that are never
    referenced as ast.Name nodes elsewhere in the code, in source order.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")
    
    # Track imported names in order: list of (name, line_number)
    imported_names = []
    
    # Collect all import statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # import a.b.c binds 'a'
            # import x as y binds 'y'
            for alias in node.names:
                if alias.asname:
                    # import x as y -> binds 'y'
                    imported_names.append((alias.asname, node.lineno, node.col_offset))
                else:
                    # import a.b.c -> binds 'a'
                    name = alias.name.split('.')[0]
                    imported_names.append((name, node.lineno, node.col_offset))
        
        elif isinstance(node, ast.ImportFrom):
            # from m import x binds 'x'
            # from m import x as y binds 'y'
            # from m import * binds nothing inspectable
            for alias in node.names:
                if alias.name == '*':
                    # Star import - don't track anything
                    continue
                if alias.asname:
                    # from m import x as y -> binds 'y'
                    imported_names.append((alias.asname, node.lineno, node.col_offset))
                else:
                    # from m import x -> binds 'x'
                    imported_names.append((alias.name, node.lineno, node.col_offset))
    
    # Collect all Name nodes that are references (not in import context)
    used_names = set()
    
    class NameCollector(ast.NodeVisitor):
        def visit_Name(self, node):
            # Only count Load context (references), not Store or Del
            if isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            self.generic_visit(node)
    
    collector = NameCollector()
    collector.visit(tree)
    
    # Find unused imports, preserving order
    unused = []
    seen = set()
    for name, lineno, col_offset in imported_names:
        if name not in used_names and name not in seen:
            unused.append(name)
            seen.add(name)
    
    return unused
