"""Octopus ported from https://twitter.com/picoter8/status/1330759076943376384
-- octopus #pico8 #tweetcart #tweetjam
::_::cls()
for r=16,128,6do
for a=0,1,1/r do
b=a+.1*(1-r/96)*sin(.8*t()+r/96)
x=62+(r+8*sin(t()/5))*cos(b)
y=62+(r+8*sin(t()/5))*sin(b)
q=3*sin(a*8-t()/5)
circfill(x,y,q+2,2)circfill(x,y,q,1)
end
end
flip()goto _

Purple/blue tentacles in the dark.
>>> run(_draw=_draw)
"""

from pypico8 import circfill, cls, cos, run, sin, t


def _draw() -> None:
    cls()
    for r in range(16, 129, 6):
        a = 0.0
        while a < 1:
            a += 1 / r
            b = a + 0.1 * (1 - r / 96) * sin(0.8 * t() + r / 96)
            x = 62 + (r + 8 * sin(t() / 5)) * cos(b)
            y = 62 + (r + 8 * sin(t() / 5)) * sin(b)
            q = 3 * sin(a * 8 - t() / 5)
            circfill(x, y, q + 2, 2)
            circfill(x, y, q, 1)


if __name__ == "__main__":
    run(_draw=_draw)
