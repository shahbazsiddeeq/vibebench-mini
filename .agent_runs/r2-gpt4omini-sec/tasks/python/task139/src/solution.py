# src/solution.py

def expand_cases(base, overrides):
    if not isinstance(base, dict):
        raise ValueError("Base must be a dictionary.")
    if not isinstance(overrides, list):
        raise ValueError("Overrides must be a list.")

    results = []
    for override in overrides:
        if not isinstance(override, dict):
            raise ValueError("Each override must be a dictionary.")
        # Create a new dictionary that merges base and the current override
        merged = base.copy()  # Shallow copy of the base
        merged.update(override)  # Update with the override
        results.append(merged)  # Add the merged dict to results

    return results
