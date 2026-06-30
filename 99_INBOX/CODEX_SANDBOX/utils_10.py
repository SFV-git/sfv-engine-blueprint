"""A small collection of mathematical and general-purpose utility functions."""

from collections.abc import Iterable
from math import gcd
from typing import TypeVar

T = TypeVar("T")


def fibonacci(n: int) -> list[int]:
    """Return the first *n* Fibonacci numbers."""
    if n < 0:
        raise ValueError("n must be non-negative")

    sequence: list[int] = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence


def is_prime(number: int) -> bool:
    """Return whether *number* is prime."""
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
    return text[::-1]


def factorial(n: int) -> int:
    """Return n factorial."""
    if n < 0:
        raise ValueError("n must be non-negative")

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


def greatest_common_divisor(a: int, b: int) -> int:
    """Return the greatest common divisor of two integers."""
    return gcd(a, b)


def least_common_multiple(a: int, b: int) -> int:
    """Return the non-negative least common multiple of two integers."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def is_palindrome(value: object) -> bool:
    """Return whether the string form of *value* is a palindrome."""
    text = str(value)
    return text == text[::-1]


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + 32


def flatten(nested: Iterable[Iterable[T]]) -> list[T]:
    """Flatten an iterable containing one level of nested iterables."""
    return [item for group in nested for item in group]


def remove_duplicates(items: Iterable[T]) -> list[T]:
    """Remove duplicates while preserving input order."""
    result: list[T] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def main() -> None:
    """Run a concise demonstration of all ten utilities."""
    print("Fibonacci:", fibonacci(10))
    print("29 is prime:", is_prime(29))
    print("Reversed string:", reverse_string("blueprint"))
    print("6!:", factorial(6))
    print("GCD of 48 and 18:", greatest_common_divisor(48, 18))
    print("LCM of 12 and 18:", least_common_multiple(12, 18))
    print("'level' is a palindrome:", is_palindrome("level"))
    print("20 C in Fahrenheit:", celsius_to_fahrenheit(20))
    print("Flattened:", flatten([[1, 2], [3], [4, 5]]))
    print("Unique values:", remove_duplicates([1, 2, 1, 3, 2]))


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[MATH_UTILITIES|Mathematical Utilities]]
# - [[STRING_UTILS|String Manipulation Utilities]]
# - [[GENERAL_UTILS|General-Purpose Utilities]]
