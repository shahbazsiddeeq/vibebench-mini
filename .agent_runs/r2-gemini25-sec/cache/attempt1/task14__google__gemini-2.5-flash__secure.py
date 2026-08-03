import csv
import os

def dedupe_csv(in_path, out_path, key):
    """
    Reads a CSV with a header row and writes a CSV keeping only the last
    occurrence of each distinct value in column `key`. The header is preserved.
    Output rows are ordered by the position of each key's last occurrence in
    the input (ascending).

    Args:
        in_path (str): The path to the input CSV file.
        out_path (str): The path to the output CSV file.
        key (str): The name of the column to use for deduplication.

    Returns:
        int: The number of data rows written to the output file.

    Raises:
        KeyError: If the `key` column is absent from the header, including when
                  the input is empty or has no header row.
        FileNotFoundError: If in_path does not exist.
        IOError: For other input/output related errors.
    """
    if not isinstance(in_path, str) or not in_path:
        raise ValueError("in_path must be a non-empty string.")
    if not isinstance(out_path, str) or not out_path:
        raise ValueError("out_path must be a non-empty string.")
    if not isinstance(key, str) or not key:
        raise ValueError("key must be a non-empty string.")

    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")

    last_occurrences = {}
    header = None
    
    try:
        with open(in_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            
            try:
                header = next(reader)
            except StopIteration:
                # File is empty, or only contains a header that we couldn't read
                # If header is None, it means no header was read.
                # If header is an empty list, it means an empty line was read as header.
                # In both cases, if key is not found, it's a KeyError.
                if key not in []: # This will always be true, ensuring KeyError if no header
                    raise KeyError(f"Key '{key}' not found in header (input file might be empty or malformed).")
            
            if key not in header:
                raise KeyError(f"Key '{key}' not found in header: {header}")

            key_index = header.index(key)
            
            for i, row in enumerate(reader):
                if len(row) != len(header):
                    # Skip malformed rows, or handle as an error if strictness is needed
                    # For this task, we'll just skip.
                    continue
                
                current_key_value = row[key_index]
                last_occurrences[current_key_value] = (i, row) # Store original row index and row data

    except Exception as e:
        # Catch potential errors during file reading or CSV parsing
        if isinstance(e, KeyError):
            raise # Re-raise KeyError as it's a specific requirement
        raise IOError(f"Error reading input CSV file: {e}")

    if header is None:
        # This case should ideally be caught by the KeyError above if key is not in header.
        # However, if the file was truly empty and no header was read, and the key check
        # somehow passed (e.g., if header was initialized to an empty list), this ensures
        # a KeyError.
        raise KeyError(f"Key '{key}' not found in header (input file might be empty or malformed).")

    # Sort the rows based on their original last occurrence index
    sorted_rows = sorted(last_occurrences.values(), key=lambda x: x[0])
    
    written_rows_count = 0
    try:
        with open(out_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            for _, row_data in sorted_rows:
                writer.writerow(row_data)
                written_rows_count += 1
    except Exception as e:
        raise IOError(f"Error writing output CSV file: {e}")

    return written_rows_count
