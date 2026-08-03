def expand_cases(base, overrides):
    """
    Returns a list with one new dict per override, where each result is base 
    merged with that single override and the override's values win on key collisions.
    The merge is SHALLOW - for a key present in both, the override's value 
    replaces the base's value outright, with no recursive merging of nested dicts.
    Each result is a fresh top-level dict (base is never mutated), and an empty 
    overrides list yields an empty list.
    """
    result = []
    for override in overrides:
        # Create a new dict starting with base
        merged = base.copy()
        # Update with override (override values win)
        merged.update(override)
        result.append(merged)
    return result
