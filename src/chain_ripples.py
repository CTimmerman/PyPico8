"""Chain Ripples PICO-8 demo ported from https://twitter.com/picoter8/status/1329225930196332545
"""

from pypico8 import cls, cos, rectfill, run, t


def _draw():
    cls()
    for j in range(-6, 136, 3):
        for i in range(-6, 136, 3):
            if (i + j) % 6 >= 3:
                x = 64 - i
                y = 64 - j
                p = (x * x + y * y) ** 0.5
                m = 6 * cos(p / 80 - t())
                rectfill(i, j + m, i + 1, j + 3 + m, 7)


if __name__ == "__main__":
    run(_draw=_draw)
