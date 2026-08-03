import re
from collections import defaultdict

def word_freq(text):
    """
    Returns a dict mapping each lowercase word to the number of times it occurs.
    A word is a maximal run of Unicode letters and digits.
    Every other character (whitespace, punctuation, apostrophes, hyphens, underscores) is a separator.
    """
    if not text:
        return {}
    
    # Use regex to find all maximal runs of Unicode letters and digits
    # \w in Python regex with re.UNICODE matches Unicode letters, digits, and underscore
    # But we need to exclude underscore as it's a separator, so we use a custom pattern
    # Pattern: one or more Unicode letters or digits
    words = re.findall(r'[\w]+', text, re.UNICODE)
    
    # Filter out words that contain only underscores (edge case)
    # and convert to lowercase
    word_list = [word.lower() for word in words if re.search(r'[^\W_]|\d', word, re.UNICODE)]
    
    # Count frequencies
    freq = defaultdict(int)
    for word in word_list:
        freq[word] += 1
    
    return dict(freq)
