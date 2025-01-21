"""Jenga ported from https://twitter.com/kometbomb/status/1360666863177449473
"""

from pypico8 import (
    cls,
    cos,
    fillp,
    pico8_to_python,
    printh,
    rect,
    sin,
    run,
    t,
)


printh(
    pico8_to_python(
        r"""
fillp(23130)::_::cls()b=t()/9for p=0,140do
l=13-p\10s=p\5%2*2-1i=p%5r=cos(l*s*sin(b/3)/9)/9+b-i/4v,w,q=j,y,x
y=l*s*6z=3/(sin(r)+4)x,y,j=cos(r)*48*z,y*z+64,64+z*(y+6)
if(i>0)c=(x-q)/12for a=q,x do d=(a-q)/(x-q)rect(a+64,(y-w)*d+w,a+64,(j-v)*d+v,c\1+(c+.5)\1*16)end
end
flip()goto _
        """
    )
)


def _init():
    global j, x, y
    j = x = y = 0
    fillp(23130)


def _update():
    pass


def _draw():
    global j, x, y
    cls()
    b = t() / 9
    for p in range(0, 140 + 1):
        L = 13 - p // 10
        s = p // 5 % 2 * 2 - 1
        i = p % 5
        r = cos(L * s * sin(b / 3) / 9) / 9 + b - i / 4
        v, w, q = j, y, x
        y = L * s * 6
        z = 3 / (sin(r) + 4)
        x, y, j = cos(r) * 48 * z, y * z + 64, 64 + z * (y + 6)
        if i > 0:
            c = (x - q) / 12
            a = q
            while a <= x:
                d = (a - q) / (x - q)
                rect(
                    a + 64,
                    (y - w) * d + w,
                    a + 64,
                    (j - v) * d + v,
                    c // 1 + (c + 0.5) // 1 * 16,
                )
                a += 1


run(_init, _update, _draw)
