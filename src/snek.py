"""Snek ported from https://twitter.com/2DArray/status/1354223916013793284
"""
from pypico8 import Table, circfill, cls, pal, pico8_to_python, printh, run, sin, t


printh(
    pico8_to_python(
        """
for i=1,6 do
    pal(i-1,({143,132,136,137,9,15})[i],1)
end
::_::
cls()
for i=0,4 do
    for y=1.3,0,-.02 do
        r=4
        if(y<.1)r+=3-abs(y-.07)*50
        if(y>.7)r*=1-(y-.7)/.3
        w=y*4+1.5
        x=sin(y*2-t())*w
        circfill(64.5+x+i/2,28+y*90,r-i,1+i)
    end
end
flip()goto _"""
    )
)


def _init():
    for i in range(1, 6 + 1):
        pal(i - 1, (Table([143, 132, 136, 137, 9, 15]))[i], 1)


def _update():
    pass


def _draw():
    cls()
    for i in range(0, 5):
        y = 1.3
        while y >= 0:
            r = 4
            if y < 0.1:
                r += 3 - abs(y - 0.07) * 50
            if y > 0.7:
                r *= 1 - (y - 0.7) / 0.3
            w = y * 4 + 1.5
            x = sin(y * 2 - t()) * w
            circfill(64.5 + x + i / 2, 28 + y * 90, r - i + 1, 1 + i)
            y += -0.02


run(_init, _update, _draw)