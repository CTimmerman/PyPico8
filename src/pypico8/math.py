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
from math import ceil, floor as flr, sqrt  # noqa; unused here but maybe not elsewhere.


def max(first, second=0):
    return builtins.max(first, second)


def min(first, second=0):
    return builtins.min(first, second)


def mid(x, y, z):
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
    """
    Converts dx, dy into an angle from 0..1
    As with cos/sin, angle is taken to run anticlockwise in screenspace

    Longer vector uses the ratio:
    >>> atan2(99, 99)
    0.875

    Special case:
    >>> atan2(0, 0)
    0.25

    >>> [(x,y, atan2(x,y)) for x in range(-1,2) for y in range(-1,2)]
    [(-1, -1, -0.375), (-1, 0, 0.5), (-1, 1, 0.625), (0, -1, -0.25), (0, 0, 0.25), (0, 1, 0.75), (1, -1, 0.125), (1, 0, 0.0), (1, 1, 0.875)]
    """
    newangle = math.atan2(dy, -dx)
    normalizedangle = (newangle / math.pi + 1) / 2
    return normalizedangle


def rnd(x=1):
    if isinstance(x, dict):
        return random.choice(tuple(x))
    return random.random() * x


def srand(x=0):
    random.seed(x)


def sgn(x):
    return math.copysign(1, x)


def div(a, b):
    """Dividing by zero evaluates to 0x7fff.ffff if positive, or -0x7fff.ffff if negative. (-32768.0 to 32767.99999)"""
    if not b:
        return (-32768.0, 32767.99999)[bool(math.copysign(1, b) + 1)]
    return a / b