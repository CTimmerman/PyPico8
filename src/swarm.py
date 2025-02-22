"""Swarm ported from https://twitter.com/MunroHoberman/status/1358777612206821376
"""

from pypico8 import (
    Table,
    add,
    all,
    atan2,
    circfill,
    cls,
    cos,
    pico8_to_python,
    poke,
    printh,
    pget,
    pset,
    rnd,
    run,
    sgn,
    sin,
    stat,
)


printh(
    pico8_to_python(
        r"""w=pset
q={}poke(24365,1)cls()circfill(63,63,63,9)::_::j=stat(32)k=stat(33)q[1]={x=j,y=k,a=0}for f in all(q)do
w(f.x,f.y,0)f.a+=.01*sgn((f.a-atan2(j-f.x,k-f.y))%1-.5)f.x+=cos(f.a)f.y+=sin(f.a)if(pget(f.x,f.y)>8 and rnd()>.9)add(q,{x=f.x,y=f.y,a=rnd()})
w(f.x,f.y,7)end
flip()goto _"""
    )
)


def _init():
    global w, q
    w = pset
    q = Table([])
    poke(24365, 1)
    cls()
    circfill(63, 63, 63, 9)


def _update():
    pass


def _draw():
    global w, q
    j = stat(32)
    k = stat(33)
    q[1] = Table(x=j, y=k, a=0)
    for f in all(q):
        w(f.x, f.y, 0)
        f.a += 0.01 * sgn((f.a - atan2(j - f.x, k - f.y)) % 1 - 0.5)
        f.x += cos(f.a)
        f.y += sin(f.a)
        if pget(f.x, f.y) > 8 and rnd() > 0.9:
            add(q, Table(x=f.x, y=f.y, a=rnd()))
        w(f.x, f.y, 7)


if __name__ == "__main__":
    run(_init, _update, _draw)
