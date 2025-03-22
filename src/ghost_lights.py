"""Ghost Lights ported from https://twitter.com/Andy_Makes/status/1298999311254994951

printh(
    pico8_to_python(
        r'''
pal({7,11,138,13,141},1)t=0r=rnd::Ghost::
t+=.01for i=0,199 do
circ(r(128),r(128),3,0)end
for z=5,1,-1 do
for k=1,2.7,.3 do
x,y=64+sin(t*.9+k)*50,64+cos(t*k+k)*50
for i=0,z*20 do
a=r(1)p=(z/5)^2d=p*25+r(p*10)circfill(x+sin(a)*d,y+cos(a)*d,5-z,z)end
end
end
flip()goto Ghost
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    global t2, r
    pal(Table([7, 11, 138, 13, 141]), 1)
    t2 = 0
    r = rnd


def _update() -> None:
    pass


def _draw() -> None:
    global t2
    t2 += 0.01
    for _ in range(0, 199 + 1):
        circ(r(128), r(128), 3, 0)
    z = 5
    while z >= 1:
        k = 1.0
        while k <= 2.7:
            x, y = 64 + sin(t2 * 0.9 + k) * 50, 64 + cos(t2 * k + k) * 50
            for _ in range(0, z * 20 + 1):
                a = r(1)
                p = (z / 5) ** 2
                d = p * 25 + r(p * 10)
                circfill(x + sin(a) * d, y + cos(a) * d, 5 - z, z)
            k += 0.3
        z += -1


if __name__ == "__main__":
    run(_init, _update, _draw)
