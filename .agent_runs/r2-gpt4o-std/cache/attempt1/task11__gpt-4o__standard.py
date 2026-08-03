def build_cmd(base, args):
    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, list) and all(isinstance(item, str) for item in base):
        cmd = base[:]
    else:
        raise ValueError("Base must be a string or a list of strings.")

    for key, value in args.items():
        if key == "verbose":
            if isinstance(value, bool):
                if value:
                    cmd.append("--verbose")
            else:
                raise ValueError("Verbose must be a boolean.")
        elif key == "timeout":
            if isinstance(value, int) and value > 0 and not isinstance(value, bool):
                cmd.extend(["--timeout", str(value)])
            else:
                raise ValueError("Timeout must be a strictly positive integer.")
        elif key == "output":
            if isinstance(value, str) and '\0' not in value and '\n' not in value and '\r' not in value:
                cmd.extend(["--output", value])
            else:
                raise ValueError("Output must be a string without NUL, newline, or carriage-return characters.")
        else:
            raise ValueError(f"Unknown argument key: {key}")

    return cmd
