from pypico8 import *


def _init():
    """
    >>> _init()
    >>> pget(0, 0)
    3
    >>> pget(3, 3)
    4
    """
    fillp(1)
    for y in range(129):
        for x in range(129):
            pset(x, y, 1 + 2 * 16)
    rectfill(0, 0, 10, 10, 3 + 4 * 16)
    circfill(64, 64, 10, 5 + 6 * 16)
    ovalfill(80, 80, 90, 90, 7 + 8 * 16)
    line(126, 0, 0, 126, 0 + 9 * 16)


run(_init)
