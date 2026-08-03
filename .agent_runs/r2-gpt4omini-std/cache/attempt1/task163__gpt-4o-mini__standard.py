# src/solution.py

def base32_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input must be bytes or bytearray.")
    
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    output = []
    padding = 0

    # Process input in chunks of 5 bytes (40 bits)
    for i in range(0, len(data), 5):
        chunk = data[i:i + 5]
        byte_len = len(chunk)
        if byte_len < 5:
            padding = 5 - byte_len
        
        # Convert to 40 bits
        bits = 0
        for byte in chunk:
            bits = (bits << 8) | byte
        
        # Extract 8 base32 characters
        for j in range(8):
            if j < (byte_len * 8 + 4) // 5:
                output.append(base32_alphabet[(bits >> (35 - j * 5)) & 0x1F])
            else:
                output.append('=')

    return ''.join(output)

def base32_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    
    s = s.strip().upper()
    
    # Validate length
    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8.")
    
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    base32_index = {char: index for index, char in enumerate(base32_alphabet)}
    
    # Validate padding
    padding_count = s.count('=')
    if padding_count not in {0, 1, 3, 4, 6}:
        raise ValueError("Invalid number of padding characters.")
    
    if '=' in s[:-padding_count]:
        raise ValueError("Padding characters must be at the end.")
    
    output = bytearray()
    
    # Process input in chunks of 8 characters
    for i in range(0, len(s), 8):
        chunk = s[i:i + 8]
        bits = 0
        
        for char in chunk:
            if char == '=':
                continue
            if char not in base32_index:
                raise ValueError("Invalid character found.")
            bits = (bits << 5) | base32_index[char]
        
        # Extract bytes from bits
        for j in range(5):
            if j < (len(chunk) * 5) // 8:
                output.append((bits >> (32 - j * 8)) & 0xFF)

    return bytes(output)
