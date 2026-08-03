import csv

def column_mean(path, col):
    total = 0.0
    count = 0
    found_column = False

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        if col not in reader.fieldnames:
            raise ValueError("Column not found")

        found_column = True
        
        for row in reader:
            value = row[col]
            try:
                num = float(value)
                total += num
                count += 1
            except ValueError:
                continue

    if count == 0:
        raise ValueError("No numeric values found in the column")

    return total / count
