import csv
from collections import OrderedDict

def dedupe_csv(in_path, out_path, key):
    try:
        with open(in_path, mode='r', encoding='utf-8', newline='') as infile:
            reader = csv.DictReader(infile)
            
            if key not in reader.fieldnames:
                raise KeyError(f"Key '{key}' not found in CSV header.")
            
            # Use an OrderedDict to keep track of the last occurrence of each key
            last_occurrence = OrderedDict()
            for row in reader:
                last_occurrence[row[key]] = row

        with open(out_path, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in last_occurrence.values():
                writer.writerow(row)

        return len(last_occurrence)

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {in_path}")
    except csv.Error as e:
        raise csv.Error(f"CSV error: {e}")
    except KeyError as e:
        raise e
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
