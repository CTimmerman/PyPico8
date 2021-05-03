"""3D Helix ported from https://twitter.com/p01/status/1009386060214874112
"""
from pypico8 import *


printh(
    pico8_to_python(
        r"""
r="3d helix ★ p01"cls()s=sin
?r
memcpy(0,24568,999)::_::cls()for y=0,138 do
i=(t()*8+y/8)%114u=y/399-t()/7w=(27+9*s(u))*s(u)a=abs(w/16)for z=0,6 do
if(z*sgn(w)>5) a=11+w/9
pal(6,a+rnd())sspr(flr(i/6)*4,i%6,3,1,64+(16+z*6)*s(u-.25)-w,y-z,w*2,1)
end
end
?r,34,50,7
flip()goto _
        """
    )
)


def _init():
    global r, s
    r = "3D HELIX ★ P01"
    cls()
    s = sin
    print(r)
    memcpy(0, 0x6000-8, 999)  # screen to spritesheet


def _update():
    pass


def _draw():
    cls()
    for y in range(0, 138 + 1):
        i = (t() * 8 + y / 8) % 114
        u = y / 399 - t() / 7
        w = (27 + 9 * s(u)) * s(u)
        a = abs(w / 16)
        for z in range(0, 6 + 1):
            if z * sgn(w) > 5:
                a = 11 + w / 9
            pal(6, a + rnd())
            sspr(
                flr(i / 6) * 4,
                i % 6,
                3,
                1,
                64 + (16 + z * 6) * s(u - 0.25) - w,
                y - z,
                w * 2,
                1,
            )
    print(r, 34, 50, 7)


run(_init, _update, _draw)