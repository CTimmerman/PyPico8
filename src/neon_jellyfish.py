r"""Neon Jellyfish ported from https://twitter.com/von_rostock/status/1335561342321881088
c=cos::_::cls(3)m=t()r=0g=0h=0p=9+4*c(m)for b=0,1,.02do
pal(b*16,({-15,1,-4,12,6,7})[b*7\1],1)g+=.004+c(b-m)*b/69r+=c(g)h-=sin(g)l=1+b\.96*4for a=0,1,.02-b/99do
u=64+r*c(a)v=p+h+l*sin(a+b\.99/2)
if(a<.5)u=62+c(b-m+a\.17/3)*9*b+a*9v=p+b*99
pset(u,v,pget(u,v)+l)end
end
flip()goto _
"""

# pylint: disable=redefined-builtin
from pypico8 import (
    Table,
    cls,
    cos,
    pal,
    pget,
    pset,
    round4,
    run,
    sin,
    t,
)


def _draw():
    cls(3)
    m = t()
    r = 0
    g = 0
    h = 0
    p = 9 + 4 * cos(m)
    b = 0
    while b <= 1:
        pal(int(b * 16), (Table([-15, 1, -4, 12, 6, 7]))[b * 7 // 1] or 0, 1)
        g = round4(g + 0.004 + cos(b - m) * b / 69)
        r = round4(r + cos(g))
        h = round4(h - sin(g))
        L = round4(1 + b // 0.96 * 4)
        a = 0
        while a <= 1:
            u = 64 + r * cos(a)
            v = p + h + L * sin(a + b // 0.99 / 2)
            if a < 0.5:
                u = 62 + cos(b - m + a // 0.17 / 3) * 9 * b + a * 9
                v = p + b * 99
            col = pget(u, v) + L
            pset(u, v, col)
            a = round4(a + 0.02 - b / 99)
        b = round4(b + 0.02)


if __name__ == "__main__":
    run(_draw=_draw)
