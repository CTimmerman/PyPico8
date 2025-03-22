r"""Islehopper ported from https://twitter.com/ValerADHD/status/1325129814454439936

printh(
    pico8_to_python(
        r'''
pal({[0]=1,15,143,138,11,139,3,131,132,5,6,7,7,7,12},1)
cls()
_=127
n=rnd
x=32
q=cos
y=32
u=sin
d=0
z=8
w=64
e=64
l=line
for i=0,30do
    a=n(_)
    b=n(_)
    r=n(9)
    for i=1,9do
        circfill(a,b,r,i)
        r-=n(4)
    end
end
memcpy(0,6<<12,8192)
::_::
cls(14)
for i=0,_ do
    a=x
    b=y
    r=d+(i/256)-.25p=_
    for j=1,24do
        a+=q(r)
        b+=u(r)
        h=sget(a&_,b&_)
        s=sin(t()/8)*4+64-(h-z)*64/j
        if(s<p)l(i,p,i,s,h)p=s
    end
end
b=btn()
w+=b\2%2-b%2
e+=b\8%2-b\4%2
x+=q(d)/4
y+=u(d)/8
r=atan2(w-64,e-_)-.25
m=t()
for f=e,e+2do
    j=u(m)/16
    l(w+q(r-j)*16,e+u(r-j)*16,w,f,13)
    l(w+q(r+.5+j)*16,e+u(r+.5+j)*16)
end
d+=(w-64)/_/_*4
flip()goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    global _, x, y, d, z, w, e
    pal(([1, 15, 143, 138, 11, 139, 3, 131, 132, 5, 6, 7, 7, 7, 12]), 1)
    cls()
    # map size
    _ = 127
    # position
    x = 32
    y = 32
    d = 0  # direction
    z = 8  # bird altitude
    w = 64  # bird x
    e = 64  # bird y
    for i in range(0, 30 + 1):
        # random place
        a = rnd(_)
        b = rnd(_)
        # random height
        r = rnd(9)
        for i in range(1, 9 + 1):
            circfill(a, b, r, i)
            r = round4(r - rnd(4))
    memcpy(0, 24576, 8192)  # screen data to sprite sheet


def _update() -> None:
    pass


def _draw() -> None:
    global _, n, x, y, d, z, w, e
    cls(14)
    for i in range(0, _ + 1):
        a = x
        b = y
        r = round4(d + (i / 256) - 0.25)
        p = _
        for j in range(1, 24 + 1):
            a = round4(a + cos(r))
            b = round4(b + sin(r))
            h = sget(flr(a) & _, flr(b) & _)
            s = sin(t() / 8) * 4 + 64 - (h - z) * 64 / j
            if s < p:
                line(i, p, i, s, h)
                p = s
    b = btn()
    w += b // 2 % 2 - b % 2
    e += b // 8 % 2 - b // 4 % 2
    x = round4(x + cos(d) / 4)
    y = round4(y + sin(d) / 8)
    # rotation
    r = round4((atan2(w - 64, e - _) - 0.25))
    m = t()
    for f in range(e, e + 2 + 1):
        j2 = sin(m) / 16
        line(w + cos(r - j2) * 16, e + sin(r - j2) * 16, w, f, 13)
        line(w + cos(r + 0.5 + j2) * 16, e + sin(r + 0.5 + j2) * 16)
    # }
    d = round4(d + (w - 64) / _ / _ * 4)


if __name__ == "__main__":
    run(_init, _update, _draw)
