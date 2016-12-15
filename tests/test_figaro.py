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

def test_math_handler_divide_slash():
    expected = "1.5"
    assert Figaro().hears("whats 3 / 2") == expected

def test_math_handler_divide_by():
    expected = "1.5"
    assert Figaro().hears("what is 3 divided by 2") == expected

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

def test_simple_memory_in_out():
    fg = Figaro()
    fg.hears("she is one of us")
    assert fg.hears("Who is she?") == 'one of us'

def test_name_in_out():
    fg = Figaro()
    assert fg.hears("who am I?") == "I don't know. You tell me."
    assert fg.hears("My name is Dan") == "Nice to meet you."
    assert fg.hears("Who am I?") == "You told me your name is Dan."

def test_conv_termination():
    fg = Figaro()
    assert fg.conversation_ended == False
    assert fg.hears("Hello") == "Hello!"
    assert fg.conversation_ended == False
    assert fg.hears("Bye") == "See you later!"
    assert fg.conversation_ended == True
