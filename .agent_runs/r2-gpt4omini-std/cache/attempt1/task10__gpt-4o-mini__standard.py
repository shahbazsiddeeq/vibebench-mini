import json
import yaml

def yaml_to_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        if not content.strip():
            return "null"
        
        data = yaml.safe_load(content)
        
        # Handle the case where data is None
        if data is None:
            return "null"
        
        # Convert to JSON with specified options
        return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
