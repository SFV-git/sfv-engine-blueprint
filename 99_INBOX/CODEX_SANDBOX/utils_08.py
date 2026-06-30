"""A small collection of mathematical and general-purpose utility functions."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from math import isqrt
from typing import TypeVar


T = TypeVar("T")


def fibonacci(n: int) -> list[int]:
    """Return the first *n* Fibonacci numbers."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    numbers: list[int] = []
    first, second = 0, 1
    for _ in range(n):
        numbers.append(first)
        first, second = second, first + second
    return numbers


def is_prime(number: int) -> bool:
    """Return whether *number* is a prime integer."""
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError("number must be an integer")
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    return all(number % divisor != 0 for divisor in range(3, isqrt(number) + 1, 2))


def reverse_string(text: str) -> str:
    """Return *text* with its characters in reverse order."""
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


def factorial(n: int) -> int:
    """Return n!, where *n* is a non-negative integer."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    result = 1
    for factor in range(2, n + 1):
        result *= factor
    return result


def is_palindrome(value: object) -> bool:
    """Return whether *value* reads the same forwards and backwards.

    Comparison ignores case and non-alphanumeric characters.
    """
    normalized = "".join(character.casefold() for character in str(value) if character.isalnum())
    return normalized == normalized[::-1]


def flatten(nested_items: Iterable[Iterable[T]]) -> list[T]:
    """Flatten an iterable containing one level of nested iterables."""
    return [item for group in nested_items for item in group]


def binary_search(items: Sequence[T], target: T) -> int:
    """Return the index of *target* in sorted *items*, or -1 when absent."""
    low, high = 0, len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def main() -> None:
    """Run a brief demonstration when this file is executed directly."""
    print("Fibonacci:", fibonacci(10))
    print("29 is prime:", is_prime(29))
    print("Reversed:", reverse_string("utility"))
    print("GCD of 84 and 30:", greatest_common_divisor(84, 30))
    print("6!:", factorial(6))
    print("Palindrome:", is_palindrome("A man, a plan, a canal: Panama!"))
    print("Flattened:", flatten([[1, 2], [3], [4, 5]]))
    print("Index of 7:", binary_search([1, 3, 5, 7, 9], 7))


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[UTILITY_FUNCTIONS|Utility Functions]]
# - [[MATH_UTILITIES|Math Utilities]]
# - [[STRING_MANIPULATION|String Manipulation]]
# - [[ALGORITHMS|Algorithms]]
# - [[DATA_STRUCTURES|Data Structures]]
# - [[CODE_QUALITY|Code Quality]]
