from src.solution import text_stats


def test_basic():
    result = text_stats("Hello world.")
    assert result["word_count"] == 2
    assert result["sentence_count"] == 1
    assert result["char_count"] == 12


def test_multiple_sentences():
    result = text_stats("Hello. How are you? I am fine!")
    assert result["sentence_count"] == 3


def test_avg_word_length_keeps_punctuation():
    # "Hello" (5) + "world." (6) -> 11 / 2 == 5.5, matching the example.
    result = text_stats("Hello world.")
    assert result["avg_word_length"] == 5.5


def test_word_count():
    result = text_stats("one two three four five")
    assert result["word_count"] == 5
