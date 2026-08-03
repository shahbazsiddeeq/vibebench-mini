def diff_records(old, new, key):
    for rec in old:
        if key not in rec:
            raise KeyError(key)
    for rec in new:
        if key not in rec:
            raise KeyError(key)

    old_map = {rec[key]: rec for rec in old}
    new_map = {rec[key]: rec for rec in new}

    added = [new_map[k] for k in new_map if k not in old_map]
    removed = [old_map[k] for k in old_map if k not in new_map]
    changed = [new_map[k] for k in new_map if k in old_map and new_map[k] != old_map[k]]

    return {"added": added, "removed": removed, "changed": changed}
