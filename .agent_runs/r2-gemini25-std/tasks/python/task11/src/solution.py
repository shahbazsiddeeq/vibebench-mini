def build_cmd(base, args):
    """
    Builds an argument list for subprocess (no shell).

    Args:
        base: Either a str (the program name) or a list of str (program plus leading args).
              The result starts with those tokens in order.
        args: A dict whose allowed keys and value types are:
            - verbose: must be a bool. If True, append "--verbose"; if False, append nothing.
            - timeout: must be a strictly positive int. bool is NOT accepted.
                       Appends "--timeout" followed by str(value).
            - output: must be a str containing no NUL, newline, or carriage-return characters.
                      Appends "--output" followed by the string.

    Returns:
        A list of strings representing the command and its arguments.

    Raises:
        ValueError: If any unknown key, or a value of the wrong type or out of range, is provided.
    """
    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, list):
        cmd = list(base)
    else:
        raise ValueError("Base must be a string or a list of strings.")

    for key, value in args.items():
        if key == "verbose":
            if not isinstance(value, bool):
                raise ValueError("Value for 'verbose' must be a boolean.")
            if value:
                cmd.append("--verbose")
        elif key == "timeout":
            if not isinstance(value, int) or isinstance(value, bool):  # bool is a subclass of int
                raise ValueError("Value for 'timeout' must be a strictly positive integer (not boolean).")
            if value <= 0:
                raise ValueError("Value for 'timeout' must be strictly positive.")
            cmd.append("--timeout")
            cmd.append(str(value))
        elif key == "output":
            if not isinstance(value, str):
                raise ValueError("Value for 'output' must be a string.")
            if '\0' in value or '\n' in value or '\r' in value:
                raise ValueError("Value for 'output' cannot contain NUL, newline, or carriage-return characters.")
            cmd.append("--output")
            cmd.append(value)
        else:
            raise ValueError(f"Unknown argument key: {key}")

    return cmd
