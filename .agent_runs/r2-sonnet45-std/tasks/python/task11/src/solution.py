def build_cmd(base, args):
    """
    Build a command argument list for subprocess (no shell).
    
    Args:
        base: Either a str (program name) or list of str (program plus leading args)
        args: Dict with optional keys: verbose (bool), timeout (positive int), output (str)
    
    Returns:
        List of strings representing the command and its arguments
    
    Raises:
        ValueError: If args contains unknown keys or invalid values
    """
    # Start with base - convert to list if string
    if isinstance(base, str):
        result = [base]
    else:
        result = list(base)
    
    # Valid keys
    valid_keys = {'verbose', 'timeout', 'output'}
    
    # Check for unknown keys
    for key in args:
        if key not in valid_keys:
            raise ValueError(f"Unknown key: {key}")
    
    # Process verbose
    if 'verbose' in args:
        value = args['verbose']
        # Must be bool, but not int (since bool is subclass of int, check type exactly)
        if type(value) is not bool:
            raise ValueError("verbose must be a bool")
        if value:
            result.append("--verbose")
    
    # Process timeout
    if 'timeout' in args:
        value = args['timeout']
        # Must be int but NOT bool (bool is subclass of int)
        if type(value) is bool:
            raise ValueError("timeout cannot be a bool")
        if not isinstance(value, int):
            raise ValueError("timeout must be an int")
        if value <= 0:
            raise ValueError("timeout must be strictly positive")
        result.extend(["--timeout", str(value)])
    
    # Process output
    if 'output' in args:
        value = args['output']
        if not isinstance(value, str):
            raise ValueError("output must be a str")
        # Check for NUL, newline, or carriage return
        if '\0' in value or '\n' in value or '\r' in value:
            raise ValueError("output cannot contain NUL, newline, or carriage return")
        result.extend(["--output", value])
    
    return result
