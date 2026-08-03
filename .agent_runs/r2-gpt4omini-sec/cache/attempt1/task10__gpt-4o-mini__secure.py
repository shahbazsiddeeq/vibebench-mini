import json
import yaml
import os

def yaml_to_json(path: str) -> str:
    # Validate the input path
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid file path provided.")
    
    # Check if the file exists and is a file
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    try:
        # Read the YAML file
        with open(path, 'r', encoding='utf-8') as file:
            yaml_content = file.read()
        
        # Load the YAML content safely
        data = yaml.safe_load(yaml_content)
        
        # Handle the case of empty YAML file
        if data is None:
            return "null"
        
        # Convert to JSON with specified options
        json_output = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        return json_output
    
    except yaml.YAMLError as e:
        raise yaml.YAMLError("YAML parsing error: " + str(e))
    except Exception as e:
        raise RuntimeError("An error occurred while processing the file: " + str(e))
