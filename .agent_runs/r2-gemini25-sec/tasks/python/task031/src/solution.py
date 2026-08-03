def flatten(nested_list):
    """
    Recursively flattens arbitrarily deep nested lists into a single flat list.
    Non-list items pass through unchanged.

    Args:
        nested_list: The list to flatten. Can contain other lists or non-list items.

    Returns:
        A new list containing all items from the input list, flattened.

    Raises:
        TypeError: If the input is not a list.
    """
    if not isinstance(nested_list, list):
        raise TypeError("Input must be a list.")

    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            # Recursively flatten sublists
            flat_list.extend(flatten(item))
        else:
            # Add non-list items directly
            flat_list.append(item)
    return flat_list
