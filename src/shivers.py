"""Shivers ported from https://twitter.com/von_rostock/status/1339009642756796423
"""

# pylint: disable=redefined-builtin
from pypico8 import (
    Table,
    cls,
    cos,
    max,
    pico8_to_python,
    pal,
    printh,
    pget,
    pset,
    rnd,
    run,
    sin,
    t,
)


printh(
    pico8_to_python(
        r"""pal({-16,-16,-14,-14,2,2,-8,-8,8,8},1)s=sin::_::c=t()%4
if(c<.1)m=rnd(19)n=rnd(19)cls(10)
for i=0,7do
u=m+54v=n+54for j=0,c*64do
g=u/512h=v/512k=i/8for l=1,5do g*=2h*=2k+=.5^l*(s(s(g)+s(h))+s(g*2)+t()%32/(1+j/3))/2end
u+=cos(k)/2v-=s(k)/2pset(u,v,max(pget(u,v)-1))end
end
goto _"""
    )
)


def _init():
    global m, n, s
    pal(Table([-16, -16, -14, -14, 2, 2, -8, -8, 8, 8]), 1)
    m = n = 0
    s = sin


def _update():
    pass


def _draw():
    global m, n
    c = t() % 4
    if c < 0.1:
        m = rnd(19)
        n = rnd(19)
        cls(10)
    for i in range(0, 8):
        u = m + 54
        v = n + 54
        for j in range(0, int(c * 64) + 1):
            g = u / 512
            h = v / 512
            k = i / 8
            for L in range(1, 6):
                g *= 2
                h *= 2
                k += 0.5**L * (s(s(g) + s(h)) + s(g * 2) + t() % 32 / (1 + j / 3)) / 2

            u += cos(k) / 2
            v -= s(k) / 2
            pset(u, v, max(pget(u, v) - 1))


if __name__ == "__main__":
    run(_init, _update, _draw)
