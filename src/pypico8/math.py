"""The pico8 manual math section implementations.
NOTE: Test with python math.py instead of python -m doctest math.py
"""

# pylint:disable = import-error, line-too-long, multiple-imports, no-name-in-module, redefined-builtin, unused-import
import builtins, math, random  # noqa: E401
from math import (
    ceil,  # noqa: F401
    floor,  # noqa: F401
)  # unused here but maybe not elsewhere.

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pypico8.infix import Infix


def _div(a: float | int, b: float | int) -> float | int:
    """Dividing by zero evaluates to 0x7fff.ffff if positive, or -0x7fff.ffff if negative.
    (-32768.0 to 32767.99999)
    >>> _div(1, 0)
    32768
    >>> _div(-1, 0)
    -32768
    >>> _div(1, 2)
    0.5
    """
    if not b:
        return -32768 if a < 0 else 32768
    return a / b


div = Infix(_div)


def _divi(a: float | int, b: float | int) -> int:
    """Divide and floor.
    >>> _divi(1, 0)
    32767
    >>> _divi(-1, 0)
    -32768
    >>> _divi(1, 2)
    0
    """
    if not b:
        return -32768 if a < 0 else 32767
    return math.floor(a / b)


divi = Infix(_divi)


def flr(v: int | float | str | None = 0) -> int:
    """Returns floored integer.

    >>> flr("65.5")
    65
    >>> flr("-65.5")
    -66
    """
    return floor(float(v))  # type: ignore


def hex_fraction(decimal_number: float, precision: int = 4) -> str:
    """Converts a decimal fraction to a string with a given precision.
    >>> hex_fraction(0.5)
    '8000'
    >>> hex_fraction(255.5)
    'FF8000'
    >>> hex_fraction(-0.025756836)
    '-0698'
    """
    hex_result = ""
    fraction = abs(decimal_number)

    for _ in range(precision):
        fraction *= 16
        digit = int(fraction)
        hex_result += hex(digit)[2:].upper()
        fraction -= digit

    if decimal_number < 0:
        return "-" + hex_result
    return hex_result


def max(first: float | int, second: float | int = 0) -> float | int:
    "Return max of two numbers."
    return builtins.max(first, second)


def min(first: float | int, second: float | int = 0) -> float | int:
    "Return min of two numbers."
    return builtins.min(first, second)


def mid(x: float | int, y: float | int, z: float | int = 0) -> float | int:
    """Returns the middle value of parameters
    >>> mid(7,5,10)
    7
    """
    a = [x, y, z]
    a.remove(builtins.min(a))
    a.remove(builtins.max(a))
    return a[0]


def round4(n: float) -> float | int:
    """Custom rounding function that always rounds down.
    >>> round4(-0.0001)
    -0.0
    >>> round4(-0.00011)
    -0.0001
    >>> round4(-0.000153)
    -0.0002
    >>> round4(2.00009)
    2
    >>> round4(0.00009)
    0
    >>> round4(0.00019)
    0.0002
    >>> round4(0.00016)
    0.0002
    >>> round4(0.00015)
    0.0001
    >>> round4(0.00069)
    0.0007
    >>> round4(0.00099)
    0.001
    >>> round4(0.9999)
    0.9999
    >>> round4(0.99991)
    1
    >>> round4(0.99981)
    0.9998
    >>> round4(0.025757)
    0.0258
    >>> round4(-0.025757)
    -0.0258
    >>> round4(-0.025756)
    -0.0257
    >>> round4(0.025756)
    0.0257
    >>> round4(-0.025756836)
    -0.0258
    >>> round4(-0.0257568359)
    -0.0257
    >>> round4(0.025756836)
    0.0258
    >>> round4(0.0257568359)
    0.0257
    """
    if n < 0:
        if n % 1 >= 0.9999:  # Note the =
            if n > -1:
                return -0.0
            return math.ceil(n)

    if n % 1 > 0.9999:
        return math.ceil(n)
    if n % 1 < 0.0001:
        return math.floor(n)

    return round(int(hex_fraction(n), 16) / 16**4 * 10**4) / 10**4


def rnd(x: float | int = 1) -> float:
    """Random number or item.
    >>> rnd(1e9) != rnd(1e9)
    True
    """
    if isinstance(x, dict):
        return random.choice(tuple(x))
    return round4(random.random() * x)


def _shl(x: float | int, n: int = 0) -> float | int:
    """Shift left n bits (zeros come in from the right)
    >>> shl(0.5, 1)
    1.0
    >>> shl(0.1, 1)
    0.2
    """
    return x * 2**n


shl = Infix(_shl)


def _shr(x: float | int, n: int = 0) -> float | int:
    """Arithmetic right shift (the left-most bit state is duplicated)
    >>> shr(2,1)
    1.0
    >>> shr(1,1)
    0.5
    >>> 1 |shr| 1
    0.5
    """
    return x / 2**n


shr = Infix(_shr)


def sgn(x: float | int = 0) -> int:
    """Return sign of number.
    >>> sgn(0)
    1
    >>> sgn(-0)
    1
    >>> sgn(-0.0)
    1
    >>> sgn(-0.1)
    -1
    """
    if x == 0:
        return 1
    return int(math.copysign(1, x))


def sqrt(x: float | int) -> float:
    """Square root x.
    >>> sqrt(2)
    1.4142
    """
    if x < 0:
        return 0
    return round(math.sqrt(x), 4)


def srand(x: int | float | str | None = 10) -> None:
    """Seed random number generator.
    >>> srand()
    >>> rnd()
    0.5714
    """
    random.seed(x)


def atan2(dx: float | int, dy: float | int) -> float:
    r"""
    Converts dx, dy into a clockwise angle >= 0 and < 1, aka [0, 1).
    for dy=1,-1,-1 do for dx=-1,1 do print(dx..", "..dy.." = "..atan2(dx,dy)) end end -- Lua/Pico8 version
    >>> print('\n'.join(f'{dx:2},{dy:2} = {atan2(dx,dy)}' for dy in range(1,-2,-1) for dx in range(-1,2)))
    -1, 1 = 0.625
     0, 1 = 0.75
     1, 1 = 0.875
    -1, 0 = 0.5
     0, 0 = 0.25
     1, 0 = 0.0
    -1,-1 = 0.375
     0,-1 = 0.25
     1,-1 = 0.125
    >>> atan2(1, 10)  # XXX: Pico8 0.2.2c rounds 0.7658538 to 0.7658 and 0.7658539 to 0.7659.
    0.7659
    """
    if dx == 0:
        if dy < 0:
            return 0.25
        if dy == 0:
            return 0.25
        if dy > 0:
            return 0.75

    if dy == 0:
        if dx < 0:
            return 0.5
        if dx > 0:
            return 0.0

    return round4((math.atan2(dy, -dx) / math.pi + 1) / 2)


def cos(x: float | int) -> float | int:
    """Cosine of 0..1 instead of 0..pi*2
    Pico8: for x=-1,1,0.25 do print(""..x.." = "..cos(x)) end
    >>> for x in range(-4,5): print(f"{x/4} = {cos(x/4)}")
    -1.0 = 1
    -0.75 = 0
    -0.5 = -1
    -0.25 = 0
    0.0 = 1
    0.25 = 0
    0.5 = -1
    0.75 = 0
    1.0 = 1
    >>> cos(0.004)
    0.9997
    >>> cos(0.0082)
    0.9987
    """
    rv = round4(math.cos(x * 2 * math.pi))
    if rv == 0:
        return 0
    return rv


def sin(x: float | int) -> float:
    """Inverted sine of 0..1 instead of 0..pi*2
    Pico8: for x=-1,1,0.25 do print(""..x.." = "..sin(x)) end
    >>> for x in range(-4,5): print(f"{x/4} = {sin(x/4)}")
    -1.0 = 0
    -0.75 = -1
    -0.5 = 0
    -0.25 = 1
    0.0 = 0
    0.25 = -1
    0.5 = 0
    0.75 = 1
    1.0 = 0
    >>> sin(0.0039)
    -0.0245

    # >>> sin(0.004)
    # -0.0253

    >>> sin(0.0041)
    -0.0257

    # >>> sin(0.0001)
    # -0.0008
    """
    rv = round4(math.sin((1 - x) * round4(2 * math.pi)))
    # Don't return -0.0
    if rv == 0:
        return 0
    return rv


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # doctest.run_docstring_examples(round4, globals())
