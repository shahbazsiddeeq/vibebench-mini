import re
import os

def parse_dotenv(path: str) -> dict[str, str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    dotenv_dict = {}
    key_regex = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('export '):
                line = line[len('export '):]
            
            if '=' not in line:
                raise ValueError("Line does not contain '=': " + line)
            
            key, raw_value = line.split('=', 1)
            key = key.strip()
            
            if not key_regex.match(key):
                raise ValueError(f"Invalid key: {key}")
            
            value = parse_value(raw_value)
            dotenv_dict[key] = value
    
    return dotenv_dict

def parse_value(raw_value: str) -> str:
    raw_value = raw_value.strip()
    
    if raw_value.startswith('"') and raw_value.endswith('"'):
        value = raw_value[1:-1]
        value = value.replace(r'\n', '\n')
        value = value.replace(r'\t', '\t')
        value = value.replace(r'\r', '\r')
        value = value.replace(r'\\', '\\')
        value = value.replace(r'\"', '"')
    elif raw_value.startswith("'") and raw_value.endswith("'"):
        value = raw_value[1:-1]
    else:
        if '#' in raw_value:
            hash_index = raw_value.find('#')
            if hash_index == 0 or raw_value[hash_index - 1].isspace():
                raw_value = raw_value[:hash_index]
        value = raw_value.strip()
    
    return value
