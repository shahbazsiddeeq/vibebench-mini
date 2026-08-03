import csv


def column_mean(path, col):
    values = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or col not in reader.fieldnames:
            raise ValueError(f"Column '{col}' not found in CSV header")
        for row in reader:
            raw = row.get(col)
            if raw is None:
                continue
            try:
                values.append(float(raw))
            except (ValueError, TypeError):
                continue
    if not values:
        raise ValueError(f"No numeric values found in column '{col}'")
    return sum(values) / len(values)
