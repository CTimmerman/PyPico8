"""Dancing Rectangles ported from https://twitter.com/picoter8/status/1334310272509620224 #pico8 #tweetcart #tweetjam
"""
from pypico8 import camera, cls, cos, line, run, sin, t


def _init():
    camera(-64, -64)


def _update():
    pass


def _draw():
    cls()
    for k in range(18, 97, 18):
        c = k / 18
        i = 0
        while i <= 1:
            b = i - t() / 24 * c
            x = k * cos(b)
            y = k * sin(b)
            o = 0
            p = 0
            j = 0
            while j <= 1:
                a = 64 / k + i * c + j - t() / 4 * c
                n = 8 * cos(a)
                m = 8 * sin(a)
                if o != p:
                    line(x + n, y + m, x + o, y + p, 7)
                o = n
                p = m
                j += 0.25
            i += 0.1 / c


run(_init, _update, _draw)