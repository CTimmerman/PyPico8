"""Moving Maze ported from https://twitter.com/lucatron_/status/1296340853636517888
2020-12-18 v0.1 by Cees Timmerman
2021-01-03 v1.0 fixed scaling
2021-01-04 v1.0.1 fixed cos, sin
2021-01-07 v1.0.2 refactored
2021-01-11 v1.0.3 fixed height
"""

from pypico8 import cls, cos, line, mid, rnd, run, sin, srand, t


def _draw():
    cls(8)
    srand(5)
    for y in range(0, 129, 8):
        for x in range(0, 129, 8):
            a = rnd() + t() / 25
            u = mid(-4, 4, cos(a) * 120)
            v = mid(-4, 4, sin(a) * 120)
            for i in range(0, 4):
                line(x + u, y + v - i, x - u, y - v - i, i > 2 and 7 or 2)


run(_draw=_draw)
