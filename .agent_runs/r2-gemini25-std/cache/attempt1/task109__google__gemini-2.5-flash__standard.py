def pipeline(*fns):
    """
    Returns a function that applies fns left-to-right to its input.

    Args:
        *fns: A variable number of functions.

    Returns:
        A new function that takes an initial value and applies each
        of the input functions to it in sequence. If no functions are
        provided, the returned function acts as an identity function.
    """
    def composed_function(arg):
        result = arg
        for fn in fns:
            result = fn(result)
        return result
    return composed_function
