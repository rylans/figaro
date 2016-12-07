from figaro import Figaro

def test_response_from_default_handler():
    expected = "I'm not sure how to respond to that."
    assert Figaro().hears("abcd") == expected

def test_response_from_greeting_handler():
    expected = "Hey there."
    assert Figaro().hears("hey") == expected

def test_response_from_math_handler():
    expected = "-32.0"
    assert Figaro().hears("Calculate 1 minus 33") == expected

def test_response_from_math_handler_unary():
    expected = "4.0"
    assert Figaro().hears("whats root 16") == expected
