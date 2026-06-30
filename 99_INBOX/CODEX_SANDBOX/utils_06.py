"""A small collection of mathematical and general-purpose utility functions."""

from collections.abc import Sequence
from math import isqrt
from typing import TypeVar


T = TypeVar("T")


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number, where fibonacci(0) is 0."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    current, following = 0, 1
    for _ in range(n):
        current, following = following, current + following
    return current


def is_prime(number: int) -> bool:
    """Return whether an integer is prime."""
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError("number must be an integer")
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    for divisor in range(3, isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False
    return True


def reverse_string(text: str) -> str:
    """Return a string with its characters in reverse order."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text[::-1]


def greatest_common_divisor(a: int, b: int) -> int:
    """Return the non-negative greatest common divisor of two integers."""
    if (
        not isinstance(a, int)
        or isinstance(a, bool)
        or not isinstance(b, int)
        or isinstance(b, bool)
    ):
        raise TypeError("a and b must be integers")

    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def flatten(nested_items: Sequence[Sequence[T]]) -> list[T]:
    """Flatten a sequence containing one level of nested sequences."""
    if not isinstance(nested_items, Sequence):
        raise TypeError("nested_items must be a sequence")

    result: list[T] = []
    for items in nested_items:
        if not isinstance(items, Sequence):
            raise TypeError("each nested item must be a sequence")
        result.extend(items)
    return result


def is_palindrome(text: str) -> bool:
    """Check for a palindrome while ignoring case and non-alphanumerics."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    normalized = "".join(character.casefold() for character in text if character.isalnum())
    return normalized == normalized[::-1]


def main() -> None:
    """Run a short demonstration when this file is executed directly."""
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"is_prime(97): {is_prime(97)}")
    print(f"reverse_string('Blueprint'): {reverse_string('Blueprint')}")
    print(f"greatest_common_divisor(84, 30): {greatest_common_divisor(84, 30)}")
    print(f"flatten([[1, 2], [3], [4, 5]]): {flatten([[1, 2], [3], [4, 5]])}")
    print(f"is_palindrome('Never odd or even'): {is_palindrome('Never odd or even')}")


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[UTILITY_SCRIPTS|Utility Scripts]]
# - [[MATH_OPERATIONS|Math Operations]]
# - [[STRING_MANIPULATION|String Manipulation]]
# - [[DATA_PROCESSING|Data Processing]]
# - [[TYPE_VALIDATION|Type Validation]]
