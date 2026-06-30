"""A small collection of mathematical and string utility functions."""


def fibonacci(n: int) -> list[int]:
    """Return the first *n* Fibonacci numbers."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    sequence: list[int] = []
    first, second = 0, 1
    for _ in range(n):
        sequence.append(first)
        first, second = second, first + second
    return sequence


def is_prime(number: int) -> bool:
    """Return whether *number* is a prime integer."""
    if not isinstance(number, int):
        raise TypeError("number must be an integer")
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


def reverse_string(text: str) -> str:
    """Return *text* with its characters in reverse order."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text[::-1]


def greatest_common_divisor(a: int, b: int) -> int:
    """Return the non-negative greatest common divisor of two integers."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a and b must be integers")

    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def main() -> None:
    """Demonstrate the four utilities when this file is run directly."""
    print(f"First 10 Fibonacci numbers: {fibonacci(10)}")
    print(f"Is 29 prime? {is_prime(29)}")
    print(f"Reverse of 'Blueprint': {reverse_string('Blueprint')}")
    print(f"GCD of 84 and 30: {greatest_common_divisor(84, 30)}")


if __name__ == "__main__":
    main()
