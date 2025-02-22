"""Mandala 2 ported from https://twitter.com/MunroHoberman/status/1339983792090570753
"""

# fmt: off
from pypico8 import Table, circ, pal, poke, printh, pico8_to_python, cos, sin, t, run
# fmt: on

printh(
    pico8_to_python(
        r"""
pal({-15,1,-13,-4,12},1)poke(24364,7)::_::for z=0,7do
for i=0,1,.1do
a=t()/8+i+z*.005l=cos(a/2)*60circ(cos(a)*l+63,sin(a)*l+63,abs(l),z)end
end
flip()goto _
        """
    )
)


def _init():
    pal(Table([-15, 1, -13, -4, 12]), 1)
    poke(24364, 7)


def _update():
    pass


def _draw():
    for z in range(0, 7 + 1):
        i = 0
        while i <= 1:
            a = t() / 8 + i + z * 0.005
            L = cos(a / 2) * 60
            circ(cos(a) * L + 63, sin(a) * L + 63, abs(L), z)
            i += 0.1


if __name__ == "__main__":
    run(_init, _update, _draw)
