import re
from collections import defaultdict

def word_freq(text):
    # Use regex to find all words (unicode letters and digits)
    words = re.findall(r'\w+', text.lower())
    # Create a dictionary to count occurrences
    frequency = defaultdict(int)
    
    for word in words:
        frequency[word] += 1
    
    return dict(frequency)
