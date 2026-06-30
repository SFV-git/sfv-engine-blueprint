"""A small collection of standalone mathematical and utility functions."""

from math import isqrt
from typing import TypeVar


T = TypeVar("T")


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number, using F(0) = 0 and F(1) = 1."""
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

    return all(number % divisor for divisor in range(3, isqrt(number) + 1, 2))


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


def remove_duplicates(items: list[T]) -> list[T]:
    """Return items in their original order with duplicate values removed."""
    if not isinstance(items, list):
        raise TypeError("items must be a list")

    unique: list[T] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique


def main() -> None:
    """Run a brief demonstration when this file is executed directly."""
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"is_prime(29): {is_prime(29)}")
    print(f"reverse_string('blueprint'): {reverse_string('blueprint')}")
    print(f"greatest_common_divisor(84, 30): {greatest_common_divisor(84, 30)}")
    print(f"remove_duplicates([1, 2, 1, 3, 2]): {remove_duplicates([1, 2, 1, 3, 2])}")


if __name__ == "__main__":
    main()
