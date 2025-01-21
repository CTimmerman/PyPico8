"""Bogosort ported from https://twitter.com/lexaloffle/status/1362393228918493188
"""

from pypico8 import (  # noqa
    Table,
    add,
    cls,
    pico8_to_python,
    printh,
    rectfill,
    rnd,
    run,
    stop,
)


printh(
    pico8_to_python(
        r"""a={} u=1 for i=1,12 do add(a,rnd(80)) end
::_::cls()
f=z for i=1,#a do
if(i<#a and a[i]>a[i+1])f=1
rectfill(i*10,99,8+i*10,99-a[i],7)
end
if(not f)stop("completed")
v=u u=1+rnd(#a)\1 -- random index
a[u],a[v]=a[v],a[u] -- swap
flip()goto _"""
    )
)


def _init():
    global a, u, z
    a = Table([])
    u = 1
    z = 0  # Seems Pico-8 does this instead of complaining about unknown vars.
    for _ in range(1, 6 + 1):
        add(a, rnd(80))


def _update():
    pass


def _draw():
    global a, u, z
    cls()
    unsorted = z
    for i in range(1, len(a) + 1):
        if i < len(a) and a[i] > a[i + 1]:
            unsorted = 1
        rectfill(i * 10, 99, 8 + i * 10, 99 - a[i], 7)

    if not unsorted:
        stop("completed")
    v = u
    u = int(1 + rnd(len(a)))  # random index
    a[u], a[v] = a[v], a[u]  # swap


run(_init, _update, _draw)
