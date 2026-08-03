import json

import yaml


def yaml_to_json(path):
    with open(path, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)

    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )
