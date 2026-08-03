def expand_cases(base, overrides):
    result = []
    for override in overrides:
        merged = base.copy()
        merged.update(override)
        result.append(merged)
    return result
