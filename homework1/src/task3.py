"""Task 3: control structures."""


def check_sign(n):
    """Return 'positive', 'negative', or 'zero' for n."""
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"


def first_n_primes(n):
    """Return the first n prime numbers."""
    primes = []
    candidate = 2
    while len(primes) < n:
        if all(candidate % p != 0 for p in primes if p * p <= candidate):
            primes.append(candidate)
        candidate += 1
    return primes


def sum_1_to_100():
    """Return sum of integers 1..100 using a while loop."""
    total = 0
    i = 1
    while i <= 100:
        total += i
        i += 1
    return total


if __name__ == "__main__":
    print(check_sign(5))
    print(first_n_primes(10))
    print(sum_1_to_100())
