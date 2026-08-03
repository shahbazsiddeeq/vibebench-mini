# src/solution.py

import urllib.parse

def build_query(params):
    if not isinstance(params, dict):
        raise ValueError("Input must be a dictionary.")

    query_parts = []

    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, str) and not isinstance(item, int):
                    raise ValueError("List items must be strings or integers.")
                query_parts.append(f"{urllib.parse.quote_plus(str(key))}={urllib.parse.quote_plus(str(item))}")
        else:
            if not isinstance(value, str) and not isinstance(value, int):
                raise ValueError("Values must be strings or integers.")
            query_parts.append(f"{urllib.parse.quote_plus(str(key))}={urllib.parse.quote_plus(str(value))}")

    return "&".join(query_parts)
