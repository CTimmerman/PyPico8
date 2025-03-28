"""Code Golf ported from https://twitter.com/MBoffin/status/1346539275131580417

printh(
    pico8_to_python(
        '''s=sin c=cos d=circfill b=64 r=128
m={}for i=0,b do m[i]=rnd()end
::_::cls(1)a=t()for i=0,b do x,y=(m[i]*r-a*b)%r,(m[b-i]*r-a*b)%r
line(x,y,x-2,y-2,6)d(i+c(a+i/b+.2)*8,i+s(a+.2)*8,4-32/i,i%2==0and 12or 7)d(i+c(a+i/b)*8,i+s(a)*8,4-32/i,i%2==0and 10or 7)
end flip()goto _'''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import Table, circfill, cls, cos, div, line, rnd, run, sin, t


def _init() -> None:
    global s, c, d, b, r, m
    s = sin
    c = cos
    d = circfill
    b = 64
    r = 128
    m = Table([])

    for i in range(
        0, int(b) + 1
    ):  # Without int() here, mypy 1.15.0 sees b as Table. :(
        m[i] = rnd()


def _update() -> None:
    pass


def _draw() -> None:
    cls(1)
    a = t()
    for i in range(
        0, b + 1
    ):  # Dividing by zero evaluates to 0x7fff.ffff if positive, or -0x7fff.ffff if negative. (-32768.0 to 32767.99999)
        x, y = (m[i] * r - a * b) % r, (m[b - i] * r - a * b) % r
        line(x, y, x - 2, y - 2, 6)
        d(
            i + c(a + i / b + 0.2) * 8,
            i + s(a + 0.2) * 8,
            4 - div(32, i),
            i % 2 == 0 and 12 or 7,
        )
        d(i + c(a + i / b) * 8, i + s(a) * 8, 4 - div(32, i), i % 2 == 0 and 10 or 7)


if __name__ == "__main__":
    run(_init, _update, _draw)
