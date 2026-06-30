"""A small mathematical utility module."""


def is_prime(number: int) -> bool:
    """Return True when number is prime, otherwise return False."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2

    return True


if __name__ == "__main__":
    samples = (2, 17, 18, 97)
    for sample in samples:
        print(f"{sample} is prime: {is_prime(sample)}")
