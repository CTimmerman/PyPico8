"""Galaxy ported from https://twitter.com/2DArray/status/1357871341769289730

printh(
    pico8_to_python(
        '''
for i=0,10 do
pal(i,({0,129,1,140,12,139,11,138,10,135,7})[i+1],1)end
cls()::_::x=rnd(8)-4z=rnd(8)-4y=rnd(2)-1q=sqrt(x*x+y*y+z*z)/4m=max(1-q)c=(atan2(x,z)-m*m-t()/32)*44%11*m
if(q<.2)c=11
if(q>1)c=0
u=64+x*20-y*8v=64+z*16+y*8+x*10p=pget(u,v)pset(u,v,p+.5+(c-p)/2)goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import (
    Table,
    atan2,
    cls,
    max,
    pal,
    pget,
    pset,
    rnd,
    run,
    sqrt,
    t,
)


def _init() -> None:
    for i in range(0, 10 + 1):
        pal(i, (Table([0, 129, 1, 140, 12, 139, 11, 138, 10, 135, 7]))[i + 1], 1)
    cls()


def _update() -> None:
    pass


def _draw() -> None:
    for _ in range(9000):
        x = rnd(8) - 4
        z = rnd(8) - 4
        y = rnd(2) - 1
        q = sqrt(x * x + y * y + z * z) / 4
        m = max(1 - q)
        c = (atan2(x, z) - m * m - t() / 32) * 44 % 11 * m
        if q < 0.2:
            c = 11
        if q > 1:
            c = 0
        u = 64 + x * 20 - y * 8
        v = 64 + z * 16 + y * 8 + x * 10
        p = pget(u, v)
        pset(u, v, p + 0.5 + (c - p) / 2)


if __name__ == "__main__":
    run(_init, _update, _draw)
