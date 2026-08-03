def power_set(elements: list) -> list[frozenset]:
    result = [frozenset()]
    for item in elements:
        result = result + [s | {item} for s in result]
    unique = []
    seen = set()
    for s in result:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return sorted(unique, key=lambda s: (len(s), sorted(str(x) for x in s)))
