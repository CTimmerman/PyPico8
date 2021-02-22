"""Archery ported from https://twitter.com/MunroHoberman/status/1361011664452259843
"""
# pylint: disable=redefined-builtin
from pypico8 import (
    cls,
    cos,
    pico8_to_python,
    printh,
    run,
    sin,
    mid,
    flip,
    camera,
    line,
    circ,
    btn,
    print,
    min,
)


printh(
    pico8_to_python(
        r"""
    d=0
    v=0
    f=.9
    n=0
    e=line
::_::
    cls(7)
    for i=40,9,-3do
        circ(0,-500,i,i%2+7)
    end
    l=50-d
    z=d*3e(-l,0,0,z,8)e(l,0)
    for i=0,.5,.1do
        e(cos(i)*l,sin(i)*(20+d))
    end
    z-=v
    ?"♥",-3,z-54,14
    e(0,z,0,z-48)
    if btn(4)then
        d=min(d+1,9)
    elseif d>4then
        f=.5n=9
    end
    d*=f
    v=mid(v+n,447)
    flip()
    camera(-63,z-99)
    goto _
"""
    )
)


def _init():
    global d, v, f, n

    d = 0
    v = 0
    f = 0.9
    n = 0


def _update():
    pass


def _draw():
    global d, v, f, n

    cls(7)

    # target
    i = 40
    while i >= 9:
        circ(0, -500, i, i % 2 + 7)
        i += -3

    # bow
    L = 50 - d
    z = d * 3
    # string
    line(-L, 0, 0, z, 8)
    line(L, 0)
    i = 0
    # handle
    while i <= 0.5:
        line(cos(i) * L, sin(i) * (20 + d))
        i += 0.1

    # arrow
    z -= v
    print("♥", -3, z - 54, 14)
    line(0, z, 0, z - 48)
    if btn(4):
        d = min(d + 1, 9)
    elif d > 4:
        f = 0.5
        n = 9

    d *= f
    v = mid(v + n, 447)
    flip()
    camera(-63, z - 99)


run(_init, _update, _draw)