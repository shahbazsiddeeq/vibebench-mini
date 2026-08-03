import re
from typing import Dict, Union


def text_stats(text: str) -> Dict[str, Union[int, float]]:
    words = text.split()
    sentences = [segment for segment in re.split(r"[.!?]+", text) if segment.strip()]

    avg_word_length = (
        round(sum(len(word) for word in words) / len(words), 2)
        if words
        else 0.0
    )

    return {
        "char_count": len(text),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_word_length": avg_word_length,
    }
