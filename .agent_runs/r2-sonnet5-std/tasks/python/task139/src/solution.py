def expand_cases(base, overrides):
    return [{**base, **override} for override in overrides]
