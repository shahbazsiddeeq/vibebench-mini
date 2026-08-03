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
        if byte_len == 0:
            break
        
        # Convert to integer
        num = int.from_bytes(chunk, 'big')
        
        # Calculate the number of bits to encode
        bits = byte_len * 8
        for j in range(0, 8):
            if bits >= 5 * (j + 1):
                output.append(base32_alphabet[(num >> (35 - 5 * j)) & 0x1F])
            else:
                output.append('=')
                padding += 1

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
    if padding_count not in {0, 1, 3, 4, 6} or s.endswith('=') and any(c != '=' for c in s[s.index('='):]):
        raise ValueError("Invalid padding.")
    
    output = bytearray()
    
    # Decode the input
    for i in range(0, len(s), 8):
        chunk = s[i:i + 8]
        num = 0
        bits = 0
        
        for char in chunk:
            if char == '=':
                continue
            if char not in base32_index:
                raise ValueError("Invalid character found.")
            num = (num << 5) | base32_index[char]
            bits += 5
        
        # Convert to bytes
        for j in range(bits // 8):
            output.append((num >> (32 - 8 * (j + 1))) & 0xFF)
    
    return bytes(output)
