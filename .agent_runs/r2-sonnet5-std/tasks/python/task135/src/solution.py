import ast


def unused_imports(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(str(e))

    imports = []  # list of (name, order_index)

    class ImportCollector(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                if alias.asname:
                    name = alias.asname
                else:
                    name = alias.name.split(".")[0]
                imports.append((name, node.lineno, node.col_offset))
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            for alias in node.names:
                if alias.name == "*":
                    continue
                if alias.asname:
                    name = alias.asname
                else:
                    name = alias.name
                imports.append((name, node.lineno, node.col_offset))
            self.generic_visit(node)

    ImportCollector().visit(tree)

    used_names = set()

    class NameCollector(ast.NodeVisitor):
        def visit_Name(self, node):
            used_names.add(node.id)
            self.generic_visit(node)

    NameCollector().visit(tree)

    result = []
    for name, lineno, col in imports:
        if name not in used_names:
            result.append(name)

    return result
