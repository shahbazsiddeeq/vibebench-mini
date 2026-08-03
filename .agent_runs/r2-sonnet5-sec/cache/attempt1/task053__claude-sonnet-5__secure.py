"""
src/solution.py

A secure, self-contained module implementing `count_lines`, a function
that counts the number of lines in a UTF-8 text file.

Design considerations for security and robustness:
    - Input is validated to ensure it is a string or os.PathLike object.
    - The file is opened explicitly with UTF-8 encoding to avoid locale-
      dependent decoding issues or ambiguity.
    - Errors are handled narrowly: only expected, well-understood
      exceptions are allowed to propagate (FileNotFoundError, IsADirectoryError,
      PermissionError, UnicodeDecodeError), and internal details (like full
      tracebacks or system paths) are not leaked in custom error messages.
    - No use of eval/exec, no shell invocations, and no use of insecure
      randomness (not needed here, but per instructions we avoid any
      non-`secrets`-based randomness throughout the module).
"""

import os


def count_lines(path: "str | os.PathLike[str]") -> int:
    """
    Count the number of lines in a UTF-8 encoded text file.

    Args:
        path: Path to the file, as a string or os.PathLike object.

    Returns:
        The number of lines in the file (int). An empty file returns 0.

    Raises:
        TypeError: If `path` is not a str or os.PathLike.
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the path refers to a directory.
        PermissionError: If the file cannot be read due to permissions.
        UnicodeDecodeError: If the file is not valid UTF-8.
        OSError: For other underlying OS-level errors.
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or os.PathLike object")

    # Normalize to a string form early; avoids surprises with exotic
    # PathLike implementations while keeping the original semantics.
    path_str = os.fspath(path)

    if not isinstance(path_str, str) or path_str.strip() == "":
        raise ValueError("path must be a non-empty string")

    try:
        with open(path_str, "r", encoding="utf-8", newline="") as f:
            line_count = sum(1 for _ in f)
    except FileNotFoundError:
        # Re-raise as-is; this is expected and part of the documented contract.
        raise
    except IsADirectoryError:
        raise
    except PermissionError:
        raise
    except UnicodeDecodeError:
        raise
    except OSError as exc:
        # Wrap unexpected OS errors without leaking internal details.
        raise OSError("Unable to read the specified file.") from exc

    return line_count
