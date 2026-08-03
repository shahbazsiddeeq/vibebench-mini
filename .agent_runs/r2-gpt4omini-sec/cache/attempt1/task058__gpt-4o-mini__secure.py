# src/solution.py

import csv
import os

def csv_filter(in_path: str, out_path: str, column: str, value: str) -> int:
    # Validate input paths
    if not isinstance(in_path, str) or not isinstance(out_path, str):
        raise ValueError("Input and output paths must be strings.")
    
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"The input file {in_path} does not exist.")
    
    if not in_path.endswith('.csv') or not out_path.endswith('.csv'):
        raise ValueError("Both input and output paths must be CSV files.")

    count = 0

    with open(in_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Check if the column exists in the header
        if column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in the CSV header.")
        
        with open(out_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()  # Write the header to the output file
            
            for row in reader:
                if row[column] == value:
                    writer.writerow(row)
                    count += 1

    return count
