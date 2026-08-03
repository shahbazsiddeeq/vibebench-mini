def luhn_valid(number: str) -> bool:
    if not isinstance(number, str):
        raise TypeError("Input must be a string.")
    if not number.isdigit() or len(number) == 0:
        raise ValueError("Input must be a non-empty string of digits.")

    total = 0
    num_digits = len(number)
    odd_even = num_digits & 1

    for i in range(num_digits):
        digit = int(number[i])

        if (i & 1) ^ odd_even:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0

def luhn_check_digit(payload: str) -> int:
    if not isinstance(payload, str):
        raise TypeError("Input must be a string.")
    if not payload.isdigit() or len(payload) == 0:
        raise ValueError("Input must be a non-empty string of digits.")

    total = 0
    num_digits = len(payload)
    odd_even = (num_digits + 1) & 1

    for i in range(num_digits):
        digit = int(payload[i])

        if (i & 1) ^ odd_even:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit

    check_digit = (10 - (total % 10)) % 10
    return check_digit
