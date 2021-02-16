"""Mandala ported from https://twitter.com/lexaloffle/status/1325757361215078401
"""
from pypico8 import (
    cls,
    cos,
    line,
    pico8_to_python,
    printh,
    pset,
    sin,
    run,
    t,
)


printh(
    pico8_to_python(
        r"""
q,t,s=0,0,64::_::cls()for i=1,55do x,y=cos(i/55+t)*80,sin(i/55+t)*80n=(abs(x)+abs(y))/3for i=1,n do u,v=i/n+cos((i*i*3.1)+q*(i/n+1)/4)/9,i/n+cos((i*i*3.1)+(q+.04)*(i/n+1)/4)/9line(s+x*u,s+y*u,s+x*v,s+y*v,8+(i&4))pset(s+x*u,s+y*u,10)end end t+=.001q+=.02flip()goto _
        """
    )
)


def _init():
    global q, t, s
    q, t, s = 0, 0, 64


def _update():
    pass


def _draw():
    global q, t
    cls()
    for i in range(1, 56):
        x, y = cos(i / 55 + t) * 80, sin(i / 55 + t) * 80
        n = (abs(x) + abs(y)) / 3
        i = 1
        while i <= n:
            u, v = (
                i / n + cos((i * i * 3.1) + q * (i / n + 1) / 4) / 9,
                i / n + cos((i * i * 3.1) + (q + 0.04) * (i / n + 1) / 4) / 9,
            )
            line(s + x * u, s + y * u, s + x * v, s + y * v, 8 + (i & 4))
            pset(s + x * u, s + y * u, 10)
            i += 1
    t += 0.001
    q += 0.02


run(_init, _update, _draw)