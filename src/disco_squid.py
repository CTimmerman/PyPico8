"""Disco Squid ported from https://www.facebook.com/lexaloffle/videos/1919955864701580/
"""
from pypico8 import circfill, cls, cos, rnd, run, sin, srand, t


def _draw():
    r = rnd
    srand()
    f = t() / 9
    cls()
    n = 650 + 60 * sin(f / 3)
    for i in range(1, int(n)):
        a = f + r(1)
        d = 0.3 + r(9)
        y = -3
        if i > 400:
            j = i - 400
            y = j * 2 / n - 1
            a = j * 40 / n + f + j / 3
            d = j * 3 / n

        x = d * cos(a)
        z = 2 + cos(f) + d * sin(a)
        x = 64 + x * 64 / z
        y = 64 + y * 64 / z
        c = 6 + i % 5
        e = 5 / z
        if z > 0.1:
            circfill(x, y, e, c)
            circfill(x, 128 - y, e, c / 4)


run(_draw=_draw)