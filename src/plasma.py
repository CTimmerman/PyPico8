"""Plasma ported from https://twitter.com/von_rostock/status/1127600516803059713

printh(
    pico8_to_python(
        r'''
r,o,s,t=128,24,0,{}for i=0,r*r do t[i]=rnd()end
function k(i,j)i/=o
j/=o
p=flr(i)q=flr(j)i-=p
v=(p+r*q)%(#t-r)j-=q
a,c=t[v],t[v+r]a=a+(t[v+1]-a)*i
return a+j*(c+(t[v+r+1]-c)*i-a)end::_::s+=1
for y=s%3,r,3 do
for x=s%4,r,4 do
c=k(x,y+s)*k(x+s,y)pset(x,y,c*8+8)end
end
flip()goto _
    '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import (
    Table,
    flr,
    pset,
    rnd,
    run,
)


def _init() -> None:
    global r, o, s, t2
    r = 128
    o, s = 24, 0
    t2 = Table([])
    for i in range(0, int(r) ** 2 + 1):
        t2[i] = rnd()


def k(i, j):
    i /= o
    j /= o
    p = flr(i)
    q = flr(j)
    i -= p
    v = (p + r * q) % (len(t2) - r)
    j -= q
    a, c = t2[v], t2[v + r]
    a = a + (t2[v + 1] - a) * i
    return a + j * (c + (t2[v + r + 1] - c) * i - a)


def _update() -> None:
    pass


def _draw() -> None:
    global s
    s += 1
    y = s % 3
    while y <= r:
        x = s % 4
        while x <= r:
            c = k(x, y + s) * k(x + s, y)
            pset(x, y, c * 8 + 8)
            x += 4
        y += 3


if __name__ == "__main__":
    run(_init, _update, _draw)
