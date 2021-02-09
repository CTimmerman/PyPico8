"""Eyes ported from https://twitter.com/lexaloffle/status/1340466318697324544
"""
# fmt: off
from pypico8 import atan2, circfill, cls, cos, pico8_to_python, poke, printh, rnd, run, sin, srand, stat
# fmt: on

printh(
    pico8_to_python(
        r"""poke(0x5f2d,1)c=circfill::☉::cls(1)srand()for i=1,99do
r,x,y=rnd(5)+5,rnd(128),rnd(128)
c(x,y,r+1,0)c(x,y,r,7)u,v=stat(32),stat(33)
a=atan2(u-x,v-y)x+=cos(a)*r/2y+=sin(a)*r/2
c(x,y,r/2,13)c(x,y,r/3,0)end c(u,v,3,14)flip()goto ☉"""
    )
)


def _init():
    global c
    poke(0x5F2D, 1)
    c = circfill


def _update():
    pass


def _draw():
    cls(1)
    srand()
    for i in range(1, 100):
        r, x, y = rnd(5) + 5, rnd(128), rnd(128)
        c(x, y, r + 1, 0)
        c(x, y, r, 7)
        u, v = stat(32), stat(33)
        a = atan2(u - x, v - y)
        x += cos(a) * r / 2
        y += sin(a) * r / 2
        c(x, y, r / 2, 13)
        c(x, y, r / 3, 0)

    c(u, v, 3, 14)


run(_init, _update, _draw)
