import csv

def csv_filter(in_path, out_path, column, value):
    with open(in_path, newline='') as infile:
        reader = csv.DictReader(infile)
        if column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in header.")
        
        filtered_rows = [row for row in reader if row[column] == value]
    
    with open(out_path, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)
    
    return len(filtered_rows)
