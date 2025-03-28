r"""Padar ported from https://munro.itch.io/padar
Aim with arrow keys and fire with action keys (Z/X/C) before you get hit.

printh(
    pico8_to_python(
        r'''
s=63
q={}
e=9
u=0
camera(-s,-s)
pal({[0]=-15,1,-13,3,-5,11,-6},1)
o,j,h=circfill,cos,sin
::_::
p=btn()
a=t()/8
if(rnd()>.98)add(q,{rnd(8)\1/8,50,-.1})
if(p>16)q[1]={atan2(p\8%2-p\4%2,p\2%2-p%2),5,2,1}
for i=0,800do
    f=rnd()
    r=rnd(99)
    x=r*h(f)
    y=r*j(f)
    o(x,y,1,abs(pget(x,y)-1))
end
for i=a,a+.01,.001do
    line(0,0,h(i)*s,j(i)*s,7)
end
for f in all(q)do
    g=f[1]
    p=f[2]
    e=min(p,e)
    d=abs(g-a+.1)%1
    x=p*h(g)
    y=p*j(g)
    f[2]+=f[3]
    if((d<.5and d or 1-d)<.1) f[4]=1
    if(f[4]) o(x,y,1)
    for k in all(q)do
        if(k!=f and k[1]==g and abs(k[2]-p)<1) del(q,f) o(x,y,7) u+=1
    end
end
?u,-s,58
if(e>0)flip()goto _
        '''
    )
)

>>> run(_init, _update60, _draw)
"""

# flake8:noqa
from pypico8 import *


def _init() -> None:
    global size, entities, e, score
    size = 63
    entities = Table([])
    e = 9
    score = 0
    camera(-size, -size)
    pal([-15, 1, -13, 3, -5, 11, -6], 1)


def _update60() -> None:
    pass


def _draw() -> None:
    global size, entities, e, score
    pressed = btn()
    speed = t() / 8
    if rnd() > 0.98:
        add(entities, Table([rnd(8) // 1 / 8, 50, -0.1]))
    if pressed > 16:
        entities[1] = Table(
            [
                atan2(
                    pressed // 8 % 2 - pressed // 4 % 2, pressed // 2 % 2 - pressed % 2
                ),
                5,
                2,
                1,
            ]
        )
    for _ in range(801):
        fr = rnd()
        r = rnd(99)
        x = r * sin(fr)
        y = r * cos(fr)
        circfill(x, y, 1, abs(pget(x, y) - 1))

    j = speed
    while j <= speed + 0.01:
        line(0, 0, sin(j) * size, cos(j) * size, 7)
        j = round(j + 0.001, 4)

    for f in all(entities):
        g = f[1]
        pressed = f[2]
        e = min(pressed, e)
        distance = abs(g - speed + 0.1) % 1
        x = pressed * sin(g)
        y = pressed * cos(g)
        f[2] += f[3]
        if (distance < 0.5 and distance or 1 - distance) < 0.1:
            f[4] = 1  # detected
        if f[4]:
            circfill(x, y, 1)  # entity
        for k in all(entities):
            if k != f and k[1] == g and abs(k[2] - pressed) < 1:
                delv(entities, f)
                circfill(x, y, 7)
                score += 1

    print(score, -size, 58)
    if e <= 0:
        stop()


if __name__ == "__main__":
    run(_init, _update60, _draw)
