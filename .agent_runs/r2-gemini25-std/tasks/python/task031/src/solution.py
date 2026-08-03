def flatten(nested):
    """
    Recursively flattens arbitrarily deep nested lists into a single flat list.
    Non-list items pass through unchanged.

    Args:
        nested: A list that may contain other lists or non-list items.

    Returns:
        A new list containing all items from the input list, flattened.
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
