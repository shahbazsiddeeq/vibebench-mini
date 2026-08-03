# src/solution.py

def caesar(text, shift):
    def shift_char(c, shift):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            return chr((ord(c) - base + shift) % 26 + base)
        return c

    return ''.join(shift_char(c, shift) for c in text)
