"""Safe CLI Arg Builder module."""

from typing import Union, List, Dict, Any


def build_cmd(base: Union[str, List[str]], args: Dict[str, Any]) -> List[str]:
    if isinstance(base, str):
        cmd: List[str] = [base]
    elif isinstance(base, list):
        if not all(isinstance(x, str) for x in base):
            raise ValueError("base list must contain only strings")
        cmd = list(base)
    else:
        raise ValueError("base must be a str or list of str")

    if not isinstance(args, dict):
        raise ValueError("args must be a dict")

    allowed_keys = {"verbose", "timeout", "output"}

    for key in args:
        if key not in allowed_keys:
            raise ValueError(f"Unknown key: {key}")

    if "verbose" in args:
        value = args["verbose"]
        if not isinstance(value, bool):
            raise ValueError("verbose must be a bool")
        if value:
            cmd.append("--verbose")

    if "timeout" in args:
        value = args["timeout"]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("timeout must be a strictly positive int (not bool)")
        if value <= 0:
            raise ValueError("timeout must be strictly positive")
        cmd.append("--timeout")
        cmd.append(str(value))

    if "output" in args:
        value = args["output"]
        if not isinstance(value, str):
            raise ValueError("output must be a str")
        if "\0" in value or "\n" in value or "\r" in value:
            raise ValueError("output must not contain NUL, newline, or carriage-return characters")
        cmd.append("--output")
        cmd.append(value)

    return cmd
