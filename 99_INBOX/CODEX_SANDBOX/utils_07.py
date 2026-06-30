"""Seven small, reusable mathematical and utility functions."""

from math import isqrt
from typing import Any, Iterable


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
    """Return whether number is a prime integer."""
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


def flatten(nested_items: Iterable[Iterable[Any]]) -> list[Any]:
    """Flatten an iterable containing one level of nested iterables."""
    return [item for group in nested_items for item in group]


def word_frequency(text: str) -> dict[str, int]:
    """Count case-insensitive whitespace-delimited words in text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    frequencies: dict[str, int] = {}
    for word in text.casefold().split():
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def main() -> None:
    """Run a small demonstration when this file is executed directly."""
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"is_prime(29): {is_prime(29)}")
    print(f"reverse_string('Codex'): {reverse_string('Codex')}")
    print(f"factorial(6): {factorial(6)}")
    print(f"greatest_common_divisor(84, 30): {greatest_common_divisor(84, 30)}")
    print(f"flatten([[1, 2], [3], [4, 5]]): {flatten([[1, 2], [3], [4, 5]])}")
    print(f"word_frequency('red blue red'): {word_frequency('red blue red')}")


if __name__ == "__main__":
    main()
