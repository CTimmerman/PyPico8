"""Based on ChatGPT but modified for proper precedence and looks."""

from typing import TypeVar, Callable, Generic

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class InfixDiv(Generic[T, U, V]):
    """
    Infix operator with div precedence.

    >>> 1 + 1 / 2
    1.5
    >>> div = InfixDiv(lambda x,y: x / y)
    >>> 1 + 1 /div/ 2
    1.5
    """

    def __init__(self, func: Callable[[T, U], V]) -> None:
        """
        Initializes the infix operator with a binary function.

        >>> def multiply(x: int, y: int) -> int:
        ...     return x * y
        >>> times = InfixDiv(multiply)
        """
        self.func = func

    def __rtruediv__(self, left: T) -> "InfixDivPartial[T, U, V]":
        """
        Handles the left-hand operand.

        >>> def subtract(x: int, y: int) -> int:
        ...     return x - y
        >>> minus = InfixDiv(subtract)
        >>> partial = 10 /minus
        >>> isinstance(partial, InfixDivPartial)
        True
        """
        return InfixDivPartial(left, self.func)

    def __truediv__(self, right: U) -> V:
        """
        Prevents incorrect usage of the infix operator.

        >>> plus = InfixDiv(lambda x, y: x + y)
        >>> try:
        ...     plus / 5  # Incorrect usage
        ... except TypeError as e:
        ...     print(e)
        Left-hand operand is required before applying the right-hand operand.
        """
        raise TypeError(
            "Left-hand operand is required before applying the right-hand operand."
        )

    def __call__(self, value1: T, value2: U) -> V:
        """
        >>> div = InfixDiv(lambda x,y: x / y)
        >>> div(1, 2)
        0.5
        """
        return self.func(value1, value2)


class InfixDivPartial(Generic[T, U, V]):  # pylint: disable=too-few-public-methods
    """
    Handles the second operand of an infix operation.

    >>> def power(x: int, y: int) -> int:
    ...     return x ** y

    >>> exponent = InfixDiv(power)
    >>> partial = 2 /exponent
    >>> result = partial / 3
    >>> result
    8
    """

    def __init__(self, left: T, func: Callable[[T, U], V]) -> None:
        """
        Stores the left-hand operand and function.

        >>> def divide(x: int, y: int) -> float:
        ...     return x / y
        >>> half = InfixDiv(divide)
        >>> partial = 10 /half
        >>> isinstance(partial, InfixDivPartial)
        True
        """
        self.left = left
        self.func = func

    def __truediv__(self, right: U) -> V:
        """
        Applies the function when the right operand is provided.

        >>> def mod(x: int, y: int) -> int:
        ...     return x % y

        >>> modulo = InfixDiv(mod)
        >>> 10 /modulo/ 3
        1
        """
        return self.func(self.left, right)


class InfixShift(Generic[T, U, V]):
    """Infix operator with shift precedence.
    >>> 1 + 1 << 1
    4
    >>> shl = InfixShift(lambda x,y: x << y)
    >>> 1 + 1 <<shl>> 1
    4
    >>> shl(2, 1)
    4
    """

    def __init__(self, func: Callable[[T, U], V]) -> None:
        """
        Initializes the infix operator with a binary function.

        >>> def multiply(x: int, y: int) -> int:
        ...     return x * y
        >>> times = InfixShift(multiply)
        """
        self.func = func

    def __rlshift__(self, left: T) -> "InfixShiftPartial[T, U, V]":
        """
        Handles the left-hand operand.

        >>> def subtract(x: int, y: int) -> int:
        ...     return x - y
        >>> minus = InfixShift(subtract)
        >>> partial = 10 <<minus
        >>> isinstance(partial, InfixShiftPartial)
        True
        """
        return InfixShiftPartial(left, self.func)

    def __rshift__(self, right: U) -> V:
        """
        Prevents incorrect usage of the infix operator.

        >>> plus = InfixShift(lambda x, y: x + y)
        >>> try:
        ...     plus >> 5  # Incorrect usage
        ... except TypeError as e:
        ...     print(e)
        Left-hand operand is required before applying the right-hand operand.
        """
        raise TypeError(
            "Left-hand operand is required before applying the right-hand operand."
        )

    def __call__(self, value1: T, value2: U) -> V:
        """
        >>> div = InfixShift(lambda x,y: x / y)
        >>> div(1, 2)
        0.5
        """
        return self.func(value1, value2)


class InfixShiftPartial(Generic[T, U, V]):  # pylint: disable=too-few-public-methods
    """
    Handles the second operand of an infix operation.

    >>> def power(x: int, y: int) -> int:
    ...     return x ** y

    >>> exponent = InfixShift(power)
    >>> partial = 2 <<exponent
    >>> result = partial >> 3
    >>> result
    8
    """

    def __init__(self, left: T, func: Callable[[T, U], V]) -> None:
        """
        Stores the left-hand operand and function.

        >>> def divide(x: int, y: int) -> float:
        ...     return x / y
        >>> half = InfixShift(divide)
        >>> partial = 10 <<half
        >>> isinstance(partial, InfixShiftPartial)
        True
        """
        self.left = left
        self.func = func

    def __rshift__(self, right: U) -> V:
        """
        Applies the function when the right operand is provided.

        >>> def mod(x: int, y: int) -> int:
        ...     return x % y

        >>> modulo = InfixShift(mod)
        >>> 10 <<modulo>> 3
        1
        """
        return self.func(self.left, right)
