"""Amorphous Form ported from https://twitter.com/szczm_/status/1125041539498106881

printh(
    pico8_to_python(
        r'''
fillp(7^5)
a,e=cos,sin
::_::
    d=a(.12)
    camera(-64,-64)
    cls()
    m=.01+3/8*(1+a(t()/8))^2
    for g=.5,0,-.04 do
        f=-d*a(g)
        h=-e(g-m)
        for i=0,1,m do
            b=50+e(i+t())
            line(b*h*a(i),b*(f+h*d*e(i)),b*h*a(i+m),b*(f+h*d*e(i+m)),"0x"..sub("776d11",g*9,g*9+2))
        end
    end
flip()
goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

# fmt: off
from pypico8 import fillp, cos, sin, camera, cls, t, line, sub, run
# fmt: on


def _init() -> None:
    global a, e

    fillp(7**5)
    a, e = cos, sin


def _update() -> None:
    pass


def _draw() -> None:
    d = a(0.12)
    camera(-64, -64)
    cls()
    m = 0.01 + 3 / 8 * (1 + a(t() / 8)) ** 2
    g = 0.5
    while g >= 0:  # bands
        f = -d * a(g)
        h = -e(g - m)
        i = 0
        while i <= 1:  # band wrap ratio
            b = 50 + e(i + t())
            line(
                b * h * a(i),
                b * (f + h * d * e(i)),
                b * h * a(i + m),
                b * (f + h * d * e(i + m)),
                "0x" + sub("776d11", g * 9, g * 9 + 2),
            )
            i += m
        g += -0.04


if __name__ == "__main__":
    run(_init, _update, _draw)
