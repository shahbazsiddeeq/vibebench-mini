import json


def sum_jsonl(path, key):
    """
    Sums numeric values for 'key' over JSON Lines in a file.

    Non-numeric or missing values for the specified key are ignored.
    If no numeric values are found for the key, a ValueError is raised.

    Args:
        path (str): The path to the JSON Lines file.
        key (str): The key whose values are to be summed.

    Returns:
        float: The sum of the numeric values for the specified key.

    Raises:
        ValueError: If no numeric values are found for the key in the file.
    """
    total_sum = 0.0
    found_numeric_value = False

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if key in data:
                    value = data[key]
                    if isinstance(value, (int, float)):
                        total_sum += float(value)
                        found_numeric_value = True
            except json.JSONDecodeError:
                # Ignore lines that are not valid JSON
                continue
            except TypeError:
                # Ignore if value is not a number (e.g., None, string that can't be converted)
                continue

    if not found_numeric_value:
        raise ValueError(f"No numeric values found for key '{key}' in the file.")

    return total_sum
