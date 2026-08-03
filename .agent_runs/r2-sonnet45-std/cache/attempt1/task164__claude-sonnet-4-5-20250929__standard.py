def vigenere_encrypt(plaintext: str, key: str) -> str:
    # Validation: TypeError checks first
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Validation: ValueError checks
    if not key:
        raise ValueError("key cannot be empty")
    if not all(c.isalpha() and ord(c) < 128 for c in key):
        raise ValueError("key must contain only ASCII letters")
    
    # Convert key to lowercase and get shifts
    key_lower = key.lower()
    key_shifts = [ord(c) - ord('a') for c in key_lower]
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha() and ord(char) < 128:
            # Get the shift for this position
            shift = key_shifts[key_index % len(key_shifts)]
            
            if char.isupper():
                # Uppercase letter
                encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Lowercase letter
                encrypted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            
            result.append(encrypted)
            key_index += 1
        else:
            # Non-letter: pass through unchanged, don't advance key
            result.append(char)
    
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    # Validation: TypeError checks first
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Validation: ValueError checks
    if not key:
        raise ValueError("key cannot be empty")
    if not all(c.isalpha() and ord(c) < 128 for c in key):
        raise ValueError("key must contain only ASCII letters")
    
    # Convert key to lowercase and get shifts
    key_lower = key.lower()
    key_shifts = [ord(c) - ord('a') for c in key_lower]
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha() and ord(char) < 128:
            # Get the shift for this position
            shift = key_shifts[key_index % len(key_shifts)]
            
            if char.isupper():
                # Uppercase letter
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                # Lowercase letter
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            result.append(decrypted)
            key_index += 1
        else:
            # Non-letter: pass through unchanged, don't advance key
            result.append(char)
    
    return ''.join(result)
