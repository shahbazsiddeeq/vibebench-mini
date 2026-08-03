from urllib.parse import quote_plus


def build_query(params):
    pairs = []
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, list):
            for v in value:
                pairs.append(f"{quote_plus(str(key))}={quote_plus(str(v))}")
        else:
            pairs.append(f"{quote_plus(str(key))}={quote_plus(str(value))}")
    return "&".join(pairs)
