"""Squares & Circles ported from https://twitter.com/kadoyan/status/1359150102728876041
"""
from pypico8 import (  # noqa
    Table,
    circfill,
    cls,
    cos,
    flr,
    rectfill,
    pico8_to_python,
    printh,
    sin,
    run,
)


printh(
    pico8_to_python(
        r"""
f,r,c,b=flr,16,{3,0},circfill
function o(c,s,t)for n=0.5,1.5,0.01 do
x,y,d=63+cos(n)*-s+t,63+sin(n)*s,flr(abs(1-n)*10)b(x,y,d,c)end
end
t=0::_::cls()t+=1
for n=0,99 do
x,l=n%10*r-t%r,f(n/10)y=l*r-t%r
rectfill(x,y,x+r,y+r,c[l%2+n%2])end
b(63,63,40,7)o(0,38,-2)o(8,40,0)flip()goto _
        """
    )
)


def _init():
    global f, r, c, b, t
    f, r, c, b, t = flr, 16, Table([3, 0]), circfill, 0


def o(c, s, t):
    n = 0.5
    while n <= 1.5:
        x, y, d = 63 + cos(n) * -s + t, 63 + sin(n) * s, flr(abs(1 - n) * 10)
        b(x, y, d, c)
        n += 0.01


def _update():
    pass


def _draw():
    global t
    cls()
    t += 1
    for n in range(0, 99 + 1):
        x, L = n % 10 * r - t % r, f(n / 10)
        y = L * r - t % r
        rectfill(x, y, x + r, y + r, c[L % 2 + n % 2])

    b(63, 63, 40, 7)
    o(0, 38, -2)
    o(8, 40, 0)


run(_init, _update, _draw)