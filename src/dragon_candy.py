"""Dragon Candy ported from https://twitter.com/MunroHoberman/status/1346166185595985920

printh(
    pico8_to_python(
        '''
        camera(-64,-64)q={}for i=0,11do
        add(q,1/4)for i=#q-1,1,-1do
        add(q,-q[i])end
        end::_::c=t()*8for i=0,999do
        j=rnd(128)-64k=rnd(128)-64v=-sqrt(j*j+k*k)pset(j+j/v+k/v,k+k/v-j/v,pget(j,k))end
        x=0y=0a=c/64for i=1,#q do
        a+=q[i]x+=cos(a)y+=sin(a)circ(x,y,1,c%9+7)
        if(i&i-1<1)c+=1end
        '''
    )
)

>>> run(_init, _draw=_draw)
"""

from pypico8 import (
    add,
    camera,
    circ,
    cos,
    pget,
    pset,
    rnd,
    run,
    sin,
    sqrt,
    t,
    Table,
)


def _init() -> None:
    global q
    camera(-64, -64)
    q = Table()
    for i in range(0, 12):
        add(q, 1 / 4)
        for i in range(len(q) - 1, 1, -1):
            add(q, -q[i])


def _draw() -> None:
    global q
    c = t() * 8
    for i in range(0, 1000):
        j = rnd(128) - 64
        k = rnd(128) - 64
        v = -sqrt(j * j + k * k)
        pset(j + j / v + k / v, k + k / v - j / v, pget(j, k))

    x = 0.0
    y = 0.0
    a = c / 64
    for i in range(1, len(q) + 1):
        a += q[i]
        x += cos(a)
        y += sin(a)
        circ(x, y, 1, c % 9 + 7)
        if i & i - 1 < 1:
            c += 1


if __name__ == "__main__":
    run(_init, _draw=_draw)
