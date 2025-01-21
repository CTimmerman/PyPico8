"""Fractus ported from https://twitter.com/MunroHoberman/status/1357378457458663431
"""

from pypico8 import *


printh(
    pico8_to_python(
        r"""
function u(x,y,a,n,c)q(x,y,n*.7,c)
    for i=-1,1do
        e=i/5+a+w/n
        if(n>5)u(x+cos(e)*n,y+sin(e)*n,e,n/2,c)
    end
end
q=circfill
::_::
    cls(12)
    q(63,63,56,170)
    w=sin(t()/8)
    u(63,80,.75,32,153)
    for y=0,127do
        n=24576+y*64
        memcpy(n,n+sin(t()+y/9)*y/64+2,60)
    end
    fillp(23895)
    u(63,63,.25,32,59)
    flip()
goto _
        """
    )
)


def _init():
    global q
    q = circfill


def u(x, y, a, n, c):
    q(x, y, n * 0.7, c)
    for i in range(-1, 2):
        e = i / 5 + a + w / n
        if n > 5:
            u(x + cos(e) * n, y + sin(e) * n, e, n / 2, c)


def _update():
    pass


def _draw():
    global w
    cls(12)
    q(63, 63, 56, 170)
    w = sin(t() / 8)
    u(63, 80, 0.75, 32, 153)
    for y in range(0, 128):
        n = 24576 + y * 64
        memcpy(n, n + sin(t() + y / 9) * y / 64 + 2, 60)  # apply wave effect to VRAM

    fillp(23895)
    u(63, 63, 0.25, 32, 59)


run(_init, _update, _draw)
