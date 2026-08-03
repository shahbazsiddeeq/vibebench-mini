def group_by_aggregate(records, key_field, value_field):
    groups = {}
    for record in records:
        key = record[key_field]
        value = record[value_field]
        if key not in groups:
            groups[key] = {"count": 0, "sum": 0.0}
        groups[key]["count"] += 1
        groups[key]["sum"] += value

    result = {}
    for key, agg in groups.items():
        count = agg["count"]
        total = float(agg["sum"])
        mean = round(total / count, 4)
        result[key] = {"count": count, "sum": total, "mean": mean}

    return result
