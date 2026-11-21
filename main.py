#!/usr/bin/env python3
"""Entry for make.fun's news-image-20261121 competition.

Writes the repository's entry.png (a one-image summary of the world news
of Saturday 21 November 2026) to /output/entry.png. Standard library
only, no network, and the same bytes on every run: the image is a fixed
file, composed beforehand by build_image.py.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
# The grader gives the program a writable /output; MAKEFUN_OUTPUT_DIR
# points the same code at a local folder for a manual test run.
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    with open(OUTPUT, "wb") as fh:
        fh.write(data)
    print("wrote", OUTPUT, len(data), "bytes")


if __name__ == "__main__":
    main()
