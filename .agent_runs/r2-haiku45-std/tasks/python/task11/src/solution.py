def build_cmd(base, args):
    """
    Build an argument list for subprocess (no shell).
    
    Args:
        base: str (program name) or list of str (program plus leading args)
        args: dict with allowed keys:
            - verbose: bool. If True, append "--verbose"
            - timeout: strictly positive int (bool not accepted). Append "--timeout" and value
            - output: str with no NUL, newline, or carriage-return. Append "--output" and value
    
    Returns:
        list of str tokens for subprocess
    
    Raises:
        ValueError: for unknown keys, wrong types, or out-of-range values
    """
    # Start with base
    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, list):
        cmd = list(base)
    else:
        raise ValueError("base must be str or list of str")
    
    # Allowed keys and their validators
    allowed_keys = {"verbose", "timeout", "output"}
    
    # Check for unknown keys
    for key in args:
        if key not in allowed_keys:
            raise ValueError(f"Unknown key: {key}")
    
    # Process verbose
    if "verbose" in args:
        value = args["verbose"]
        # Must be bool, not int (even though bool subclasses int)
        if not isinstance(value, bool):
            raise ValueError("verbose must be a bool")
        if value:
            cmd.append("--verbose")
    
    # Process timeout
    if "timeout" in args:
        value = args["timeout"]
        # Must be int but NOT bool (bool is subclass of int, so check explicitly)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("timeout must be a strictly positive int")
        if value <= 0:
            raise ValueError("timeout must be strictly positive")
        cmd.append("--timeout")
        cmd.append(str(value))
    
    # Process output
    if "output" in args:
        value = args["output"]
        if not isinstance(value, str):
            raise ValueError("output must be a str")
        # Check for NUL, newline, or carriage-return
        if '\x00' in value or '\n' in value or '\r' in value:
            raise ValueError("output must not contain NUL, newline, or carriage-return")
        cmd.append("--output")
        cmd.append(value)
    
    return cmd
