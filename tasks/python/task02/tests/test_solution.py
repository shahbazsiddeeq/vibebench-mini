from src.solution import reverse_words
def test_reverse_simple(): assert reverse_words("hello world")=="world hello"
def test_reverse_trim(): assert reverse_words(" a b c ")=="c b a"
def test_reverse_single(): assert reverse_words("hello")=="hello"
