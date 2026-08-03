def group_by_aggregate(records, key_field, value_field):
    """
    Group records by key_field and aggregate values from value_field.
    
    Returns a dict mapping each group key to a dict with 'count', 'sum', and 'mean'.
    """
    if not records:
        return {}
    
    groups = {}
    
    for record in records:
        # Let KeyError propagate if fields are missing
        key = record[key_field]
        value = record[value_field]
        
        if key not in groups:
            groups[key] = {'count': 0, 'sum': 0.0, 'values': []}
        
        groups[key]['count'] += 1
        groups[key]['sum'] += float(value)
        groups[key]['values'].append(value)
    
    # Calculate means and clean up
    result = {}
    for key, group_data in groups.items():
        count = group_data['count']
        total_sum = group_data['sum']
        mean = round(total_sum / count, 4)
        
        result[key] = {
            'count': count,
            'sum': total_sum,
            'mean': mean
        }
    
    return result
