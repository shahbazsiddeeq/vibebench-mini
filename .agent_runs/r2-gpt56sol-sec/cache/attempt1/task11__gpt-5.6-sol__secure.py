"""Safely construct subprocess argument lists without invoking a shell."""

from typing import Any


def build_cmd(base: str | list[str], args: dict[str, Any]) -> list[str]:
    """Build a command argument list from a base command and supported options."""
    if isinstance(base, str):
        command = [base]
    elif isinstance(base, list):
        if not all(isinstance(token, str) for token in base):
            raise ValueError("base must contain only strings")
        command = list(base)
    else:
        raise ValueError("base must be a string or a list of strings")

    if not isinstance(args, dict):
        raise ValueError("args must be a dictionary")

    allowed_keys = {"verbose", "timeout", "output"}
    if any(key not in allowed_keys for key in args):
        raise ValueError("args contains an unknown option")

    if "verbose" in args:
        verbose = args["verbose"]
        if not isinstance(verbose, bool):
            raise ValueError("verbose must be a boolean")
        if verbose:
            command.append("--verbose")

    if "timeout" in args:
        timeout = args["timeout"]
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout must be a strictly positive integer")
        command.extend(("--timeout", str(timeout)))

    if "output" in args:
        output = args["output"]
        if not isinstance(output, str):
            raise ValueError("output must be a string")
        if any(character in output for character in ("\x00", "\n", "\r")):
            raise ValueError("output contains a forbidden character")
        command.extend(("--output", output))

    return command
