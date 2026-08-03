# src/solution.py

def normalize_case(text: str) -> str:
    if not text:
        return text

    # Lowercase the entire text
    text = text.lower()
    
    # Initialize a list to hold the characters of the result
    result = []
    capitalize_next = True

    for char in text:
        if capitalize_next and char.isalpha():
            result.append(char.upper())
            capitalize_next = False
        else:
            result.append(char)

        # Check if the current character is a sentence-ending punctuation
        if char in '.!?':
            capitalize_next = True

    return ''.join(result)
