"""Fatal Error ported from https://twitter.com/cbmakes/status/1348119427150188544
TODO: Fix too-bright blue.

cls(13)
poke(0x5f2c,3)
pal(1,140,1)
r=rectfill
k=rect
a=2
c=3
f=40
t=30
::_::
a+=2
c+=2
if(a>60)a=-10
if(c>60)c=rnd(30)-10
k(a-1,c-1,a+f+1,c+t+1,6)
r(a,c,a+f,c+t,6)
k(a,c,a+f,c+t,1)
r(a,c,a+f,c+5,1)
?"- 𝘹",a+28,c,7
?"𝘦𝘳𝘳𝘰𝘳",a+11,c+10,0
r(a+24,c+23,a+36,c+26,5)
flip()
goto _
"""

from pypico8 import cls, pal, poke, print, rect, rectfill, rnd, run


def _init():
    global r, k, a, c, f, t
    cls(13)
    poke(0x5F2C, 3)
    pal(1, 140, 1)
    r = rectfill
    k = rect
    a = 2
    c = 3
    f = 40
    t = 30


def _update():
    pass


def _draw():
    global r, k, a, c, f, t
    a += 2
    c += 2
    if a > 60:
        a = -10
    if c > 60:
        c = rnd(30) - 10
    k(a - 1, c - 1, a + f + 1, c + t + 1, 6)
    r(a, c, a + f, c + t, 6)
    k(a, c, a + f, c + t, 1)
    r(a, c, a + f, c + 5, 1)
    print("- 𝘹", a + 28, c, 7)
    print("𝘦𝘳𝘳𝘰𝘳", a + 11, c + 10, 0)
    r(a + 24, c + 23, a + 36, c + 26, 5)


run(_init, _update, _draw)
