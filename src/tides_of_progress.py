"""Tides of Progress ported from https://twitter.com/MunroHoberman/status/1363231958772441089
"""

# flake8:noqa
from pypico8 import *


printh(
    pico8_to_python(
        r"""
pal({-15,1,-13,-5,11,-6,-9,7,10,9,-7,8,-8,2,-14},1)
f=0
::_::
e=t()/8
x=rnd(2)
y=rnd(2)
n=abs(x-1)+sin(e)
m=abs(y-1)+cos(e)
circ(x*64,y*64,1,sqrt(n*n+m*m)*sin(e)*15)
f+=1
goto _
        """
    )
)


def _init():
    global f
    pal(Table([-15, 1, -13, -5, 11, -6, -9, 7, 10, 9, -7, 8, -8, 2, -14]), 1)
    f = 0


def _update():
    pass


def _draw():
    global f
    for _ in range(3000):
        e = t() / 8
        x = rnd(2)
        y = rnd(2)
        n = abs(x - 1) + sin(e)
        m = abs(y - 1) + cos(e)
        circ(x * 64, y * 64, 1, sqrt(n * n + m * m) * sin(e) * 15)
        f += 1


if __name__ == "__main__":
    run(_init, _update, _draw)
