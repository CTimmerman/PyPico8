"""Ported from https://twitter.com/Andy_Makes/status/1381801446916698118

printh(
    pico8_to_python(
        r'''
pal({10,9,137,142,8,7,12,140,1,2},1)
::Gem stone::
o=20*(t()%1)
cls(1)
for d=5,1,-1do
for c=-1,8do
for r=-1,8do
x=c*20
y=r*20
s=((d/5)^1.6)*(15+sin((x+y+o*2)*.005+t())*7)
rectfill(x-s+o,y-s+o,x+s+o,y+s+o,d+((c+r)%2)*5)
end
end
end
flip()goto Gem stone
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    pal(Table([10, 9, 137, 142, 8, 7, 12, 140, 1, 2]), 1)


def _update() -> None:
    pass


def _draw() -> None:
    o = 20 * (t() % 1)
    cls(1)
    d = 5
    while d >= 1:
        for c in range(-1, 8 + 1):
            for r in range(-1, 8 + 1):
                x = c * 20
                y = r * 20
                s = ((d / 5) ** 1.6) * (15 + sin((x + y + o * 2) * 0.005 + t()) * 7)
                rectfill(
                    x - s + o, y - s + o, x + s + o, y + s + o, d + ((c + r) % 2) * 5
                )

        d += -1


if __name__ == "__main__":
    run(_init, _update, _draw)
