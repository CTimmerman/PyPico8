"""Assembled Horizon ported from https://x.com/MunroHoberman/status/1385388186801745921

printh(
    pico8_to_python(
        r'''
z=64
q={}
pal({1,2,-8,8,-7,9,10,7,-9,-6,11,-5,3,-13,1,-15},1)
for i=1,4^6do
    add(q,i%16,rnd(#q)+1)
end
cls()
for i=1,4^6do
    pset(i%z*2,i/z\1*2,q[i])
end
::_::
for i=2,#q do
    while(i>1and q[i]<q[i-1])
    e=i-1
    f=i-2
    q[i],q[e]=q[e],q[i]
    pset(e%z*2,e/z\1*2,q[i])
    pset(f%z*2,f/z\1*2,q[e])
    i-=1
end
goto _
    '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    global size, q

    size = 32
    q = Table()  # type: ignore  # "int is not callable", mypy?!
    pal(Table([1, 2, -8, 8, -7, 9, 10, 7, -9, -6, 11, -5, 3, -13, 1, -15]), 1)
    for i in range(1, size**2 + 1):
        add(q, i % 16, rnd(q.len()) + 1)

    cls()
    for i in range(1, size**2 + 1):
        pset(i % size * 2, 20 + i / div / size / divi / 1 * 2, q[i])


def _update() -> None:
    pass


def _draw() -> None:
    global size, q
    for i in range(2, q.len() + 1):
        # Sort next block.
        while i > 1 and q[i] < q[i - 1]:
            e = i - 1
            f = i - 2
            q[i], q[e] = q[e], q[i]
            pset(e % size * 2, 20 + e / div / size / divi / 1 * 2, q[i])
            pset(f % size * 2, 20 + f / div / size / divi / 1 * 2, q[e])
            i -= 1


if __name__ == "__main__":
    run(_init, _update, _draw)
