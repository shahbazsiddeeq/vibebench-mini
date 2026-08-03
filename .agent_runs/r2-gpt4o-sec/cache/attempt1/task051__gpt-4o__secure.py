import re

def normalize_case(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Lowercase the entire text
    text = text.lower()
    
    # Function to capitalize the first alphabetic character in a sentence
    def capitalize_first_letter(match):
        sentence = match.group(0)
        # Find the first alphabetic character and capitalize it
        for i, char in enumerate(sentence):
            if char.isalpha():
                return sentence[:i] + char.upper() + sentence[i+1:]
        return sentence
    
    # Use regex to find sentence boundaries and apply capitalization
    result = re.sub(r'(?:^|(?<=[.!?]))[^.!?]*', capitalize_first_letter, text)
    
    return result
