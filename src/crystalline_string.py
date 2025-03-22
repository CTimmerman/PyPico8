"""Crystalline String ported from https://twitter.com/lexaloffle/status/1362072813834620929

printh(
    pico8_to_python(
        r'''
cls()
z,q=0,{}
for z=0,1,2>>9 do
    add(q,{x=64,y=64,u=cos(z)/4,v=sin(z)/4})
end
::☉::
for d=0x6000,0x7fff,2 do
    poke2(d,%d/7.9)
end
line(7)
for a in all(q) do
    line(a.x,a.y)
    for j=1,4 do
        if((a.x+a.u)\1&~127!=0)a.u*=-1
        if((a.y+a.v)\1&~127!=0)a.v*=-1
        a.x+=a.u
        a.y+=a.v
    end
end
flip()
goto ☉
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    global z, q
    cls()
    z = 0.0
    q = Table()
    while float(z) <= 1:  # mypy 1.15.0 thinks z is a Table otherwise.
        add(q, Table(x=64, y=64, u=cos(z) / 4, v=sin(z) / 4))
        z = float(z) + shr(2, 9)


def _update() -> None:
    pass


def _draw() -> None:
    d = 0x6000
    while d <= 0x7FFF:
        poke2(d, peek2(d) / 7.9)
        d += 2

    color(7)
    for a in all(q):
        line(a.x, a.y)
        for _ in range(1, 4 + 1):
            if int(a.x + a.u) & ~127 != 0:
                a.u *= -1
            if int(a.y + a.v) & ~127 != 0:
                a.v *= -1
            a.x += a.u
            a.y += a.v


if __name__ == "__main__":
    run(_init, _update, _draw)
