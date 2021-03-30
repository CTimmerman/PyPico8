"""The pico8 manual math section implementations.

>>> flr(4.1)
4
>>> ceil(4.1)
5
>>> flr(-2.3)
-3
>>> ceil(-2.3)
-2
"""
# pylint:disable=multiple-imports,redefined-builtin
import builtins, math, random
from math import ceil, floor as flr  # noqa; unused here but maybe not elsewhere.


def max(first, second=0):
    return builtins.max(first, second)


def min(first, second=0):
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
    return math.cos(x * (math.pi * 2))


def sin(x):
    return -math.sin(x * (math.pi * 2))


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
    return x * 2 ** n


def shr(x, n):
    """Arithmetic right shift (the left-most bit state is duplicated)
    >>> shr(2,1)
    1.0
    >>> shr(1,1)
    0.5
    """
    return x / 2 ** n


def srand(x=0):
    random.seed(x)


def sgn(x):
    return int(math.copysign(1, x))


def sqrt(x):
    if x < 0:
        return 0
    return math.sqrt(x)


def div(a, b):
    """Dividing by zero evaluates to 0x7fff.ffff if positive, or -0x7fff.ffff if negative. (-32768.0 to 32767.99999)"""
    if not b:
        return (-32768.0, 32767.99999)[bool(math.copysign(1, b) + 1)]
    return a / b


if __name__ == "__main__":
    import doctest

    doctest.testmod()