"""Octopus ported from https://twitter.com/picoter8/status/1330759076943376384
"""
from pypico8 import circfill, cls, cos, run, sin, t


def _draw():
    cls()
    for r in range(16, 129, 6):
        a = 0
        while a < 1:
            a += 1 / r
            b = a + 0.1 * (1 - r / 96) * sin(0.8 * t() + r / 96)
            x = 62 + (r + 8 * sin(t() / 5)) * cos(b)
            y = 62 + (r + 8 * sin(t() / 5)) * sin(b)
            q = 3 * sin(a * 8 - t() / 5)
            circfill(x, y, q + 2, 2)
            circfill(x, y, q, 1)


run(_draw=_draw)