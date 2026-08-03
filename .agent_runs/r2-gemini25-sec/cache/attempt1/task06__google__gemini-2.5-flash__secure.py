import json
import os

def sum_jsonl(path: str, key: str) -> float:
    """
    Sums numeric values for 'key' over JSON Lines in a file.

    Non-numeric or missing values for the specified key in a row are ignored.
    If no numeric values are found for the key, a ValueError is raised.

    Args:
        path: The path to the JSONL file.
        key: The string key whose values are to be summed.

    Returns:
        The sum of the numeric values for the specified key.

    Raises:
        ValueError: If the file is empty, or if no numeric values are found
                    for the specified key across all lines.
        TypeError: If 'path' or 'key' are not strings.
        FileNotFoundError: If the file specified by 'path' does not exist.
        PermissionError: If there are issues accessing the file.
        OSError: For other OS-related errors during file operations.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")
    if not isinstance(key, str):
        raise TypeError("Key must be a string.")
    if not key:
        raise ValueError("Key cannot be an empty string.")

    total_sum = 0.0
    found_numeric_value = False

    try:
        # Ensure the path is normalized and absolute to prevent directory traversal issues
        # and to provide a consistent path for error messages.
        abs_path = os.path.abspath(path)

        # Basic check to prevent reading from special files or directories
        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"File not found: {path}")
        if os.path.islink(abs_path):
            # Resolve symlinks to prevent unexpected behavior or security risks
            abs_path = os.path.realpath(abs_path)
            if not os.path.isfile(abs_path):
                raise FileNotFoundError(f"Symlink target is not a file: {path}")

        with open(abs_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    data = json.loads(line)
                    if isinstance(data, dict) and key in data:
                        value = data[key]
                        # Only sum if the value is an int or float
                        if isinstance(value, (int, float)):
                            total_sum += float(value)
                            found_numeric_value = True
                except json.JSONDecodeError:
                    # Log or ignore malformed JSON lines, depending on requirements.
                    # For this task, we ignore them as per "non-numeric/missing rows are ignored".
                    pass
                except TypeError as e:
                    # Catch potential type errors during data access if data is not a dict
                    # or other unexpected structures.
                    pass
                except Exception as e:
                    # Catch any other unexpected errors during line processing
                    # and provide a generic message without exposing internal details.
                    pass

    except FileNotFoundError:
        raise # Re-raise as it's an expected error type for the user
    except PermissionError:
        raise PermissionError(f"Permission denied to access file: {path}")
    except OSError as e:
        raise OSError(f"Operating system error accessing file {path}: {e}")
    except Exception as e:
        # Catch any other unexpected exceptions during file opening/reading
        raise RuntimeError(f"An unexpected error occurred while processing the file: {e}")

    if not found_numeric_value:
        raise ValueError(f"No numeric values found for key '{key}' in file '{path}'.")

    return total_sum
