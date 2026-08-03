def normalize_case(text: str) -> str:
    # Lowercase the entire text first
    text = text.lower()
    
    # Initialize variables
    result = []
    capitalize_next = True
    
    # Iterate over each character in the text
    for char in text:
        if capitalize_next and char.isalpha():
            # Capitalize the first alphabetic character after a sentence boundary
            result.append(char.upper())
            capitalize_next = False
        else:
            result.append(char)
        
        # Check if the current character is a sentence boundary
        if char in '.!?':
            capitalize_next = True
    
    return ''.join(result)
