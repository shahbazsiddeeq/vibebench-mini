import unicodedata
import re

def slugify(s: str) -> str:
    # Normalize and strip accents
    normalized = unicodedata.normalize('NFKD', s)
    ascii_str = normalized.encode('ascii', 'ignore').decode('ascii')
    
    # Lowercase the string
    ascii_str = ascii_str.lower()
    
    # Replace runs of non-alphanumeric characters with a single hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_str)
    
    # Trim leading and trailing hyphens
    slug = slug.strip('-')
    
    return slug

# Unit tests
def test_punct_and_trim():
    assert slugify("  Hello,  world --- ") == "hello-world"

def test_underscores():
    assert slugify("hello_world_2025") == "hello-world-2025"

def test_non_latin_dropped():
    assert slugify("日本語") == ""
    assert slugify("日本語 test 123") == "test-123"
