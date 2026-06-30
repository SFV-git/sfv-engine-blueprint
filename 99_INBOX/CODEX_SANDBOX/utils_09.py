"""A small collection of dependency-free mathematical and utility functions."""

from __future__ import annotations

from collections.abc import Iterable
from math import isqrt
from typing import TypeVar


T = TypeVar("T")


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number, where fibonacci(0) is 0."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def is_prime(number: int) -> bool:
    """Return whether number is prime."""
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError("number must be an integer")
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    return all(number % divisor for divisor in range(3, isqrt(number) + 1, 2))


def reverse_string(text: str) -> str:
    """Return text with its characters in reverse order."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text[::-1]


def factorial(n: int) -> int:
    """Return n factorial."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


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


def is_palindrome(value: object) -> bool:
    """Check whether value reads the same backward, ignoring case and symbols."""
    normalized = "".join(character.casefold() for character in str(value) if character.isalnum())
    return normalized == normalized[::-1]


def flatten(nested: Iterable[Iterable[T]]) -> list[T]:
    """Flatten one level of nested iterables into a list."""
    return [item for group in nested for item in group]


def remove_duplicates(values: Iterable[T]) -> list[T]:
    """Return unique values in their original order, including unhashable values."""
    unique: list[T] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return unique


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    if not isinstance(celsius, (int, float)) or isinstance(celsius, bool):
        raise TypeError("celsius must be a number")
    return (celsius * 9 / 5) + 32


def main() -> None:
    """Run a concise demonstration when this module is executed directly."""
    demonstrations = {
        "fibonacci(10)": fibonacci(10),
        "is_prime(29)": is_prime(29),
        "reverse_string('Python')": reverse_string("Python"),
        "factorial(6)": factorial(6),
        "greatest_common_divisor(84, 30)": greatest_common_divisor(84, 30),
        "is_palindrome('Never odd or even')": is_palindrome("Never odd or even"),
        "flatten([[1, 2], [3, 4]])": flatten([[1, 2], [3, 4]]),
        "remove_duplicates([1, 2, 1, 3])": remove_duplicates([1, 2, 1, 3]),
        "celsius_to_fahrenheit(20)": celsius_to_fahrenheit(20),
    }
    for description, result in demonstrations.items():
        print(f"{description} -> {result}")


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[SOURCE_OF_TRUTH_RULES|Source of Truth Rules]]
# - [[USAGE_OPTIMIZATION|Usage Optimization]]
# - [[MASTER_CONTEXT|Master Context]]
