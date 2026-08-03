import ast

class ImportCollector(ast.NodeVisitor):
    def __init__(self):
        self.imported_names = {}  # {name: ast.Name node}
        self.defined_names = set()

    def visit_Import(self, node):
        for alias in node.names:
            name_to_bind = alias.asname if alias.asname else alias.name.split('.')[0]
            # Store the ast.Name node for the bound name
            # We need to create a dummy ast.Name node as the original alias.name might be a.b.c
            # and we only bind 'a'. The line number and column offset are taken from the alias.
            dummy_name_node = ast.Name(id=name_to_bind, ctx=ast.Load())
            dummy_name_node.lineno = alias.lineno
            dummy_name_node.col_offset = alias.col_offset
            self.imported_names[name_to_bind] = dummy_name_node
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.names and not (len(node.names) == 1 and node.names[0].name == '*'):
            for alias in node.names:
                name_to_bind = alias.asname if alias.asname else alias.name
                dummy_name_node = ast.Name(id=name_to_bind, ctx=ast.Load())
                dummy_name_node.lineno = alias.lineno
                dummy_name_node.col_offset = alias.col_offset
                self.imported_names[name_to_bind] = dummy_name_node
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_names.add(target.id)
            elif isinstance(target, (ast.Tuple, ast.List)):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.defined_names.add(elt.id)
        self.generic_visit(node)

    def visit_For(self, node):
        if isinstance(node.target, ast.Name):
            self.defined_names.add(node.target.id)
        elif isinstance(node.target, (ast.Tuple, ast.List)):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    self.defined_names.add(elt.id)
        self.generic_visit(node)

    def visit_With(self, node):
        for item in node.items:
            if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                self.defined_names.add(item.optional_vars.id)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.name:
            self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_comprehension(self, node):
        if isinstance(node.target, ast.Name):
            self.defined_names.add(node.target.id)
        elif isinstance(node.target, (ast.Tuple, ast.List)):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    self.defined_names.add(elt.id)
        self.generic_visit(node)

    def visit_NamedExpr(self, node): # For Python 3.8+ walrus operator
        if isinstance(node.target, ast.Name):
            self.defined_names.add(node.target.id)
        self.generic_visit(node)


class UsageDetector(ast.NodeVisitor):
    def __init__(self, imported_names):
        self.imported_names = imported_names
        self.used_names = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Load, ast.Store, ast.Del)) and node.id in self.imported_names:
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Check if the base of the attribute access is an imported name
        if isinstance(node.value, ast.Name) and node.value.id in self.imported_names:
            self.used_names.add(node.value.id)
        self.generic_visit(node)


def unused_imports(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}") from e

    collector = ImportCollector()
    collector.visit(tree)

    # Filter out names that are defined within the module (e.g., function names, class names)
    # and thus might shadow an import or be used in a way that doesn't count as import usage.
    # This is a simplification; a full scope analysis would be more robust.
    # For this problem, we primarily care about whether the *imported* name is used.
    # If an imported name is then redefined, it's still considered "used" if the original
    # imported name was referenced before redefinition.
    # However, the problem statement implies we're looking for names that are *never* referenced.

    detector = UsageDetector(collector.imported_names)
    detector.visit(tree)

    unused = []
    # Sort imported names by their appearance in the source
    sorted_imported_names = sorted(
        collector.imported_names.items(),
        key=lambda item: (item[1].lineno, item[1].col_offset)
    )

    for name, name_node in sorted_imported_names:
        if name not in detector.used_names:
            unused.append(name_node.id)

    return unused
