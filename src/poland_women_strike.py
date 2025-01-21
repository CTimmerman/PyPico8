"""All-Poland Women's Strike ported from https://twitter.com/von_rostock/status/1328125395858812934
TODO: fix tatter
"""

# pylint: disable=redefined-builtin
from pypico8 import (
    cls,
    cos,
    line,
    pico8_to_python,
    printh,
    pset,
    rnd,
    run,
    sin,
    sget,
    sset,
    t,
)


printh(
    pico8_to_python(
        r"""::_::cls(1)for b=0,127do
y=rnd(88)c=1u=64-y/4
if(y>51)c=2.1
if(y>64)u+=24c=1
sset(u+rnd(22*c-y/4),y+16,8)a=b/128+t()x=64+cos(a/4)*60y=32+sin(a/2)*8p=22-x/3q=59-y/3
for a=0,1,.02do pset(x+p*a,y+q*a,sget(b,a*128))end
end
line(x,y,64,192,4)line(x-1,y)flip()goto _"""
    )
)


def _init():
    pass


def _update():
    pass


def _draw():
    cls(1)
    for b in range(0, 128):
        y = rnd(88)
        c = 1
        u = 64 - y / 4
        if y > 51:
            c = 2.1
        if y > 64:
            u += 24
            c = 1
        sset(u + rnd(22 * c - y / 4), y + 16, 8)
        a = b / 128 + t()
        x = 64 + cos(a / 4) * 60
        y = 32 + sin(a / 2) * 8
        p = 22 - x / 3
        q = 59 - y / 3
        a = 0
        while a <= 1:
            pset(x + p * a, y + q * a, sget(b, a * 128))
            a += 0.02

    line(x, y, 64, 192, 4)
    line(x - 1, y)


run(_init, _update, _draw)
