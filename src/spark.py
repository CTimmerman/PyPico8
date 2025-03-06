r"""Spark ported from https://x.com/von_rostock/status/1854655683381109129
r=rnd
::_::
?"\^!5f11▒1😐<7"
b=r()<cos(r())
u=0
v=0
g=r()
for d=0,1,.0004do
    a=r()
    x=64+d*33*sin(a)
    y=64+d*33*cos(a)
    c=d^8*(2+r(2))+.2\d
    e=pget(x,y)
    if(e>c)c=e-1
    pset(x,y,c)
    d=(u*u+v*v)>>10
    if(b and d<1) then
        u+=sin(g)/3
        v+=cos(g)/3
        g+=r(-1)>>(20.5-d)
        pset(u+64,v+64,(pget(u+64,v+64)+1+d)&7)
    end
end
goto _
"""

from pypico8 import *


def _draw():
    print(r"\^!5f11▒1😐<7")
    b = rnd() < cos(rnd())
    u = 0
    v = 0
    g = rnd()
    d = 0
    while 1:
        a = rnd()
        x = 64 + d * 33 * sin(a)
        y = 64 + d * 33 * cos(a)
        c = d**8 * (2 + rnd(2)) + divi(0.2, d)
        e = pget(x, y)
        if e > c:
            c = e - 1
        pset(x, y, c)  # clean up
        d = max(d, shr(u * u + v * v, 10))  # limit to circle
        if b and d < 1:
            # spark
            u = round4(u + sin(g) / 3)
            v = round4(v + cos(g) / 3)
            g = round4(g + shr(rnd(-1), (20.5 - d)))  # angle
            pset(u + 64, v + 64, (pget(u + 64, v + 64) + 1 + flr(d)) & 7)

        if d >= 1:
            break
        d = round4(d + 0.0004)


if __name__ == "__main__":
    run(_draw=_draw)
