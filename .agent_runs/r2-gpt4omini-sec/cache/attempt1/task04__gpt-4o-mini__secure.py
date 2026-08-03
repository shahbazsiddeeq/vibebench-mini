# src/solution.py

import csv
import os

def column_mean(path: str, col: str) -> float:
    # Validate inputs
    if not isinstance(path, str) or not isinstance(col, str):
        raise ValueError("Invalid input types. 'path' and 'col' must be strings.")
    
    # Check if the file exists
    if not os.path.isfile(path):
        raise ValueError("The specified file does not exist.")
    
    total = 0.0
    count = 0
    found_column = False

    try:
        with open(path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if col not in reader.fieldnames:
                raise ValueError("Column not found in the CSV file.")
            found_column = True
            
            for row in reader:
                value = row.get(col)
                if value is not None:
                    try:
                        num_value = float(value)
                        total += num_value
                        count += 1
                    except ValueError:
                        # Skip non-numeric values
                        continue

    except Exception as e:
        raise ValueError("An error occurred while processing the CSV file.") from e

    if count == 0:
        if not found_column:
            raise ValueError("Column not found in the CSV file.")
        raise ValueError("No numeric values found in the specified column.")

    return total / count
