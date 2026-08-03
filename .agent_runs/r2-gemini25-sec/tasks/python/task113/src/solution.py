def from_roman(s: str) -> int:
    """
    Converts a Roman numeral string to an integer.

    Raises ValueError for empty input or invalid characters.
    Example: from_roman("XIV") -> 14, from_roman("IV") -> 4
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    if not s:
        raise ValueError("Input cannot be empty.")

    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    # Iterate through the Roman numeral string from right to left
    for char in reversed(s):
        if char not in roman_map:
            raise ValueError(f"Invalid Roman numeral character: '{char}'")

        current_value = roman_map[char]

        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value

    # Basic validation for common invalid sequences (e.g., IIII, VV)
    # This is not exhaustive for all invalid Roman numerals but catches common errors.
    # A more robust validation would involve checking for adherence to Roman numeral rules
    # like no more than three identical consecutive symbols (except for M),
    # and specific subtraction rules (e.g., only I, X, C can be subtracted).
    # For this problem, we'll focus on the conversion logic and basic character validation.

    # Re-convert the calculated integer back to Roman and compare to ensure validity
    # This is a common security-conscious approach to validate input that has been parsed.
    # If the input Roman numeral is not valid (e.g., "IIII"), the conversion will yield 4,
    # but _to_roman(4) is "IV", not "IIII". This check will catch such cases.
    # We need a helper function _to_roman for this, which is provided in the test.
    # For a self-contained module, we'll include a minimal version of _to_roman.

    # Minimal _to_roman for validation purposes
    def _to_roman_for_validation(n: int) -> str:
        if not isinstance(n, int) or not (1 <= n <= 3999):
            # Limit to standard Roman numeral range for validation
            return "" # Indicate invalid range for this check

        table = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
        ]
        out = []
        temp_n = n
        for value, sym in table:
            while temp_n >= value:
                out.append(sym)
                temp_n -= value
        return "".join(out)

    # Validate the input Roman numeral by converting back and comparing
    if total > 0 and _to_roman_for_validation(total) != s:
        # This catches cases like "IIII" (converts to 4, but _to_roman(4) is "IV")
        # or "VV" (converts to 10, but _to_roman(10) is "X")
        # or "IC" (converts to 99, but _to_roman(99) is "XCIX")
        raise ValueError(f"Invalid Roman numeral format: '{s}'")

    return total
