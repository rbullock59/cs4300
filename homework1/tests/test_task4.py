import pytest

from src.task4 import calculate_discount


@pytest.mark.parametrize(
    "price,discount,expected",
    [
        (100, 10, 90.0),
        (100.0, 10.0, 90.0),
        (50, 0, 50.0),
        (50, 100, 0.0),
    ],
)
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == pytest.approx(expected)


def test_rejects_non_numeric_price():
    with pytest.raises(TypeError):
        calculate_discount("100", 10)


def test_rejects_non_numeric_discount():
    with pytest.raises(TypeError):
        calculate_discount(100, "10")


def test_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_discount(-10, 10)


def test_rejects_out_of_range_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, 150)
