"""No War ported from https://twitter.com/brubsby/status/1214986266720133121
"""

from pypico8 import (
    cls,
    cos,
    line,
    memcpy,
    pico8_to_python,
    print,
    printh,
    sin,
    srand,
    sspr,
    rnd,
    run,
    t,
)


printh(
    pico8_to_python(
        r"""cls(6)
?"no war",4,1,8
g=61memcpy(0,24576,999)r=rnd::_::srand(1)q=2*t()cls()y=50.3-cos(q)/2
for i=0,30 do
?"웃",q-r(g),y+r(40),r(16)
line(q+g*i,y,q+g*i,y+28,5)
?"웃",q+g*i-5,y+25,12
sspr(i,0,1,7,q+i*2,y-((i*2-30)^2-900)/(sin(q)+8)/g,2,14)end
flip()goto _"""
    )
)


def _init():
    global g, r
    cls(6)
    print("no war", 4, 1, 8)
    g = 61
    memcpy(0, 24576, 999)
    r = rnd


def _update():
    pass


def _draw():
    srand(1)
    q = 2 * t()
    cls()
    y = 50.3 - cos(q) / 2
    for i in range(0, 30 + 1):
        print("웃", q - r(g), y + r(40), r(16))
        line(q + g * i, y, q + g * i, y + 28, 5)
        print("웃", q + g * i - 5, y + 25, 12)
        # fmt: off
        sspr(i, 0, 1, 7, q + i * 2, y - ((i * 2 - 30) ** 2 - 900) / (sin(q) + 8) / g, 2, 14)


if __name__ == "__main__":
    run(_init, _update, _draw)
