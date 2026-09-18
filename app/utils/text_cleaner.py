import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Normalize text for fraud detection and matching.

    Keeps digits because they often carry signal in scam and fraud messages,
    while removing punctuation, normalizing whitespace, and lowering case.
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    text = unicodedata.normalize("NFKC", text)
    text = text.lower().strip()

    text = text.replace("&amp;", " and ")
    text = re.sub(r"[_]+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text
