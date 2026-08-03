def _validate_input(number_str: str):
    if not isinstance(number_str, str):
        raise TypeError("Input must be a string.")
    if not number_str:
        raise ValueError("Input string cannot be empty.")
    if not number_str.isdigit():
        raise ValueError("Input string must contain only digits.")

def _luhn_checksum(number_str: str) -> int:
    """
    Calculates the Luhn checksum for a given digit string.
    This is a helper function and does not perform input validation.
    """
    total = 0
    # Iterate from right to left
    for i, digit_char in enumerate(reversed(number_str)):
        digit = int(digit_char)
        if (i + 1) % 2 == 0:  # Every second digit from the right (positions 2, 4, ...)
            doubled_digit = digit * 2
            if doubled_digit > 9:
                doubled_digit -= 9
            total += doubled_digit
        else:
            total += digit
    return total

def luhn_valid(number: str) -> bool:
    """
    Checks if a digit string satisfies the Luhn checksum.

    Args:
        number: The digit string to validate, including its trailing check digit.

    Returns:
        True if the number is Luhn-valid, False otherwise.

    Raises:
        TypeError: If the argument is not a str.
        ValueError: If it is empty or contains any non-digit character.
    """
    _validate_input(number)
    return _luhn_checksum(number) % 10 == 0

def luhn_check_digit(payload: str) -> int:
    """
    Calculates the single check digit that, when appended to the right of `payload`,
    makes the full string Luhn-valid.

    Args:
        payload: The digit string for which to calculate the check digit.

    Returns:
        The single check digit (an int 0..9).

    Raises:
        TypeError: If the argument is not a str.
        ValueError: If it is empty or contains any non-digit character.
    """
    _validate_input(payload)

    # Calculate the checksum for the payload as if it were a full number
    # but treating the missing check digit as 0 for now.
    # The _luhn_checksum function already handles the doubling logic correctly
    # based on position from the right.
    # We need to find a digit `x` such that _luhn_checksum(payload + str(x)) % 10 == 0.

    # Let S be the sum of digits from the payload, where digits are processed
    # according to Luhn's algorithm, but without considering the check digit's
    # contribution yet.
    # The check digit will be at position 1 (rightmost).
    # So, it will NOT be doubled.

    # We can calculate the sum for the payload and then find the remainder needed.
    # The `_luhn_checksum` function assumes the last digit is part of the number.
    # If we append '0' to the payload, the `_luhn_checksum` will calculate
    # the sum for `payload + '0'`. The '0' will be at position 1 (rightmost)
    # and thus not doubled.
    # Let `current_sum = _luhn_checksum(payload + '0')`.
    # We want `(current_sum - 0 + x) % 10 == 0` where `x` is the check digit.
    # This simplifies to `(current_sum + x) % 10 == 0`.
    # So, `x = (10 - (current_sum % 10)) % 10`.

    # Calculate the sum for the payload string, treating it as if it were
    # the number *without* the check digit.
    # The check digit will be at position 1 (rightmost) when appended.
    # So, the digits of the payload will shift their positions.
    # If payload is "ABC", and check digit is "D", the full number is "ABCD".
    # D is pos 1, C is pos 2, B is pos 3, A is pos 4.
    # So C and A are doubled.

    # We can simulate appending a '0' and then adjust.
    # The `_luhn_checksum` function processes from right to left.
    # If we pass `payload + '0'`, the '0' will be at position 1 (not doubled).
    # The last digit of `payload` will be at position 2 (doubled).
    # The second to last digit of `payload` will be at position 3 (not doubled), etc.

    # Let's calculate the sum for `payload + '0'`
    sum_with_zero_check_digit = _luhn_checksum(payload + '0')

    # We need `(sum_with_zero_check_digit - 0 + check_digit) % 10 == 0`
    # This means `(sum_with_zero_check_digit + check_digit) % 10 == 0`
    # So, `check_digit = (10 - (sum_with_zero_check_digit % 10)) % 10`
    
    remainder = sum_with_zero_check_digit % 10
    if remainder == 0:
        return 0
    else:
        return 10 - remainder
