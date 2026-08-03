import json
import yaml
from pathlib import Path

def yaml_to_json(path: str) -> str:
    """
    Reads a UTF-8 YAML file from the given path and returns its canonical JSON string representation.

    Args:
        path: The path to the YAML file.

    Returns:
        A JSON string with sorted keys, compact separators, and non-ASCII characters
        emitted as-is. YAML dates/datetimes are serialized as their string form.
        An empty YAML file (parses to None) produces the JSON string "null".

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the path points to a directory.
        PermissionError: If there are issues with file permissions.
        yaml.YAMLError: If the YAML content is invalid or contains unsafe constructs.
        json.JSONError: If there's an issue during JSON serialization (unlikely with
                        safe YAML loading and standard types).
        UnicodeDecodeError: If the file is not valid UTF-8.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if file_path.is_dir():
        raise IsADirectoryError(f"Is a directory: '{path}'")
    if not file_path.is_file():
        # This covers cases like symlinks to non-existent files, or special files
        raise FileNotFoundError(f"Not a regular file: '{path}'")

    try:
        # Read the file content as UTF-8
        yaml_content = file_path.read_text(encoding="utf-8")
    except PermissionError as e:
        raise PermissionError(f"Permission denied when reading file: '{path}'") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"File '{path}' is not valid UTF-8: {e}") from e
    except Exception as e:
        # Catch other potential I/O errors
        raise IOError(f"An unexpected I/O error occurred while reading '{path}': {e}") from e

    try:
        # Use yaml.safe_load to prevent arbitrary code execution
        # This will raise YAMLError for unsafe tags
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid or unsafe YAML content in '{path}': {e}") from e

    # Handle empty YAML file which parses to None
    if data is None:
        return "null"

    # Custom JSON encoder to handle types not natively supported by JSON
    # such as datetime.date, datetime.datetime, etc., by converting them to strings.
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (
                yaml.representer.BaseRepresenter.yaml_datetime,
                yaml.representer.BaseRepresenter.yaml_date,
                yaml.representer.BaseRepresenter.yaml_time
            )):
                return str(obj)
            # Let the base class default method raise the TypeError for other unsupported types
            return json.JSONEncoder.default(self, obj)

    try:
        # Serialize to JSON with specified requirements
        json_string = json.dumps(
            data,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),  # Compact separators
            cls=CustomJSONEncoder # Use custom encoder for non-native types
        )
        return json_string
    except json.JSONError as e:
        # This is unlikely if yaml.safe_load produces standard Python types,
        # but good to catch for robustness.
        raise json.JSONError(f"Failed to serialize YAML data to JSON: {e}") from e
    except Exception as e:
        # Catch any other unexpected errors during JSON serialization
        raise RuntimeError(f"An unexpected error occurred during JSON serialization: {e}") from e
