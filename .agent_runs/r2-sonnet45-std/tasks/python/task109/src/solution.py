def pipeline(*fns):
    """
    Returns a function that applies fns left-to-right to its input.
    
    Args:
        *fns: Variable number of functions to compose
        
    Returns:
        A function that applies all fns in sequence from left to right
    """
    def composed(x):
        result = x
        for fn in fns:
            result = fn(result)
        return result
    
    return composed
