"""Audio functions."""

# pylint:disable = multiple-imports, no-member, unused-argument, wrong-import-position
import os, threading, time  # noqa: E401
from array import array
from collections.abc import MutableSequence, Sequence

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.mixer import Sound, get_init, pre_init

pre_init(44100, -16, 1, 1024)
pygame.init()

audio_channel_notes = [0, 0, 0]
threads: list[threading.Thread] = []


def sfx(n: int, channel: int = -1, offset: int = 0, length: int = 1) -> None:
    """
    play sfx n on channel (0..3) from note offset (0..31) for length notes
    n -1 to stop sound on that channel
    n -2 to release sound on that channel from looping
    Any music playing on the channel will be halted
    offset in number of notes (0..31)

    channel -1 (default) to automatically choose a channel that is not being used
    channel -2 to stop the sound from playing on any channel

    >>> sfx(0)
    >>> sfx(-1)
    """
    if channel == -1:
        chan = pygame.mixer.find_channel()
    else:
        chan = pygame.mixer.Channel(channel)
    note_list = sfx_list[n]
    for note in note_list[offset : offset + length]:
        if chan:
            # chan.play(note)
            # Play note for half a second.
            reps = int(0.1 / note.get_length())
            note.play(reps)
            time.sleep(note.get_length() * reps)


class Note(Sound):  # pylint: disable=too-few-public-methods
    """A musical note. Code from https://gist.github.com/ohsqueezy/6540433"""

    def __init__(self, frequency: int, volume: float = 0.1) -> None:
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self) -> Sequence[int]:
        """Raw wave data."""
        period = int(round(get_init()[0] / self.frequency))
        samples: MutableSequence[int] = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for sample_time in range(period):
            # square wave
            if sample_time < period / 2:
                samples[sample_time] = amplitude
            else:
                samples[sample_time] = -amplitude
        return samples


sfx_list = []
for sfx_i in range(64):
    sfx_notes = []
    for note_i in range(32):
        sfx_notes.append(Note(50 + sfx_i * 4 + note_i * 40))

    sfx_list.append(sfx_notes)


def music(n: int = 0, fade_len: int = 0, channel_mask: int = 0) -> None:
    """
    play music starting from pattern n (0..63)
    n -1 to stop music
    fade_len in ms (default: 0)
    channel_mask specifies which channels to reserve for music only
        e.g. to play on channels 0..2: 1+2+4 = 7

    Reserved channels can still be used to play sound effects on, but only when that
    channel index is explicitly requested by sfx().

    >>> music(0)
    >>> music(-1)
    """
    # global threads
    if n == -1:
        for thread in threads:
            thread.stop = True  # type: ignore[attr-defined]
            thread.join()
        return

    def music_worker() -> None:
        thread = threading.current_thread()
        thread.do_work = threading.Event()  # type: ignore[attr-defined]  # set() and clear() to run and pause.
        thread.do_work.set()  # type: ignore[attr-defined]
        pattern = sfx_list[n]
        while True:
            for note in pattern:
                reps = int(0.1 / note.get_length())
                note.play(reps)
                time.sleep(note.get_length() * reps)
                if getattr(thread, "stop", False):
                    return
                thread.do_work.wait()  # type: ignore[attr-defined]

    thread = threading.Thread(target=music_worker)
    threads.append(thread)
    thread.start()
