"""The pico8 manual math section implementations.
NOTE: Test with python math.py instead of python -m doctest math.py
>>> flr(4.1)
4
>>> ceil(4.1)
5
>>> flr(-2.3)
-3
>>> ceil(-2.3)
-2
"""

# pylint:disable = line-too-long, multiple-imports, redefined-builtin, unused-import
import builtins, math, random  # noqa: E401
from math import (
    ceil,  # noqa: F401
    floor,  # noqa: F401
)  # unused here but maybe not elsewhere.

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pypico8.infix import Infix


def flr(v: int | float | str | None = 0) -> int:
    "Returns floored integer."
    return floor(float(v))  # type: ignore


def max(first, second=0):
    "Return max of two numbers."
    return builtins.max(first, second)


def min(first, second=0):
    "Return min of two numbers."
    return builtins.min(first, second)


def mid(x, y, z=0):
    """Returns the middle value of parameters
    >>> mid(7,5,10)
    7
    """
    a = [x, y, z]
    a.remove(builtins.min(a))
    a.remove(builtins.max(a))
    return a[0]


def cos(x):
    """Cosine of 0..1 instead of 0..pi*2
    Pico8: for x=-1,1,0.25 do print(""..x.." = "..cos(x)) end
    >>> for x in range(-4,5): print(f"{x/4} = {cos(x/4)}")
    -1.0 = 1.0
    -0.75 = -0.0
    -0.5 = -1.0
    -0.25 = 0.0
    0.0 = 1.0
    0.25 = 0.0
    0.5 = -1.0
    0.75 = -0.0
    1.0 = 1.0
    """
    return round(math.cos(x * 2 * math.pi), 4)


def sin(x):
    """Inverted sine of 0..1 instead of 0..pi*2
    Pico8: for x=-1,1,0.25 do print(""..x.." = "..sin(x)) end
    >>> for x in range(-4,5): print(f"{x/4} = {sin(x/4)}")
    -1.0 = -0.0
    -0.75 = -1.0
    -0.5 = 0.0
    -0.25 = 1.0
    0.0 = 0.0
    0.25 = -1.0
    0.5 = -0.0
    0.75 = 1.0
    1.0 = 0.0
    """
    return round((1 - math.sin(x * 2 * math.pi)) - 1, 4)


def atan2(dx, dy):
    r"""
    Converts dx, dy into a clockwise angle >= 0 and < 1, aka [0, 1).
    for dy=1,-1,-1 do for dx=-1,1 do print(dx..", "..dy.." = "..atan2(dx,dy)) end end -- Lua/Pico8 version
    >>> print('\n'.join(f'{dx:2},{dy:2} = {atan2(dx,dy)}' for dy in range(1,-2,-1) for dx in range(-1,2)))
    -1, 1 = 0.625
     0, 1 = 0.75
     1, 1 = 0.875
    -1, 0 = 0.5
     0, 0 = 0.25
     1, 0 = 0
    -1,-1 = 0.375
     0,-1 = 0.25
     1,-1 = 0.125
    """
    if dy == 0:
        if dx < 0:
            return 0.5
        if dx == 0:
            return 0.25
        if dx > 0:
            return 0

    return (math.atan2(dy, -dx) / math.pi + 1) / 2


def rnd(x=1):
    "Random number or item."
    if isinstance(x, dict):
        return random.choice(tuple(x))
    return random.random() * x


def shl(x, n):
    """Shift left n bits (zeros come in from the right)
    >>> shl(0.5, 1)
    1.0
    >>> shl(0.1, 1)
    0.2
    """
    return x * 2**n


def _shr(x, n):
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


def srand(x=0):
    "Seed random number generator."
    random.seed(x)


def sgn(x):
    """
    >>> sgn(0)
    1
    """
    return int(math.copysign(1, x))


def sqrt(x):
    "Square root x."
    if x < 0:
        return 0
    return math.sqrt(x)


def _div(a, b) -> float | int:
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


def _divi(a, b) -> int:
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

if __name__ == "__main__":
    import doctest

    doctest.testmod()
