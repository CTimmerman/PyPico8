"""Snek ported from https://twitter.com/2DArray/status/1354223916013793284

printh(
    pico8_to_python(
        '''
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
flip()goto _'''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import Table, circfill, cls, pal, run, sin, t


def _init() -> None:
    for i in range(1, 6 + 1):
        pal(i - 1, (Table([143, 132, 136, 137, 9, 15]))[i], 1)


def _update() -> None:
    pass


def _draw() -> None:
    cls()
    for i in range(0, 5):
        y = 1.3
        while y >= 0:
            r = 4.0
            if y < 0.1:
                r += 3 - abs(y - 0.07) * 50
            if y > 0.7:
                r *= 1 - (y - 0.7) / 0.3
            w = y * 4 + 1.5
            x = sin(y * 2 - t()) * w
            circfill(64.5 + x + i / 2, 28 + y * 90, r - i + 1, 1 + i)
            y += -0.02


if __name__ == "__main__":
    run(_init, _update, _draw)
