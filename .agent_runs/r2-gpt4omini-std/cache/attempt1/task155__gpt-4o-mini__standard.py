def group_by_aggregate(records, key_field, value_field):
    if not records:
        return {}
    
    aggregated_data = {}
    
    for record in records:
        key = record[key_field]
        value = record[value_field]
        
        if key not in aggregated_data:
            aggregated_data[key] = {'count': 0, 'sum': 0.0}
        
        aggregated_data[key]['count'] += 1
        aggregated_data[key]['sum'] += float(value)
    
    for key, data in aggregated_data.items():
        data['mean'] = round(data['sum'] / data['count'], 4)
    
    return aggregated_data
