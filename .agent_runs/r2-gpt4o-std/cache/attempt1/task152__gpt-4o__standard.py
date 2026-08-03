import re
import os

def parse_dotenv(path: str) -> dict[str, str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    env_vars = {}
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

            if raw_value.startswith('"') and raw_value.endswith('"'):
                value = raw_value[1:-1]
                value = value.replace(r'\n', '\n').replace(r'\t', '\t')
                value = value.replace(r'\r', '\r').replace(r'\\', '\\')
                value = value.replace(r'\"', '"')
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                value = raw_value[1:-1]
            else:
                comment_index = raw_value.find('#')
                if comment_index != -1 and (comment_index == 0 or raw_value[comment_index - 1].isspace()):
                    raw_value = raw_value[:comment_index]
                value = raw_value.strip()

            env_vars[key] = value

    return env_vars
