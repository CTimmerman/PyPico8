"""Padar ported from https://munro.itch.io/padar
"""
# flake8:noqa
from pypico8 import *


printh(
    pico8_to_python(
        r"""
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
        if(k!=f and k[1]==g and abs(k[2]-p)<1)
            del(q,f)
            o(x,y,7)
            u+=1
        end
    end
?u,-s,58
if(e>0)flip()goto _
        """
    )
)


def _init():
    global s, q, e, u
    s = 63
    q = Table([])
    e = 9
    u = 0
    camera(-s, -s)
    pal([-15, 1, -13, 3, -5, 11, -6], 1)


def _update():
    pass


def _draw():
    global s, q, e, u
    p = btn()
    a = t() / 8
    if rnd() > 0.98:
        add(q, Table([int(rnd(8)) / 8, 50, -0.1]))
    if p > 16:
        q[1] = Table([atan2(p // 8 % 2 - p // 4 % 2, p // 2 % 2 - p % 2), 5, 2, 1])
    for i in range(801):
        f = rnd()
        r = rnd(99)
        x = r * sin(f)
        y = r * cos(f)
        circfill(x, y, 1, abs(pget(x, y) - 1))
    # }
    i = a
    while i <= a + 0.01:
        i += 0.001
        line(0, 0, sin(i) * s, cos(i) * s, 7)
    # }
    for f in all(q):
        g = f[1]
        p = f[2]
        e = min(p, e)
        d = abs(g - a + 0.1) % 1
        x = p * sin(g)
        y = p * cos(g)
        f[2] += f[3]
        if (d < 0.5 and d or 1 - d) < 0.1:
            f[4] = 1
        if f[4]:
            circfill(x, y, 1)
        for k in all(q):
            if k != f and k[1] == g and abs(k[2] - p) < 1:
                delete(q, f)
                circfill(x, y, 7)
                u += 1
            # }
        # }
        print(u, -s, 58)
        if e > 0:
            flip()


run(_init, _update, _draw)