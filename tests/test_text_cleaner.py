from app.utils.text_cleaner import clean_text


def test_clean_text_keeps_numbers_and_removes_punctuation():
    text = "URGENT!!! Send 5000 now to verify payment."
    assert clean_text(text) == "urgent send 5000 now to verify payment"


def test_clean_text_collapses_whitespace():
    text = "  hello    world  "
    assert clean_text(text) == "hello world"
