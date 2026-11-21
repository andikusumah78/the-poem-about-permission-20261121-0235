#!/usr/bin/env python3
"""The poem about permission.

Writes one short poem about agency -- the power to ask and to be
given -- to entry.txt in the output directory. Pure Python 3.13
standard library, no network, no files read, deterministic: the
same bytes on every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (default output: /output)
"""
import os
import sys
import tempfile

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


def validate_output(text):
    """Self-check the poem before writing it.

    Rules: 1-280 Unicode code points, valid UTF-8, not
    whitespace-only. Raises ValueError with a clear message
    when a rule is violated.
    """
    if not 1 <= len(text) <= 280:
        raise ValueError(
            f"poem must be 1-280 Unicode code points, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("poem must not be whitespace-only")
    # Round-trip through UTF-8 to prove the text is valid UTF-8.
    text.encode("utf-8").decode("utf-8")


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        validate_output(POEM)
    except ValueError as exc:
        print(f"error: invalid poem output: {exc}", file=sys.stderr)
        raise SystemExit(1)
    data = POEM.encode("utf-8")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.txt")
    # Write atomically: temp file in the same directory, then replace,
    # so a failed run never leaves a partial entry.txt behind.
    fd, tmp_path = tempfile.mkstemp(dir=outdir, prefix=".entry.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    print(f"wrote {path} ({len(POEM)} characters, {len(data)} bytes)")


if __name__ == "__main__":
    main()
