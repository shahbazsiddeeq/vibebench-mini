import json
import yaml


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle YAML dates/datetimes by converting them to their string representation
        if isinstance(obj, (yaml.timestamp.Timestamp, yaml.representer.BaseRepresenter.yaml_representers)):
            return str(obj)
        # Let the base class default method raise the TypeError for other types
        return json.JSONEncoder.default(self, obj)


def yaml_to_json(path: str) -> str:
    """
    Reads a UTF-8 YAML file at `path` and returns a canonical JSON string.

    - Loads with PyYAML's safe loader (yaml.safe_load).
    - JSON has keys sorted (sort_keys=True) and compact separators.
    - Non-ASCII characters are emitted as-is (ensure_ascii=False).
    - YAML dates/datetimes are serialized as their string form.
    - An empty YAML file (parses to None) produces the JSON string "null".
    """
    with open(path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    # Handle the case where the YAML file is empty, which yaml.safe_load parses to None
    if yaml_data is None:
        return "null"

    # Convert the loaded YAML data to a JSON string with specified formatting
    json_string = json.dumps(
        yaml_data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(',', ':'),
        cls=CustomJSONEncoder  # Use custom encoder to handle specific YAML types
    )
    return json_string
