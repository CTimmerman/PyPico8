r"""Ported from https://x.com/von_rostock/status/1885480371145310636

c=cos::_::cls(3)m=t()r=0g=0h=0p=9+4*c(m)for b=0,1,.02do
pal(b*16,({-15,1,-4,12,6,7})[b*7\1],1)g+=.004+c(b-m)*b/69r+=c(g)h-=sin(g)l=1+b\.96*4for a=0,1,.02-b/99do
u=64+r*c(a)v=p+h+l*sin(a+b\.99/2)
if(a<.5)u=62+c(b-m+a\.17/3)*9*b+a*9v=p+b*99
pset(u,v,pget(u,v)+l)end
end
flip()goto _

>>> run(_draw=_draw)
"""

from pypico8 import *

p = Table([])
x = 64
y = 64
a = 0.0
g = 0.0
h = 0


def _draw() -> None:
    global p, x, y, a, g, h

    print(r"\^1\^c0\^!5f11▒⬇️3⬅️;⌂:♥")
    for k in all(p):
        pset(k[1], k[2], min(pget(k[1], k[2]) + 1 + max(k[3]), 8))
        k[3] -= 1
        k[1] -= k[5]
        k[2] += k[4]

    for _ in range(1, 80 + 1):
        if len(p) > 128 * 8:
            p = p[1:]
            # deli(p, 1)  # Slow!
        u = cos(a) / div / 2
        v = sin(a) / div / 2
        x = int((x + u) % 127)
        y = int((y + v) % 127)
        if rnd() < 0.1:
            g = rnd()
        h -= 1
        if h > 0:
            g = a - 0.6
        a -= (((a - g + 0.5) % 1) - 0.5) / 20
        add(p, Table([x, y, h, u, v]))
        if h <= -30 and pget(x + u * 4, y + v * 4) > 0:
            h = 30


if __name__ == "__main__":
    run(_draw=_draw)
