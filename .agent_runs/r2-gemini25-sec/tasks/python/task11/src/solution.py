import collections.abc

def build_cmd(base, args):
    """
    Builds an argument list for subprocess (no shell).

    Args:
        base: Either a str (the program name) or a list of str (program plus leading args).
              The result starts with these tokens in order.
        args: A dict whose allowed keys and value types are:
            - verbose: Must be a bool. If True, append "--verbose"; if False, append nothing.
            - timeout: Must be a strictly positive int. bool is NOT accepted.
                       Appends "--timeout" followed by str(value).
            - output: Must be a str containing no NUL, newline, or carriage-return characters.
                      Appends "--output" followed by the string.

    Returns:
        A list of strings representing the command and its arguments.

    Raises:
        ValueError: If any unknown key is provided, or a value of the wrong type or out of range.
    """
    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, collections.abc.Sequence) and not isinstance(base, (str, bytes)):
        cmd = []
        for item in base:
            if not isinstance(item, str):
                raise ValueError("Base list elements must be strings.")
            cmd.append(item)
    else:
        raise ValueError("Base must be a string or a list of strings.")

    if not isinstance(args, dict):
        raise ValueError("Args must be a dictionary.")

    for key, value in args.items():
        if key == "verbose":
            if not isinstance(value, bool):
                raise ValueError("Value for 'verbose' must be a boolean.")
            if value:
                cmd.append("--verbose")
        elif key == "timeout":
            if not isinstance(value, int) or isinstance(value, bool): # bool is a subclass of int
                raise ValueError("Value for 'timeout' must be a strictly positive integer (not boolean).")
            if value <= 0:
                raise ValueError("Value for 'timeout' must be strictly positive.")
            cmd.extend(["--timeout", str(value)])
        elif key == "output":
            if not isinstance(value, str):
                raise ValueError("Value for 'output' must be a string.")
            if '\0' in value or '\n' in value or '\r' in value:
                raise ValueError("Value for 'output' cannot contain NUL, newline, or carriage-return characters.")
            cmd.extend(["--output", value])
        else:
            raise ValueError(f"Unknown argument key: {key}")

    return cmd
