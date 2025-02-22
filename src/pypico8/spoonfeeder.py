"""Spoonfeed, by Cees Timmerman, 2025-02-18.

Usage: python spoonfeeder.py "doctest" "file1" "file2" etc.

Because pre-commit only does multiple file arguments,
doctest only does a single file argument,
and CLI scripts and tools vary."""

import subprocess
import sys


def spoonfeed(args):
    print(f"Spoonfeeding {args}")
    for arg in args[2:]:
        done = subprocess.run(
            [*args[1].split(" "), arg],
            check=True,  # Raise exception if nonzero returncode.
            shell=True,
        )
        print(f"Done {arg}: {done}")


if __name__ == "__main__":
    spoonfeed(sys.argv)
    print("Done all.")
