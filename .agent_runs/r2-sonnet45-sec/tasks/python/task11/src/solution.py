def build_cmd(base, args):
    """
    Build a command argument list for subprocess (no shell).
    
    Args:
        base: Either a str (program name) or list of str (program plus leading args)
        args: Dict with allowed keys: verbose (bool), timeout (positive int), output (str)
    
    Returns:
        List of strings representing the command and its arguments
    
    Raises:
        ValueError: If args contains unknown keys, wrong types, or invalid values
    """
    # Start with base command
    if isinstance(base, str):
        result = [base]
    elif isinstance(base, list):
        result = list(base)  # Make a copy
    else:
        raise ValueError("base must be a string or list of strings")
    
    # Validate that all keys in args are allowed
    allowed_keys = {"verbose", "timeout", "output"}
    for key in args:
        if key not in allowed_keys:
            raise ValueError(f"Unknown key: {key}")
    
    # Process verbose flag
    if "verbose" in args:
        verbose = args["verbose"]
        # Must be exactly bool, not int (since bool is subclass of int in Python)
        if type(verbose) is not bool:
            raise ValueError("verbose must be a bool")
        if verbose:
            result.append("--verbose")
    
    # Process timeout
    if "timeout" in args:
        timeout = args["timeout"]
        # Must be int but NOT bool (bool is subclass of int)
        if type(timeout) is bool:
            raise ValueError("timeout must be an int, not bool")
        if not isinstance(timeout, int):
            raise ValueError("timeout must be an int")
        if timeout <= 0:
            raise ValueError("timeout must be strictly positive")
        result.extend(["--timeout", str(timeout)])
    
    # Process output
    if "output" in args:
        output = args["output"]
        if not isinstance(output, str):
            raise ValueError("output must be a string")
        # Check for forbidden characters: NUL, newline, carriage return
        if '\0' in output or '\n' in output or '\r' in output:
            raise ValueError("output must not contain NUL, newline, or carriage-return characters")
        result.extend(["--output", output])
    
    return result
