"""Mandala ported from https://twitter.com/lexaloffle/status/1325757361215078401

printh(
    pico8_to_python(
        r'''
q,t,s=0,0,64::_::cls()for i=1,55do x,y=cos(i/55+t)*80,sin(i/55+t)*80n=(abs(x)+abs(y))/3for i=1,n do u,v=i/n+cos((i*i*3.1)+q*(i/n+1)/4)/9,i/n+cos((i*i*3.1)+(q+.04)*(i/n+1)/4)/9line(s+x*u,s+y*u,s+x*v,s+y*v,8+(i&4))pset(s+x*u,s+y*u,10)end end t+=.001q+=.02flip()goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import (
    cls,
    cos,
    line,
    pset,
    sin,
    run,
)


def _init() -> None:
    global q, t2, s
    q, t2, s = 0, 0, 64


def _update() -> None:
    pass


def _draw() -> None:
    global q, t2
    cls()
    for i in range(1, 56):
        x, y = cos(i / 55 + t2) * 80, sin(i / 55 + t2) * 80
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
    t2 += 0.001
    q += 0.02


if __name__ == "__main__":
    run(_init, _update, _draw)
