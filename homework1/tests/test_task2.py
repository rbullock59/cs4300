from src.task2 import get_integer, get_float, get_string, get_boolean


def test_integer():
    assert isinstance(get_integer(), int)
    assert get_integer() == 42


def test_float():
    assert isinstance(get_float(), float)
    assert get_float() == 3.14


def test_string():
    assert isinstance(get_string(), str)
    assert get_string() == "hello"


def test_boolean():
    assert isinstance(get_boolean(), bool)
    assert get_boolean() is True
