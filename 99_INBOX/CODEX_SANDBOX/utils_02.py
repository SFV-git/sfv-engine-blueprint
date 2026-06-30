"""Small, dependency-free mathematical utility functions."""


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


def main() -> None:
    """Demonstrate both utilities when this file is run directly."""
    print(f"Fibonacci(10): {fibonacci(10)}")
    print(f"Is 29 prime? {is_prime(29)}")


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[input_validation|Input Validation and Error Handling in Python Functions]]
# - [[algorithm_efficiency|Algorithm Efficiency and Time Complexity Analysis]]
# - [[utility_module_design|Best Practices for Designing Reusable Utility Modules]]
# - [[mathematical_algorithms|Mathematical Algorithms and Their Implementations]]
