import re


def clean_text(text: str) -> str:
    """Lowercase and strip extra spaces from user input."""
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    # Replace multiple spaces with single
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text: str, keywords) -> bool:
    """Return True if any keyword appears in text."""
    return any(k in text for k in keywords)
