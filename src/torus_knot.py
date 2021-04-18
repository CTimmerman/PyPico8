"""Torus Knot ported from https://twitter.com/p01/status/1243498820450881536
"""
from pypico8 import *


printh(
    pico8_to_python(
        r"""
c=circfill
d=cos::_::s=t()for i=1,99 do
if(i<6)pal(i,-({16,14,11,3,10})[i],1)c(64,64,(6-i+s%2)^3,i%2)
m=i/198*d(i/2)q=64/(4+d(m))j=2+i/19
fillp(({1034,1394,22447})[flr(j*4%4)])
c(64+2*q*sin(m),64+q*d(s/2+m),q-9*d(m*3-s)*d(s/9),j+flr(j+.7)*16)end
?"tOrus\nknOt",9,9
flip()goto _
        """
    )
)


def _init():
    global c, d
    c = circfill
    d = cos


def _update():
    pass


def _draw():
    s = t()
    for i in range(1, 99 + 1):
        if i < 6:
            pal(i, -(Table([16, 14, 11, 3, 10]))[i], 1)
            c(64, 64, (6 - i + s % 2) ** 3, i % 2)
        m = i / 198 * d(i / 2)
        q = 64 / (4 + d(m))
        j = 2 + i / 19
        fillp((Table([1034, 1394, 22447]))[flr(j * 4 % 4)])
        c(
            64 + 2 * q * sin(m),
            64 + q * d(s / 2 + m),
            q - 9 * d(m * 3 - s) * d(s / 9),
            j + flr(j + 0.7) * 16,
        )

    print("T☉RUS\nKN☉T", 9, 9)


run(_init, _update, _draw)