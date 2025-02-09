"""256 Followers ported from https://twitter.com/ValerADHD/status/1332080472193687552
"""

from pypico8 import (
    cls,
    circfill,
    pico8_to_python,
    poke,
    print,
    printh,
    pset,
    rnd,
    run,
    t,
)


printh(
    pico8_to_python(
        r"""
poke(0x5f2c,3)n=0r=rnd::_::cls(1)
?"followers: "..n\1,4,16
for i=0,7do
?n>>i&1,44-i*4,28
end
if(n<255)n+=t()n=min(n,255)else n+=t()%.1
if(n>=256.5) goto a
flip()goto _::a::for i=0,999do pset(r(64),r(64),1)end
circfill(r(64),r(64),r(7),r(8)+8)
?"thank you!",12,28,7
flip()goto a
        """
    )
)


def _init():
    global n, r
    poke(0x5F2C, 3)  # Set 64x64 screen size.
    n = 0
    r = rnd


def _update():
    pass


def _draw():
    global n, r
    if n >= 256.5:
        for i in range(0, 999 + 1):
            pset(r(64), r(64), 1)
        circfill(r(64), r(64), r(7), r(8) + 8)
        print("thank you!", 12, 28, 7)
    else:
        cls(1)
        print(f"followers: {int(n // 1)}", 4, 16)
        for i in range(0, 7 + 1):
            print(int(n) >> i & 1, 44 - i * 4, 28)

        if n < 255:
            n += t()
            n = min(n, 255)
        else:
            n += t() % 0.1


run(_init, _update, _draw)
