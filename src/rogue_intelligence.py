"""Rogue Intelligence ported from https://twitter.com/MunroHoberman/status/1361314323012988938
"""
# pylint: disable=redefined-builtin
from pypico8 import (
    Table,
    cos,
    line,
    max,
    pget,
    pset,
    pal,
    pico8_to_python,
    printh,
    run,
    sin,
    t,
)


printh(
    pico8_to_python(
        r"""function v(x,y,n,a)j=x+n*cos(a)k=y+n*s(a)line(x,y,j,k,7)x=j
y=k
for i=-1,1do
if(n>2)v(x,y,n/2,a+i/4+max(s(l)))end
end
pal({-16,2,-8,-2,-1,15},1)s=sin::_::l=t()/8for y=0,127,3do
for x=0,127do
z=(y-l*999)%127pset(x,z,abs(pget(x,z)-1))end
end
for i=0,4do
v(63,63,29,i/4+l)end
goto _"""
    )
)


def _init():
    pal(Table([-16, 2, -8, -2, -1, 15]), 1)


def v(x, y, n, a):
    s = sin
    j = x + n * cos(a)
    k = y + n * s(a)
    line(x, y, j, k, 7)
    x = j
    y = k
    for i in range(-1, 2):
        if n > 2:
            v(x, y, n / 2, a + i / 4 + max(s(L)))


def _update():
    pass


def _draw():
    global L
    L = t() / 8
    y = 0
    while y <= 127:
        for x in range(0, 128):
            z = (y - L * 999) % 127
            pset(x, z, abs(pget(x, z) - 1))
        y += 3

    for i in range(0, 5):
        v(63, 63, 29, i / 4 + L)


run(_init, _update, _draw)