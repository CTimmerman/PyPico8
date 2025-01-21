"""Bike ported from https://twitter.com/2DArray/status/1358220507074723841
"""

from pypico8 import (
    Table,
    camera,
    circ,
    cls,
    cos,
    line,
    pico8_to_python,
    printh,
    run,
    sin,
    t,
)


printh(
    pico8_to_python(
        """
l={4,0,2,6,8,6,8,7,9,7,7,6,9,0,7,6,4,0,0,0,2,6,1,8,3,8}
::_::
    cls()w=t()/4
    for j=0,2 do
        camera(-38,-74-j)
        for i=1,23,2 do
            a=l[i]*5
            g=-l[i+1]*4
            p=l[i+2]*5
            r=-l[i+3]*4
            line(a,g,p,r,8+j)
            if((i-16)^2==9) circ(a,g,16) for q=w,w+1,.07 do line(a,g,a+sin(q)*15,g+cos(q)*15) end  -- NOTE: if block goes to end of line!
        end
    end
flip()goto _"""
    )
)


def _init():
    global l
    l = Table(
        [4, 0, 2, 6, 8, 6, 8, 7, 9, 7, 7, 6, 9, 0, 7, 6, 4, 0, 0, 0, 2, 6, 1, 8, 3, 8]
    )


def _update():
    pass


def _draw():
    cls()
    w = t() / 4
    for j in range(0, 3):
        camera(-38, -74 - j)
        for i in range(1, 24, 2):
            a = l[i] * 5
            g = -l[i + 1] * 4
            p = l[i + 2] * 5
            r = -l[i + 3] * 4
            line(a, g, p, r, 8 + j)
            if (i - 16) ** 2 == 9:
                circ(a, g, 16)
                q = w
                while q <= w + 1:
                    line(a, g, a + sin(q) * 15, g + cos(q) * 15)
                    q += 0.07


run(_init, _update, _draw)
