import secrets

def _validate_input(number_str: str, allow_empty: bool = False):
    """
    Internal helper to validate the input string for Luhn functions.
    Raises TypeError if not a string.
    Raises ValueError if empty (unless allow_empty is True) or contains non-digit characters.
    """
    if not isinstance(number_str, str):
        raise TypeError("Input must be a string.")
    if not allow_empty and not number_str:
        raise ValueError("Input string cannot be empty.")
    if not number_str.isdigit():
        raise ValueError("Input string must contain only digits ('0'-'9').")

def _luhn_checksum_calculate(number_str: str) -> int:
    """
    Internal helper to calculate the Luhn checksum sum.
    Assumes number_str is already validated to be a non-empty digit string.
    """
    total_sum = 0
    # Iterate from right to left
    for i, char_digit in enumerate(reversed(number_str)):
        digit = int(char_digit)
        if (i + 1) % 2 == 0:  # Every second digit from the right (positions 2, 4, ...)
            doubled_digit = digit * 2
            if doubled_digit > 9:
                doubled_digit -= 9
            total_sum += doubled_digit
        else:
            total_sum += digit
    return total_sum

def luhn_valid(number: str) -> bool:
    """
    Checks if a digit string satisfies the Luhn checksum.
    The input 'number' INCLUDES its trailing check digit.

    Args:
        number: The digit string to validate.

    Returns:
        True if the number is Luhn-valid, False otherwise.

    Raises:
        TypeError: If the argument is not a str.
        ValueError: If it is empty or contains any non-digit character.
    """
    _validate_input(number)
    checksum_sum = _luhn_checksum_calculate(number)
    return checksum_sum % 10 == 0

def luhn_check_digit(payload: str) -> int:
    """
    Calculates the single check digit that, when appended to the right of 'payload',
    makes the full string Luhn-valid.

    Args:
        payload: The digit string for which to calculate the check digit.

    Returns:
        The single check digit (an int 0-9).

    Raises:
        TypeError: If the argument is not a str.
        ValueError: If it is empty or contains any non-digit character.
    """
    _validate_input(payload)

    # To find the check digit 'x', we need (checksum_sum_of_payload + x) % 10 == 0.
    # The check digit 'x' is treated as the rightmost digit (position 1),
    # so the digits of the payload will be processed as if 'x' is present.
    # This means the rightmost digit of the payload will be at position 2 (doubled).

    # Calculate the sum for the payload as if it were followed by a '0' (the check digit).
    # This means the rightmost digit of the payload will be at position 2 (doubled).
    # We can achieve this by calculating the checksum for `payload + "0"` and then
    # adjusting for the '0' being at position 1 (not doubled).
    # Or, more directly, calculate the sum for the payload, but treat its rightmost
    # digit as if it's at position 2 (doubled), its second rightmost at position 3 (not doubled), etc.

    # Let's use a slightly modified _luhn_checksum_calculate logic for the payload
    # to find the remainder needed.
    # We want (sum_of_payload_digits_processed_as_if_check_digit_is_present + check_digit) % 10 == 0
    # The check_digit itself is at position 1 (not doubled).
    # The rightmost digit of the payload is at position 2 (doubled).

    total_sum_for_payload_prefix = 0
    # Iterate from right to left over the payload, treating its rightmost digit
    # as if it's the second-to-last digit of the full number (i.e., at an even position from the right).
    for i, char_digit in enumerate(reversed(payload)):
        digit = int(char_digit)
        # If 'i' is 0, it's the rightmost digit of payload, which is at position 2 in the full number.
        # If 'i' is 1, it's the second rightmost of payload, which is at position 3 in the full number.
        # So, if (i+1) is even, it's an odd position in the full number (not doubled).
        # If (i+1) is odd, it's an even position in the full number (doubled).
        # This is equivalent to: if i is odd, it's not doubled. If i is even, it's doubled.
        if (i + 1) % 2 != 0:  # This digit is at an even position from the right in the full number
            doubled_digit = digit * 2
            if doubled_digit > 9:
                doubled_digit -= 9
            total_sum_for_payload_prefix += doubled_digit
        else:  # This digit is at an odd position from the right in the full number
            total_sum_for_payload_prefix += digit

    # Now we need to find a check_digit (0-9) such that
    # (total_sum_for_payload_prefix + check_digit) % 10 == 0
    remainder = total_sum_for_payload_prefix % 10
    if remainder == 0:
        return 0
    else:
        return 10 - remainder
