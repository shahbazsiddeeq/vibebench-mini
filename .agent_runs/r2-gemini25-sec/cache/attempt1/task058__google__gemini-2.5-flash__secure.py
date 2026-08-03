import csv
import os

def csv_filter(in_path: str, out_path: str, column: str, value: str) -> int:
    """
    Filters a CSV file, writing rows where a specified column matches a given value
    to a new CSV file.

    Args:
        in_path: The path to the input CSV file.
        out_path: The path to the output CSV file.
        column: The name of the column to filter by.
        value: The value to match in the specified column.

    Returns:
        The count of data rows written to the output file.

    Raises:
        FileNotFoundError: If in_path does not exist.
        IsADirectoryError: If in_path is a directory.
        PermissionError: If there are issues accessing in_path or out_path.
        KeyError: If the specified column is not found in the CSV header.
        ValueError: If in_path or out_path are not valid file paths.
        csv.Error: For general CSV parsing or writing errors.
    """

    if not isinstance(in_path, str) or not in_path:
        raise ValueError("Input path must be a non-empty string.")
    if not isinstance(out_path, str) or not out_path:
        raise ValueError("Output path must be a non-empty string.")
    if not isinstance(column, str) or not column:
        raise ValueError("Column name must be a non-empty string.")
    if not isinstance(value, str):
        raise ValueError("Value must be a string.")

    # Validate paths for security and robustness
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")
    if not os.path.isfile(in_path):
        raise IsADirectoryError(f"Input path is a directory, not a file: {in_path}")

    # Ensure output directory exists if specified, but don't create it here
    # The open() call will handle creating the file itself.
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        # This is a security-conscious approach: we don't create directories
        # automatically. If the user wants to write to a non-existent directory,
        # they should create it themselves.
        raise FileNotFoundError(f"Output directory does not exist: {out_dir}")
    if out_dir and not os.path.isdir(out_dir):
        raise NotADirectoryError(f"Output directory path is not a directory: {out_dir}")

    written_rows_count = 0
    fieldnames = []

    try:
        with open(in_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)

            try:
                header = next(reader)
            except StopIteration:
                # Handle empty file case: write an empty file with no header
                with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
                    pass # Create an empty file
                return 0
            except csv.Error as e:
                raise csv.Error(f"Error reading CSV header from {in_path}: {e}")

            fieldnames = [h.strip() for h in header] # Sanitize header names

            if column not in fieldnames:
                raise KeyError(f"Column '{column}' not found in CSV header: {', '.join(fieldnames)}")

            # Use DictReader for easier column access, but we already have the header
            # so we can reconstruct it.
            # We need to re-open the file or seek to the beginning if we want to use DictReader
            # directly after reading the header with csv.reader.
            # A simpler approach is to manually map rows to dicts.

            # Prepare for writing
            with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                # Process remaining rows
                for row_num, row_list in enumerate(reader, start=2): # start=2 for data rows after header
                    if len(row_list) != len(fieldnames):
                        # Log or handle malformed row, for now, skip it
                        # For security, we don't expose internal row structure
                        continue

                    row_dict = dict(zip(fieldnames, row_list))

                    # Sanitize input data before comparison if necessary,
                    # but for direct string comparison, it's usually fine.
                    # If 'value' could contain malicious code or special characters
                    # that affect interpretation, further sanitization would be needed.
                    # Here, we assume direct string comparison is safe.
                    if row_dict.get(column) == value:
                        writer.writerow(row_dict)
                        written_rows_count += 1

    except FileNotFoundError:
        raise # Re-raise specific error
    except IsADirectoryError:
        raise # Re-raise specific error
    except PermissionError as e:
        raise PermissionError(f"Permission denied for file operation on {in_path} or {out_path}: {e}")
    except KeyError:
        raise # Re-raise specific error
    except ValueError:
        raise # Re-raise specific error
    except csv.Error as e:
        raise csv.Error(f"CSV processing error: {e}")
    except Exception as e:
        # Catch any other unexpected errors and provide a generic message
        raise RuntimeError(f"An unexpected error occurred during CSV filtering: {e}")

    return written_rows_count
