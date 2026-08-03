import re
from collections import defaultdict

def word_freq(text):
    # Use a regular expression to find all words consisting of Unicode letters and digits
    words = re.findall(r'\w+', text, re.UNICODE)
    
    # Convert all words to lowercase
    words = [word.lower() for word in words]
    
    # Count the frequency of each word
    frequency = defaultdict(int)
    for word in words:
        frequency[word] += 1
    
    return dict(frequency)
