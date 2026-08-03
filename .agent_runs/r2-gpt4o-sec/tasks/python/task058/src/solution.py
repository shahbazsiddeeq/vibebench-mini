import csv
import os

def csv_filter(in_path, out_path, column, value):
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"The input file {in_path} does not exist.")
    
    count = 0
    with open(in_path, newline='', mode='r') as infile:
        reader = csv.DictReader(infile)
        
        if column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in the CSV header.")
        
        with open(out_path, newline='', mode='w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            for row in reader:
                if row.get(column) == value:
                    writer.writerow(row)
                    count += 1
    
    return count
