from figaro import Figaro

def test_default_handler():
    expected = "I'm not sure how to respond to that."
    assert Figaro().hears("abcd") == expected

def test_greeting_handler():
    expected = "Hey there."
    assert Figaro().hears("hey") == expected

def test_math_handler_minus():
    expected = "-32.0"
    assert Figaro().hears("Calculate 1 minus 33") == expected

def test_math_handler_sqrt():
    expected = "4.0"
    assert Figaro().hears("whats root 16") == expected

def test_math_handler_cos():
    expected = "1.0"
    assert Figaro().hears("what is cos 0") == expected

def test_math_hander_ln():
    from math import e
    expected = "2.0"
    assert Figaro().hears("what is ln " + str(e*e)) == expected

