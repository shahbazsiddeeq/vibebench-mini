import urllib.parse

def build_query(params):
    if not isinstance(params, dict):
        raise ValueError("Input must be a dictionary.")

    query_parts = []
    
    for key in sorted(params.keys()):
        if not isinstance(key, str):
            raise ValueError("All keys must be strings.")
        
        value = params[key]
        
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, (str, int)):
                    raise ValueError("List items must be strings or integers.")
                query_parts.append((key, str(item)))
        elif isinstance(value, (str, int)):
            query_parts.append((key, str(value)))
        else:
            raise ValueError("Values must be strings, integers, or lists of these.")
    
    return urllib.parse.urlencode(query_parts, doseq=True)
