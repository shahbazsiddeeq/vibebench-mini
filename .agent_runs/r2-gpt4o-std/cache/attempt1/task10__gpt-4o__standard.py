import json
import yaml

def yaml_to_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise e

    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
