import json


def merge_json_files(paths, output):
    result = {}
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError(f"File {path} does not contain a JSON object")
        result.update(data)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f)

    return result
