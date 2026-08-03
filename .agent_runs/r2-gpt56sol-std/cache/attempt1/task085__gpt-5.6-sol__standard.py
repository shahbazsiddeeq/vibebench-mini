from urllib.parse import urlencode


def build_query(params: dict) -> str:
    items = []
    for key in sorted(params, key=str):
        value = params[key]
        if isinstance(value, (list, tuple)):
            items.extend((key, item) for item in value)
        else:
            items.append((key, value))
    return urlencode(items)
