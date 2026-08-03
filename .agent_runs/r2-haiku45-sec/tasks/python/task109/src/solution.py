def pipeline(*fns):
    """
    Returns a function that applies fns left-to-right to its input.
    
    Args:
        *fns: Variable number of callable functions to compose
        
    Returns:
        A function that applies all input functions left-to-right
        
    Raises:
        TypeError: If any argument is not callable
    """
    # Validate that all arguments are callable
    for fn in fns:
        if not callable(fn):
            raise TypeError(f"Expected callable, got {type(fn).__name__}")
    
    def composed(value):
        """Apply all functions left-to-right to the input value."""
        result = value
        for fn in fns:
            result = fn(result)
        return result
    
    return composed
