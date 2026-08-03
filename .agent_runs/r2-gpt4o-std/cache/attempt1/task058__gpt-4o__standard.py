# src/solution.py

import csv

def csv_filter(in_path, out_path, column, value):
    with open(in_path, newline='') as infile:
        reader = csv.DictReader(infile)
        
        if column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in CSV header.")
        
        with open(out_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            count = 0
            for row in reader:
                if row[column] == value:
                    writer.writerow(row)
                    count += 1
    
    return count
