def diff_records(old, new, key):
    old_dict = {record[key]: record for record in old}
    new_dict = {record[key]: record for record in new}

    added = []
    removed = []
    changed = []

    for new_key, new_record in new_dict.items():
        if new_key not in old_dict:
            added.append(new_record)
        elif old_dict[new_key] != new_record:
            changed.append(new_record)

    for old_key in old_dict:
        if old_key not in new_dict:
            removed.append(old_dict[old_key])

    return {"added": added, "removed": removed, "changed": changed}
