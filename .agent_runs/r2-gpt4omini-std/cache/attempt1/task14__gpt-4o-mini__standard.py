import csv
from collections import OrderedDict

def dedupe_csv(in_path, out_path, key):
    with open(in_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Check if the key exists in the header
        if key not in reader.fieldnames:
            raise KeyError(f"Key '{key}' not found in CSV header.")
        
        # Use an OrderedDict to maintain the order of last occurrences
        deduped_data = OrderedDict()
        
        for row in reader:
            deduped_data[row[key]] = row
        
    # Write the deduped data to the output CSV
    with open(out_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in deduped_data.values():
            writer.writerow(row)
    
    return len(deduped_data)
