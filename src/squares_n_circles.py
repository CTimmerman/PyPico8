"""Squares & Circles ported from https://twitter.com/kadoyan/status/1359150102728876041

printh(
    pico8_to_python(
        r'''
f,r,c,b=flr,16,{3,0},circfill
function o(c,s,t)
    for n=0.5,1.5,0.01 do
        x,y,d=63+cos(n)*-s+t,63+sin(n)*s,flr(abs(1-n)*10)b(x,y,d,c)
    end
end
t=0

::_::
cls()
t+=1
for n=0,99 do
    x,l=n%10*r-t%r,f(n/10)
    y=l*r-t%r
    rectfill(x,y,x+r,y+r,c[l%2+n%2])
end
b(63,63,40,7)o(0,38,-2)o(8,40,0)flip()goto _
        '''
    )
)

>>> run(_draw=_draw)
"""

# pylint: disable = global-statement, invalid-name
from pypico8 import (
    Table,
    circfill,
    cos,
    flr,
    rectfill,
    sin,
    run,
)


ct = Table([3, 0])
r: int = 16  # Rectangle size.
t: int = 0


def logo(c, size, wut):
    "Draw crescent in color c."
    n = 0.5
    while n <= 1.5:
        x, y, d = 63 + cos(n) * -size + wut, 63 + sin(n) * size, flr(abs(1 - n) * 10)
        circfill(x, y, d, c)
        n += 0.01


def _draw() -> None:
    global t
    t += 1
    for n in range(0, 99 + 1):
        x = n % 10 * r - t % r
        L = flr(n / 10)  # Layer, back to front.
        y = L * r - t % r
        rectfill(x, y, x + r, y + r, ct[L % 2 + n % 2])  # or color [0, 3][(L + n) % 2]

    circfill(63, 63, 40, 7)  # logo white
    logo(0, 38, -2)  # logo black
    logo(8, 40, 0)  # logo pink


if __name__ == "__main__":
    run(_draw=_draw)
