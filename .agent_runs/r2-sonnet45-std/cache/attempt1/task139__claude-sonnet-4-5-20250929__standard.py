def expand_cases(base, overrides):
    """
    Returns a list with one new dict per override, where each result is base 
    merged with that single override. Override values win on key collisions.
    The merge is shallow - no recursive merging of nested dicts.
    """
    result = []
    for override in overrides:
        # Create a shallow copy of base
        merged = base.copy()
        # Update with override (shallow update)
        merged.update(override)
        result.append(merged)
    return result
