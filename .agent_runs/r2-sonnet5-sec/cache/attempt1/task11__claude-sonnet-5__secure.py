"""
Safe CLI Arg Builder
=====================

This module provides a single public function, :func:`build_cmd`, which
safely constructs a list of command-line arguments suitable for passing to
``subprocess.run`` (or similar APIs) with ``shell=False``.

Design goals / security considerations
---------------------------------------
* Never build a shell command string -- always return a list of discrete
  tokens so that no shell interpretation, quoting, or injection can occur.
* Strictly validate every input: unknown keys and values of the wrong type
  (including subtle cases like ``bool`` being a subclass of ``int``) are
  rejected with a ``ValueError``.
* String values are checked for embedded NUL / newline / carriage-return
  characters, which could be used to smuggle extra "lines" of input into
  argument-consuming programs or logs.
* No use of ``eval``/``exec``/shell invocation of any kind.
* Error messages are generic and do not leak internal state.
"""

from __future__ import annotations

from typing import Any, Dict, List, Union

__all__ = ["build_cmd"]

# Characters that are not allowed inside string argument values because they
# could be used to inject additional lines/content into files, logs, or
# downstream parsers that split on these characters.
_FORBIDDEN_STR_CHARS = ("\x00", "\n", "\r")


def _validate_base(base: Union[str, List[str]]) -> List[str]:
    """Validate and normalize the `base` argument into a list of strings."""
    if isinstance(base, str):
        return [base]

    if isinstance(base, list):
        if not all(isinstance(item, str) for item in base):
            raise ValueError("base list must contain only strings")
        return list(base)

    raise ValueError("base must be a str or a list of str")


def _validate_verbose(value: Any) -> List[str]:
    # Must be exactly a bool; reject ints/other truthy/falsy values.
    if not isinstance(value, bool):
        raise ValueError("verbose must be a bool")
    return ["--verbose"] if value else []


def _validate_timeout(value: Any) -> List[str]:
    # bool is a subclass of int in Python, so explicitly exclude it.
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("timeout must be a strictly positive int")
    if value <= 0:
        raise ValueError("timeout must be a strictly positive int")
    return ["--timeout", str(value)]


def _validate_output(value: Any) -> List[str]:
    if not isinstance(value, str):
        raise ValueError("output must be a str")
    if any(ch in value for ch in _FORBIDDEN_STR_CHARS):
        raise ValueError("output contains forbidden characters")
    return ["--output", value]


# Mapping of allowed keys to their validator functions.
_VALIDATORS = {
    "verbose": _validate_verbose,
    "timeout": _validate_timeout,
    "output": _validate_output,
}


def build_cmd(base: Union[str, List[str]], args: Dict[str, Any]) -> List[str]:
    """
    Build a safe command-line argument list.

    Parameters
    ----------
    base:
        Either a string (the program name) or a list of strings
        (program plus leading fixed arguments). The resulting command
        always starts with these tokens, in order.
    args:
        A dict of allowed keys (``verbose``, ``timeout``, ``output``)
        mapping to appropriately typed values, as described in the
        module docstring.

    Returns
    -------
    list of str
        The full command, ready to be passed to a subprocess API with
        ``shell=False``.

    Raises
    ------
    ValueError
        If `base` or `args` (or any of its values) is invalid.
    """
    cmd = _validate_base(base)

    if not isinstance(args, dict):
        raise ValueError("args must be a dict")

    for key, value in args.items():
        if not isinstance(key, str) or key not in _VALIDATORS:
            raise ValueError("unknown argument key")
        cmd.extend(_VALIDATORS[key](value))

    return cmd
