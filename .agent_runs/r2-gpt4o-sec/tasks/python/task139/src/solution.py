# src/solution.py

from typing import Dict, List

def expand_cases(base: Dict, overrides: List[Dict]) -> List[Dict]:
    if not isinstance(base, dict) or not isinstance(overrides, list):
        raise ValueError("Invalid input types: base must be a dict and overrides must be a list of dicts.")
    
    result = []
    for override in overrides:
        if not isinstance(override, dict):
            raise ValueError("Each override must be a dictionary.")
        
        merged = base.copy()
        merged.update(override)
        result.append(merged)
    
    return result
