def expand_cases(base, overrides):
    """
    Expands a base dictionary with a list of override dictionaries.

    Args:
        base (dict): The base dictionary.
        overrides (list): A list of dictionaries, where each dictionary
                          represents an override.

    Returns:
        list: A list of new dictionaries. Each dictionary in the result list
              is a merge of the base dictionary with one of the override
              dictionaries. Override values win on key collisions.
              The merge is shallow.
    """
    results = []
    for override in overrides:
        new_dict = base.copy()  # Start with a shallow copy of the base
        new_dict.update(override)  # Apply the override
        results.append(new_dict)
    return results
