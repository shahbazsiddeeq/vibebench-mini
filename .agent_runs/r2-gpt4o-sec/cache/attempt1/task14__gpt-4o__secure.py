import csv
from collections import OrderedDict

def dedupe_csv(in_path, out_path, key):
    """
    Reads a CSV file, removes duplicate rows based on the specified key,
    and writes the result to another CSV file, keeping only the last occurrence
    of each key. Returns the number of data rows written.
    
    :param in_path: Path to the input CSV file.
    :param out_path: Path to the output CSV file.
    :param key: The column name to deduplicate by.
    :return: Number of data rows written to the output file.
    :raises KeyError: If the key column is absent from the header.
    """
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
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
