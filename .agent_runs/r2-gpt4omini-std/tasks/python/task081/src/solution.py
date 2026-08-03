# src/solution.py

def diff_records(old, new, key):
    old_dict = {record[key]: record for record in old}
    new_dict = {record[key]: record for record in new}

    added = [record for record in new if record[key] not in old_dict]
    removed = [record for record in old if record[key] not in new_dict]
    changed = [
        new_record for new_key, new_record in new_dict.items()
        if new_key in old_dict and old_dict[new_key] != new_record
    ]

    # Check for missing keys
    for record in old + new:
        if key not in record:
            raise KeyError(f"Key '{key}' is missing from record: {record}")

    return {"added": added, "removed": removed, "changed": changed}
