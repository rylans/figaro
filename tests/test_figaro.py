from figaro import Figaro

def test_response_from_default_handler():
    expected = "I'm not sure how to respond to that."
    assert Figaro().hears("abcd") == expected

def test_response_form_greeting_handler():
    expected = "Hey there."
    assert Figaro().hears("hey") == expected
