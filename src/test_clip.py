"""https://pico-8.fandom.com/wiki/Clip
Should show two whole white and half red circles at top and bottom of the screen."""

from pypico8 import circfill, clip, peek, printh, run


def _init():
    """ """
    # set the clipping region to exclude 8 pixels at the top and bottom
    clip(0, 8, 128, 112)

    # these circles are clipped to (0-127,8-119)
    circfill(10, 10, 8, 8)
    circfill(10, 118, 8, 8)

    # reset the clipping region to full screen
    clip()

    # these circles are not clipped
    circfill(40, 10, 8, 7)
    circfill(40, 118, 8, 7)

    # get the current clip rectangle from its memory-mapped addresses
    clip_x = peek(0x5F20)
    clip_y = peek(0x5F21)
    clip_w = peek(0x5F22) - clip_x
    clip_h = peek(0x5F23) - clip_y
    printh(str(clip_x) + " " + str(clip_y) + " " + str(clip_w) + " " + str(clip_h))


def _update():
    pass


def _draw():
    pass


if __name__ == "__main__":
    run(_init, _update, _draw)
