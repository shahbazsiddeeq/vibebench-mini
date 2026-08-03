# src/solution.py

def caesar(text, shift):
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    if not isinstance(shift, int):
        raise ValueError("Shift must be an integer.")
    
    def shift_char(c, shift):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            return chr((ord(c) - base + shift) % 26 + base)
        return c

    return ''.join(shift_char(c, shift) for c in text)
