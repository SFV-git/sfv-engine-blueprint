"""A small collection of mathematical and string utility functions."""


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number, using F(0) = 0 and F(1) = 1."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    current, next_value = 0, 1
    for _ in range(n):
        current, next_value = next_value, current + next_value
    return current


def is_prime(number: int) -> bool:
    """Return True when number is prime, otherwise return False."""
    if not isinstance(number, int) or isinstance(number, bool):
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
    """Return text with its characters in reverse order."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text[::-1]


def main() -> None:
    """Demonstrate the utilities when this file is run directly."""
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"is_prime(29) = {is_prime(29)}")
    print(f"reverse_string('Blueprint') = {reverse_string('Blueprint')}")


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[MATHEMATICAL_UTILITIES|Mathematical Utilities]]
# - [[STRING_MANIPULATION|String Manipulation]]
# - [[UTILITY_FUNCTIONS|Utility Functions]]
# - [[CODE_QUALITY_GUIDELINES|Code Quality Guidelines]]
