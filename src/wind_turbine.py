"""Wind Turbine ported from https://twitter.com/DrewesThorsten/status/1352677414250426369
"""

from pypico8 import (
    Table,
    circfill,
    cls,
    cos,
    flr,
    line,
    pico8_to_python,
    rectfill,
    run,
    sin,
    t,
)


print(
    pico8_to_python(
        r"""k={7,11,3}s,c,l=sin,cos,line::_::cls(12)for i=1,80 do
o=c(i/225)*2p=max(flr(-o*3,0))+1l(64+o,i+50,64-o+5,i+50,k[p])end
for i=0,2 do
d=i/3+t()/9
for j=-.1,.1,.01 do
l(66+s(d+j)*3,50+c(d+j)*3,s(d)*40+66,c(d)*40+50,7)end
end
circfill(66,50,3,6)rectfill(0,125,127,127,11)flip()goto _"""
    )
)


def _init():
    global k, s, c, L
    k = Table([7, 11, 3])
    s, c, L = sin, cos, line


def _update():
    pass


def _draw():
    cls(12)
    for i in range(1, 80 + 1):
        o = c(i / 225) * 2
        p = max(flr(-o * 3), 0) + 1
        L(64 + o, i + 50, 64 - o + 5, i + 50, k[p])

    for i in range(0, 2 + 1):
        d = i / 3 + t() / 9
        j = -0.1
        while j <= 0.1:
            j += 0.01
            L(66 + s(d + j) * 3, 50 + c(d + j) * 3, s(d) * 40 + 66, c(d) * 40 + 50, 7)

    circfill(66, 50, 3, 6)
    rectfill(0, 125, 127, 127, 11)


if __name__ == "__main__":
    run(_init, _update, _draw)
