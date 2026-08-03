def flatten(nested):
    """Recursively flatten nested lists into a single list."""
    result = []

    def visit(item):
        if isinstance(item, list):
            for value in item:
                visit(value)
        else:
            result.append(item)

    visit(nested)
    return result
