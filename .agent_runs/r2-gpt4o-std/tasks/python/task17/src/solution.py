import re

def natural_sort(items):
    def natural_key(s):
        # Split the string into a list of strings and numbers
        parts = re.split(r'(\d+)', s)
        # Convert numeric parts to integers, leave other parts as strings
        return [int(part) if part.isdigit() else part for part in parts]

    # Sort using the natural key
    return sorted(items, key=natural_key)

# Example usage:
# print(natural_sort(["file10", "file2", "file1"]))  # Output: ["file1", "file2", "file10"]
# print(natural_sort(["A2", "a11", "a1b", "a1a"]))  # Output: ["A2", "a1a", "a1b", "a11"]
