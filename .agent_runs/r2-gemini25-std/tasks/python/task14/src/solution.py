import csv
import collections

def dedupe_csv(in_path, out_path, key):
    """
    Reads a CSV with a header row and writes a CSV keeping only the last
    occurrence of each distinct value in column `key`. The header is preserved.
    Output rows are ordered by the position of each key's last occurrence in
    the input (ascending).

    Args:
        in_path (str): Path to the input CSV file.
        out_path (str): Path to the output CSV file.
        key (str): The column name to use for deduplication.

    Returns:
        int: The number of data rows written.

    Raises:
        KeyError: If the `key` column is absent from the header, including
                  when the input is empty or has no header row.
    """
    deduplicated_rows = collections.OrderedDict()
    header = []

    with open(in_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        try:
            header = next(reader)
        except StopIteration:
            # Input file is empty, or has no header.
            # If key is not in header, it's a KeyError.
            # An empty header will not contain any key.
            if key not in header:
                raise KeyError(f"Key '{key}' not found in header.")
            # If header is empty and key is not in it, this case is handled above.
            # If header is empty, and key is not in it, then no rows will be written.
            # This path should not be reached if header is empty.
            pass # This should not be reached if header is empty and key is not in it.

        if key not in header:
            raise KeyError(f"Key '{key}' not found in header.")

        key_index = header.index(key)

        for row in reader:
            if not row:  # Skip empty rows
                continue
            if len(row) > key_index: # Ensure row has enough columns for the key
                deduplicated_rows[row[key_index]] = row

    with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        if header:
            writer.writerow(header)
        
        written_count = 0
        for row in deduplicated_rows.values():
            writer.writerow(row)
            written_count += 1

    return written_count
