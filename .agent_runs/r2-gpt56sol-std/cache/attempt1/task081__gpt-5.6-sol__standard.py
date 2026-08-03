def diff_records(old, new, key):
    """Compare two record collections using *key* as the record identifier."""
    old_records = list(old)
    new_records = list(new)

    for record in old_records:
        if key not in record:
            raise KeyError(key)
    for record in new_records:
        if key not in record:
            raise KeyError(key)

    old_by_key = {record[key]: record for record in old_records}
    new_by_key = {record[key]: record for record in new_records}

    return {
        "added": [
            record
            for record in new_by_key.values()
            if record[key] not in old_by_key
        ],
        "removed": [
            record
            for record in old_by_key.values()
            if record[key] not in new_by_key
        ],
        "changed": [
            record
            for record in new_by_key.values()
            if record[key] in old_by_key
            and record != old_by_key[record[key]]
        ],
    }
