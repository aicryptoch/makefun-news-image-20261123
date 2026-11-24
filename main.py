#!/usr/bin/env python3
"""THE FRONT PAGE — akun19 entry program for news-image-20261123.

The picture beside this file is a straight newspaper front page for
Monday 23 November 2026, led by the US Army plan to detonate unstable
explosives in Iowa. This program does one small job: it copies that
picture, entry.png, into the output directory exactly as it stands.

Standard library only (hashlib, os, sys). No image library is used and
nothing is redrawn, so two runs always produce identical bytes.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 299037
EXPECTED_SHA256 = "57b58cf991b0b238a5b4850b52f4954d3d7158e6bb858bc06ca7e2dbdf851c0b"

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1048576


def read_picture(path):
    with open(path, "rb") as handle:
        return handle.read()


def check_dimensions(blob):
    """Second, independent guard: the PNG IHDR must say 1024 x 1024."""
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        sys.exit("entry.png has no IHDR chunk where one belongs")
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if (width, height) != (1024, 1024):
        sys.exit("entry.png is %dx%d, not 1024x1024" % (width, height))


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")

    blob = read_picture(source)
    check_dimensions(blob)

    if not blob.startswith(PNG_HEADER):
        sys.exit("entry.png is not a PNG file")
    if len(blob) > BYTE_LIMIT:
        sys.exit("entry.png is over the 1 MiB limit: %d bytes" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        sys.exit(
            "entry.png size changed: %d bytes, expected %d"
            % (len(blob), EXPECTED_BYTES)
        )
    if hashlib.sha256(blob).hexdigest() != EXPECTED_SHA256:
        sys.exit("entry.png sha256 does not match the recorded digest")

    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(blob)

    sys.stderr.write(
        "copied entry.png: %d bytes sha256=%s\n"
        % (len(blob), hashlib.sha256(blob).hexdigest())
    )


if __name__ == "__main__":
    main()
