"""Drippy demo ported from https://www.lexaloffle.com/bbs/?pid=22497#p
2021-01-18 Cees Timmerman added lines.
"""
from pypico8 import line, pget, pico8_to_python, printh, pset, rectfill, rnd, run, stat

printh(
    pico8_to_python(
        r"""
rectfill(0,0,127,127,1)
x=64 y=64 c=8
poke(0x5f2d, 1)

--this is not originally made by
--me, i just added mouse support

--first time using pico-8
--original drippy from demos was
--used to make this with mouse
--support as my first test

--any advie / help would be 
--greatly appreciated. 

function _draw()

--this could probably be much 
--better but i have no clue how
--to move a sprite over without
--erasing whats already there
    for i=0,127 do 
        for j=0,127 do 
  pix = pget(i,j)
  if (pix == 7) then
                pset(i,j,1)
            end
        end
    end

    if (stat(34) == 1) then
     pset(x,y,c)
    end
 spr(0,x+2,y+2)
end

function _update()
 
 x = stat(32)-1
 y = stat(33)-1
 
 c=c+0.1
 if (c >= 16) then c = 8 end

 for i=1,100 do 
  x2 = rnd(128)
  y2 = rnd(128)
  col = pget(x2,y2)
  if (col~=1) then
   pset(x2,y2+1,col) 
  end
 end
end
"""
    )
)


def _init():
    global x, y, c
    rectfill(0, 0, 127, 127, 1)
    x = 64
    y = 64
    c = 8


def _draw():
    global last_mouse_buttons
    # hide cursor?
    for i in range(0, 127 + 1):
        for j in range(0, 127 + 1):
            pix = pget(i, j)
            if pix == 7:
                pset(i, j, 1)
    # draw
    mouse_buttons = stat(34)
    if mouse_buttons & 1:
        if last_mouse_buttons & 1:
            line(x, y, col=c)
        else:
            line(x, y, x, y, c)
    
    last_mouse_buttons = mouse_buttons

    # spr(48, x + 2, y + 2)  # Where do they get their fancy sprites and how do they barely leave a trail?


def _update():
    global x, y, c
    x = stat(32)
    y = stat(33)

    c = c + 0.1
    if c >= 16:
        c = 8
    
    # drip
    for i in range(1, 100 + 1):
        x2 = rnd(128)
        y2 = rnd(128)
        col = pget(x2, y2)
        if col != 1:
            pset(x2, y2 + 1, col)


run(_init, _update, _draw)