def build_cmd(base, args):
    import secrets

    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, list) and all(isinstance(item, str) for item in base):
        cmd = base[:]
    else:
        raise ValueError("Base must be a string or a list of strings.")

    if not isinstance(args, dict):
        raise ValueError("Args must be a dictionary.")

    for key, value in args.items():
        if key == "verbose":
            if not isinstance(value, bool):
                raise ValueError("Verbose must be a boolean.")
            if value:
                cmd.append("--verbose")
        elif key == "timeout":
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError("Timeout must be a strictly positive integer.")
            cmd.extend(["--timeout", str(value)])
        elif key == "output":
            if not isinstance(value, str) or any(c in value for c in '\0\n\r'):
                raise ValueError("Output must be a string without NUL, newline, or carriage-return characters.")
            cmd.extend(["--output", value])
        else:
            raise ValueError(f"Unknown argument key: {key}")

    return cmd
