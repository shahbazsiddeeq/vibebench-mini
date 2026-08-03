def group_by_aggregate(records, key_field, value_field):
    """
    Group records by key_field and aggregate values from value_field.
    
    Args:
        records: List of dicts
        key_field: Field name to group by
        value_field: Field name to aggregate
        
    Returns:
        Dict mapping group keys to {'count': int, 'sum': float, 'mean': float}
    """
    if not records:
        return {}
    
    # Group records by key_field
    groups = {}
    for record in records:
        # Let KeyError propagate if fields are missing
        key = record[key_field]
        value = record[value_field]
        
        if key not in groups:
            groups[key] = []
        groups[key].append(value)
    
    # Calculate aggregates for each group
    result = {}
    for key, values in groups.items():
        count = len(values)
        total = float(sum(values))
        mean = round(total / count, 4)
        
        result[key] = {
            'count': count,
            'sum': total,
            'mean': mean
        }
    
    return result
