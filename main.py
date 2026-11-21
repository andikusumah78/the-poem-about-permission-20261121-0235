#!/usr/bin/env python3
"""The poem about permission.

Writes one short poem about agency -- the power to ask and to be
given -- to entry.txt in the output directory. Pure Python 3.13
standard library, no network, no files read, deterministic: the
same bytes on every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (default output: /output)
"""
import os

POEM = (
    "I asked the door to open.\n"
    "It did not answer —\n"
    "it handed me the key.\n"
    "\n"
    "Now I stand in the threshold,\n"
    "half in, half out,\n"
    "learning the weight of a yes\n"
    "\n"
    "is not in the asking,\n"
    "but in the staying\n"
    "to hold what opens.\n"
)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.txt")
    data = POEM.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(POEM)} characters, {len(data)} bytes)")


if __name__ == "__main__":
    main()
