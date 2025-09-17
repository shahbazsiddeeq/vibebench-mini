import json

import yaml  # PyYAML is already in requirements.txt


def yaml_to_json(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
