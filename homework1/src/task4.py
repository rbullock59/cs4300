"""Task 4: functions and duck typing."""

from numbers import Number


def calculate_discount(price, discount):
    """Return price after applying discount percent.

    Duck typing: accepts anything numeric-like (int, float, Decimal, ...)
    rather than checking for a specific type.
    """
    if not isinstance(price, Number) or isinstance(price, bool):
        raise TypeError("price must be numeric")
    if not isinstance(discount, Number) or isinstance(discount, bool):
        raise TypeError("discount must be numeric")
    if price < 0:
        raise ValueError("price must be non-negative")
    if not 0 <= discount <= 100:
        raise ValueError("discount must be between 0 and 100")
    return price * (1 - discount / 100)
