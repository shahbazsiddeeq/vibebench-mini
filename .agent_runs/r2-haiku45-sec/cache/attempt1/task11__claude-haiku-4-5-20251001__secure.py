"""Safe CLI Argument Builder - builds subprocess argument lists securely."""


def build_cmd(base, args):
    """
    Build a safe argument list for subprocess (no shell).
    
    Args:
        base: str (program name) or list of str (program + leading args)
        args: dict with optional keys:
            - verbose (bool): if True, append "--verbose"
            - timeout (positive int, not bool): append "--timeout" and value
            - output (str, no NUL/newline/CR): append "--output" and value
    
    Returns:
        list of str: complete argument list for subprocess
    
    Raises:
        ValueError: for unknown keys, wrong types, or invalid values
    """
    # Validate and normalize base
    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, list):
        if not all(isinstance(item, str) for item in base):
            raise ValueError("base list must contain only strings")
        cmd = list(base)
    else:
        raise ValueError("base must be str or list of str")
    
    # Validate args is a dict
    if not isinstance(args, dict):
        raise ValueError("args must be a dict")
    
    # Define allowed keys and their validators
    allowed_keys = {"verbose", "timeout", "output"}
    
    # Check for unknown keys
    unknown_keys = set(args.keys()) - allowed_keys
    if unknown_keys:
        raise ValueError(f"unknown keys: {unknown_keys}")
    
    # Process each argument
    if "verbose" in args:
        verbose = args["verbose"]
        # Must be exactly bool, not int subclass
        if type(verbose) is not bool:
            raise ValueError("verbose must be a bool")
        if verbose:
            cmd.append("--verbose")
    
    if "timeout" in args:
        timeout = args["timeout"]
        # Reject bool (even though bool is subclass of int)
        if type(timeout) is bool:
            raise ValueError("timeout must not be a bool")
        if not isinstance(timeout, int):
            raise ValueError("timeout must be an int")
        if timeout <= 0:
            raise ValueError("timeout must be strictly positive")
        cmd.append("--timeout")
        cmd.append(str(timeout))
    
    if "output" in args:
        output = args["output"]
        if not isinstance(output, str):
            raise ValueError("output must be a str")
        # Check for forbidden characters: NUL, newline, carriage return
        if "\x00" in output or "\n" in output or "\r" in output:
            raise ValueError("output must not contain NUL, newline, or carriage return")
        cmd.append("--output")
        cmd.append(output)
    
    return cmd
