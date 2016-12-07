from figaro import Figaro

def test_figaro_greets():
    expected = "Call me Figaro."
    assert Figaro().greet() == expected
