import unicodedata

def remove_special_chars(text: str) -> str:
    """Remove characters with Unicode categories So, Cn, Co from a string."""
    return ''.join(
        char for char in text 
        if unicodedata.category(char) not in {'So', 'Cn', 'Co'}
    )