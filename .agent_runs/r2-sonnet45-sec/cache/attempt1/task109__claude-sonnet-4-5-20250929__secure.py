def pipeline(*fns):
    """
    Returns a function that applies the given functions left-to-right to its input.
    
    Args:
        *fns: Variable number of functions to compose
        
    Returns:
        A function that applies all fns in sequence to its argument
    """
    # Validate that all arguments are callable
    for i, fn in enumerate(fns):
        if not callable(fn):
            raise TypeError(f"Argument at position {i} is not callable")
    
    def composed(value):
        """Apply all functions in the pipeline to the input value."""
        result = value
        for fn in fns:
            try:
                result = fn(result)
            except Exception as e:
                # Re-raise with context but don't expose internal details
                raise type(e)(f"Error in pipeline function: {str(e)}") from None
        return result
    
    return composed
