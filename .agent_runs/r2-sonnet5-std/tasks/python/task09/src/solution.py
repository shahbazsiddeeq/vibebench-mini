import re
from collections import Counter


def top_k_words(text, k):
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    counts = Counter(words)
    sorted_words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words[:k]
