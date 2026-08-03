import csv
import os

def column_mean(path, col):
    if not os.path.isfile(path):
        raise ValueError("File does not exist")

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if col not in reader.fieldnames:
            raise ValueError(f"Column '{col}' not found in CSV header")

        total = 0.0
        count = 0

        for row in reader:
            try:
                value = float(row[col])
                total += value
                count += 1
            except (ValueError, TypeError):
                continue

        if count == 0:
            raise ValueError("No numeric values found in the column")

        return total / count
