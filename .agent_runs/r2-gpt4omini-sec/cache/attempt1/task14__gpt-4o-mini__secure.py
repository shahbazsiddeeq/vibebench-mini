import csv
import os

def dedupe_csv(in_path: str, out_path: str, key: str) -> int:
    # Validate input paths
    if not isinstance(in_path, str) or not isinstance(out_path, str) or not isinstance(key, str):
        raise ValueError("in_path, out_path, and key must be strings.")
    
    # Check if input file exists
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"The input file {in_path} does not exist.")
    
    # Read the input CSV
    with open(in_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Check if the key exists in the header
        if key not in reader.fieldnames:
            raise KeyError(f"The key '{key}' is not present in the CSV header.")
        
        # Store the last occurrence of each key
        last_occurrences = {}
        for row in reader:
            last_occurrences[row[key]] = row
    
    # Write the output CSV
    with open(out_path, mode='w', encoding='utf-8', newline='') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write the rows in the order of their last occurrence
        for row in last_occurrences.values():
            writer.writerow(row)
    
    return len(last_occurrences)
