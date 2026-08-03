import secrets

def diff_records(old, new, key):
    """
    Compares two lists of records and returns the differences.

    Args:
        old (list): A list of dictionaries representing the old records.
        new (list): A list of dictionaries representing the new records.
        key (str): The key to use for identifying unique records.

    Returns:
        dict: A dictionary with three keys:
              - "added": Records present in 'new' but not in 'old'.
              - "removed": Records present in 'old' but not in 'new'.
              - "changed": Records present in both, but with differing values
                           (excluding the key itself).

    Raises:
        KeyError: If the specified 'key' is missing from any record in
                  either the 'old' or 'new' lists.
        TypeError: If 'old' or 'new' are not lists, or if records are not dicts,
                   or if 'key' is not a string.
        ValueError: If 'key' is an empty string.
    """
    if not isinstance(old, list):
        raise TypeError("Input 'old' must be a list.")
    if not isinstance(new, list):
        raise TypeError("Input 'new' must be a list.")
    if not isinstance(key, str):
        raise TypeError("Input 'key' must be a string.")
    if not key:
        raise ValueError("Input 'key' cannot be an empty string.")

    old_map = {}
    for i, record in enumerate(old):
        if not isinstance(record, dict):
            raise TypeError(f"Record at old[{i}] is not a dictionary.")
        if key not in record:
            raise KeyError(f"Key '{key}' missing from old record: {record}")
        old_map[record[key]] = record

    new_map = {}
    for i, record in enumerate(new):
        if not isinstance(record, dict):
            raise TypeError(f"Record at new[{i}] is not a dictionary.")
        if key not in record:
            raise KeyError(f"Key '{key}' missing from new record: {record}")
        new_map[record[key]] = record

    added = []
    removed = []
    changed = []

    # Find added and changed records
    for new_key_val, new_record in new_map.items():
        if new_key_val not in old_map:
            added.append(new_record)
        else:
            old_record = old_map[new_key_val]
            # Compare records, excluding the key itself
            if any(old_record.get(k) != v for k, v in new_record.items() if k != key) or \
               any(k not in new_record for k in old_record if k != key):
                changed.append(new_record)

    # Find removed records
    for old_key_val, old_record in old_map.items():
        if old_key_val not in new_map:
            removed.append(old_record)

    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
