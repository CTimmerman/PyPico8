"""Curvy Lines ported from https://twitter.com/picoter8/status/1344334600479404034
"""

from pypico8 import camera, cls, line, run, sin, sqrt, t


def _init():
    global s
    s = 64
    camera(-s, -s)


def _update():
    pass


def _draw():
    cls()
    n = -s
    m = -s
    for j in range(-80, s + 1, 6):
        for i in range(-s, s + 1, 4):
            p = 40 * t() % 6
            y = j + p
            w = sqrt(i * i + y * y) / s
            v = y + 4 * sin(w * 2 + t())
            if i != -s:
                line(n, m, i, v, 7)
            n = i
            m = v


run(_init, _update, _draw)
