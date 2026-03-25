"""Example Python file for testing Doxen analysis."""

from typing import List, Optional


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def __init__(self, precision: int = 2) -> None:
        """Initialize calculator with specified precision.

        Args:
            precision: Number of decimal places for results
        """
        self.precision = precision

    def add(self, a: float, b: float) -> float:
        """Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        return round(a + b, self.precision)

    def multiply(self, numbers: List[float]) -> float:
        """Multiply a list of numbers.

        Args:
            numbers: List of numbers to multiply

        Returns:
            Product of all numbers
        """
        result = 1.0
        for num in numbers:
            result *= num
        return round(result, self.precision)


def factorial(n: int) -> int:
    """Calculate factorial of a number.

    Args:
        n: Non-negative integer

    Returns:
        Factorial of n

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def main() -> None:
    """Main entry point for calculator demo."""
    calc = Calculator(precision=3)
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"2 * 3 * 4 = {calc.multiply([2, 3, 4])}")
    print(f"5! = {factorial(5)}")


if __name__ == "__main__":
    main()
