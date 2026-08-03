def group_by_aggregate(records, key_field, value_field):
    from collections import defaultdict

    # Initialize a dictionary to hold the aggregated data
    groups = defaultdict(lambda: {'count': 0, 'sum': 0.0})

    # Process each record
    for record in records:
        # Extract key and value, let KeyError propagate if missing
        key = record[key_field]
        value = record[value_field]

        # Update the group's count and sum
        groups[key]['count'] += 1
        groups[key]['sum'] += float(value)

    # Calculate mean for each group and prepare the final result
    result = {}
    for key, data in groups.items():
        count = data['count']
        total_sum = data['sum']
        mean = round(total_sum / count, 4)
        result[key] = {'count': count, 'sum': total_sum, 'mean': mean}

    return result
