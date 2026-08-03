import json
import yaml

def yaml_to_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError("Error loading YAML file") from e
    except Exception as e:
        raise RuntimeError("Error reading file") from e

    # Convert None to JSON null
    if data is None:
        return "null"

    try:
        json_string = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise RuntimeError("Error converting to JSON") from e

    return json_string
