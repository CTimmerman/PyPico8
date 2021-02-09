"""Fake Sprite ported from https://twitter.com/YerisTR/status/1228768088277094400
and https://twitter.com/MunroHoberman/status/1228829417499189248
"""
import pypico8
from pypico8 import (
    Table,
    circfill,
    cls,
    flr,
    memcpy,
    pal,
    pico8_to_python,
    print,
    printh,
    run,
    sget,
    sin,
    sspr,
    t,
)


printh(
    pico8_to_python(
        r"""cls()
?"nice\ntutorial"
memcpy(0,0x6000,2048)c=4
d=6
::_::cls()scale=sin(t()/9)+2
for i=1,8 do
pal(6,15-i)for x=0,64 do
for y=0,20 do 
if(sget(x,y)>0)sspr(flr(x/c)*c,flr(y/d)*d,4,5,x*c*scale,y*d*scale+i*scale,c*scale,d*scale)end
end
end
flip()goto _"""
    )
)


def _init():
    global c, d, size, p
    cls()
    print("NICE\nTUTORIAL")
    memcpy(0, 0x6000, 2048)  # copy screen to spritesheet.
    c = 4
    d = 6
    size = 5
    p = Table([1, 2, 8, 14, 15])


def _update():
    pass


def fake_sprite():
    for y in range(0, 5):
        for x in range(0, 25):
            col = sget(x, y)
            if col > 0:
                xt = 30 + x * (size) + sin(t() + y / 10) * 3
                yt = 85 + y * size
                circfill(xt, yt, size - 1, p[y + 1])


def _draw():
    """Rainbow zoom."""
    cls()
    pypico8.surf.blit(pypico8.spritesheet, (0, 0))
    scale = sin(t() / 9) + 2
    # rainbow
    for i in range(1, 8 + 1):
        pal(6, 15 - i)
        # zoomed text
        for x in range(0, 64 + 1):
            for y in range(0, 20 + 1):
                if sget(x, y) > 0:
                    sspr(
                        flr(x / c) * c,
                        flr(y / d) * d,
                        4,
                        5,
                        x * c * scale,
                        y * d * scale + i * scale,
                        c * scale,
                        d * scale,
                    )
    
    fake_sprite()


run(_init, _update, _draw)
