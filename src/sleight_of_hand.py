"""Sleight of Hand ported from https://twitter.com/MunroHoberman/status/1345134382810619913
"""
from pypico8 import (
    Table,
    add,
    circ,
    cos,
    delete,
    pico8_to_python,
    print,
    printh,
    rectfill,
    rnd,
    run,
    sin,
    t,
)


printh(
    pico8_to_python(
        """
d={}r,e=rectfill,rnd::_::for i=0,999do
circ(e(128),e(128),1)end
for z=1,52do
f=d[z]or add(d,{0,0,z})a=z/52+t()/4x=f[1]y=f[2]f[1]+=(cos(a)*55+60-x)/9f[2]+=(sin(a)*55+57-y)/9r(x,y,x+9,y+14,6)r(x,y,x+8,y+13,7)
?chr(128+f[3]),x+1,y+4,f[3]*8
end
add(d,del(d,e(d)),e(#d)+1)flip()goto _
        """
    )
)


def _init():
    global d, r, e
    d = Table()
    r, e = rectfill, rnd


def _update():
    pass


def _draw():
    for _ in range(0, 1000):
        circ(e(128), e(128), 1)

    for z in range(1, 53):
        f = d[z] or add(d, Table([0, 0, z]))
        a = z / 52 + t() / 4
        x = f[1]
        y = f[2]
        f[1] += (cos(a) * 55 + 60 - x) / 9
        f[2] += (sin(a) * 55 + 57 - y) / 9
        r(x, y, x + 9, y + 14, 6)
        r(x, y, x + 8, y + 13, 7)
        print(chr(128 + f[3]), x + 1, y + 4, f[3] * 8)

    add(d, delete(d, e(d)), e(len(d)) + 1)


run(_init, _update, _draw)