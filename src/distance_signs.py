"""Distance Signs ported from https://x.com/MunroHoberman/status/1365000731284041732

printh(
    pico8_to_python(
        r'''
function s(n)
    return mid(1,(n-.3)/0)
end
pal({-16,-14,-11,-3,13},1)
::_::
    r=t()/8
    x=rnd(128)
    y=rnd(128)
    e=x/128-cos(r)/4-.5
    f=y/128-sin(r)/4-.5
    j=cos(r)*e-sin(r)*f/2+.5
    k=sin(r)*e/2+cos(r)*f+.5
    n=s(j)
    m=s(k)
    n*=s(1-j)
    m*=s(1-k)
    c=abs(pget(x,y)-1)
    circ(x,y,1,min(7,n*m*2+c))
    goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import (  # noqa
    Table,
    circ,
    cos,
    div,
    mid,
    pal,
    pget,
    rnd,
    run,
    sin,
    t,
)


def _init() -> None:
    pal(Table([-16, -14, -11, -3, 13]), 1)


def s(n):
    return mid(1, div((n - 0.3), 0))


def _update() -> None:
    pass


def _draw() -> None:
    for _ in range(1000):
        r = t() / 8
        x = rnd(128)
        y = rnd(128)
        e = x / 128 - cos(r) / 4 - 0.5
        f = y / 128 - sin(r) / 4 - 0.5
        j = cos(r) * e - sin(r) * f / 2 + 0.5
        k = sin(r) * e / 2 + cos(r) * f + 0.5
        n = s(j)
        m = s(k)
        n *= s(1 - j)
        m *= s(1 - k)
        c = abs(pget(x, y) - 1)
        circ(x % 128, y % 128, 1, min(7, n * m * 2 + c))


if __name__ == "__main__":
    run(_init, _update, _draw)
