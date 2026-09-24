import pytest

from src.task3 import check_sign, first_n_primes, sum_1_to_100


@pytest.mark.parametrize("n,expected", [(5, "positive"), (-3, "negative"), (0, "zero")])
def test_check_sign(n, expected):
    assert check_sign(n) == expected


def test_first_n_primes():
    assert first_n_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_sum_1_to_100():
    assert sum_1_to_100() == 5050
