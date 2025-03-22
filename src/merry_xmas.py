"""Merry Xmas ported from https://twitter.com/Frozax/status/1342463299909275651

printh(
    pico8_to_python(
        r'''
pal({129,1,140,12,7},1)
::_::
cls(1)
function e(x,y,r,d)
    local d,x,y,r,s,a=d-1,x,y,r,r\2,t()/6
    if(d%2==0)a=-a
    v=(r+s)*1.2
    local f,g=cos(a)*v,sin(a)*v
    if(d>0)e(x+f,y+g,s,d)e(x-f,y-g,s,d)e(x-g,y+f,s,d)e(x+g,y-f,s,d)
    circfill(x,y,r,5-d)
end
e(64,64,25,5)
?"merry xmas",45,62,7
flip()goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    pal(Table([129, 1, 140, 12, 7]), 1)


def _update() -> None:
    pass


def _draw() -> None:
    cls(1)

    def e(x, y, r, d):
        d, s, a = d - 1, r // 2, t() / 6
        if d % 2 == 0:
            a = -a
        v = (r + s) * 1.2
        f, g = cos(a) * v, sin(a) * v
        if d > 0:
            e(x + f, y + g, s, d)
            e(x - f, y - g, s, d)
            e(x - g, y + f, s, d)
            e(x + g, y - f, s, d)
        circfill(x, y, r, 5 - d)

    e(64, 64, 25, 5)
    print("merry xmas", 45, 62, 7)


if __name__ == "__main__":
    run(_init, _update, _draw)
