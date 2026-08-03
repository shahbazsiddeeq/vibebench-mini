import json
import os

def merge_json_files(paths: list[str], output: str):
    """
    Merges a list of UTF-8 JSON files into a single JSON output file.

    The merge is shallow: only top-level keys are combined. When the same top-level key
    appears in more than one file, the value from the later file in the list replaces
    the earlier value entirely. Files are applied in list order, so the last file
    has highest precedence.

    Args:
        paths: A list of strings, where each string is the path to a UTF-8 JSON file.
               Each file must contain a JSON object at its top level.
        output: The path to the output file where the merged JSON will be written.

    Raises:
        ValueError: If any file's top-level JSON value is not an object, or if
                    a file cannot be read or parsed as valid JSON.
        IOError: If there are issues writing to the output file.
    """
    if not isinstance(paths, list):
        raise TypeError("Input 'paths' must be a list.")
    if not all(isinstance(p, str) for p in paths):
        raise TypeError("All elements in 'paths' must be strings.")
    if not isinstance(output, str):
        raise TypeError("Input 'output' must be a string.")

    merged_data = {}

    for file_path in paths:
        try:
            # Ensure the path is safe and doesn't contain directory traversal attempts
            # This is a basic check; more robust path sanitization might be needed
            # depending on the source of `paths`. For this problem, we assume `paths`
            # are valid file paths.
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
            if not os.path.isfile(file_path):
                raise ValueError(f"Path is not a file: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    current_data = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in file '{file_path}': {e}")

            if not isinstance(current_data, dict):
                raise ValueError(
                    f"Top-level JSON value in file '{file_path}' is not an object."
                )

            merged_data.update(current_data)

        except OSError as e:
            # Catch file-related OS errors (e.g., permission denied)
            raise ValueError(f"Error accessing file '{file_path}': {e}") from e
        except Exception as e:
            # Catch any other unexpected errors during file processing
            raise ValueError(f"An unexpected error occurred with file '{file_path}': {e}") from e

    try:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=None, separators=(',', ':'))
    except OSError as e:
        raise IOError(f"Error writing to output file '{output}': {e}") from e
    except Exception as e:
        raise IOError(f"An unexpected error occurred while writing to '{output}': {e}") from e
