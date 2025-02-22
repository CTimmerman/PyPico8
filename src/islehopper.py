"""Islehopper ported from https://twitter.com/ValerADHD/status/1325129814454439936
"""

from pypico8 import (
    atan2,
    btn,
    circfill,
    cls,
    cos,
    line,
    pal,
    pico8_to_python,
    printh,
    memcpy,
    sget,
    sin,
    rnd,
    run,
    t,
)


printh(
    pico8_to_python(
        r"""
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
        """
    )
)


def _init():
    global _, x, q, y, u, d, z, w, e
    pal(([1, 15, 143, 138, 11, 139, 3, 131, 132, 5, 6, 7, 7, 7, 12]), 1)
    cls()
    _ = 127
    x = 32
    q = cos
    y = 32
    u = sin
    d = 0
    z = 8
    w = 64
    e = 64
    for i in range(0, 30 + 1):
        a = rnd(_)
        b = rnd(_)
        r = rnd(9)
        for i in range(1, 9 + 1):
            circfill(a, b, r, i)
            r = round(r - rnd(4), 4)
        # }
    # }
    memcpy(0, 6 << 12, 8192)


def _update():
    pass


def _draw():
    global _, n, x, q, y, u, d, z, w, e
    cls(14)
    for i in range(0, _ + 1):
        a = x
        b = y
        r = d + (i / 256) - 0.25
        p = _
        for j in range(1, 24 + 1):
            a = round(a + q(r), 4)
            b = round(b + u(r), 4)
            h = sget(int(a) & _, int(b) & _)
            s = sin(t() / 8) * 4 + 64 - (h - z) * 64 / j
            if s < p:
                line(i, p, i, s, h)
                p = s
        # }
    # }
    b = btn()
    w += b // 2 % 2 - b % 2
    e += b // 8 % 2 - b // 4 % 2
    x = round(x + q(d) / 4, 4)
    y = round(y + u(d) / 8, 4)
    r = round(r + atan2(w - 64, e - _) - 0.25, 4)
    m = t()
    for f in range(e, e + 2 + 1):
        j = u(m) / 16
        line(w + q(r - j) * 16, e + u(r - j) * 16, w, f, 13)
        line(w + q(r + 0.5 + j) * 16, e + u(r + 0.5 + j) * 16)
    # }
    d = round(d + (w - 64) / _ / _ * 4, 4)


if __name__ == "__main__":
    run(_init, _update, _draw)
