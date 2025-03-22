"""Jiggly Ovals ported from https://twitter.com/picoter8/status/1332575337998397440

-- jiggly ovals #pico8 #tweetcart #tweetjam
::_::
cls()
for i=4,128,6do
c=cos(t()+i/256)
s=sin(t()+i/128)
x=i+i/6*c
y=i+i/6*s
oval(64+2*s-x,64+4*c+i/6-y,64+2*s+x,64+4*c+i/6+y,7)
end
flip()
goto _

>>> run(_draw=_draw)
"""

from pypico8 import cls, cos, oval, run, sin, t


def _draw() -> None:
    cls()
    for i in range(4, 129, 6):
        c = cos(t() + i / 256)
        s = sin(t() + i / 128)
        x = i + i / 6 * c
        y = i + i / 6 * s
        oval(
            64 + 2 * s - x,
            64 + 4 * c + i / 6 - y,
            64 + 2 * s + x,
            64 + 4 * c + i / 6 + y,
            7,
        )


if __name__ == "__main__":
    run(_draw=_draw)
