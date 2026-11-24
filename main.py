#!/usr/bin/env python3
"""THE FRONT PAGE — delivery program for the akun19 news-image entry.

THE FRONT PAGE is the Monday 23 November 2026 newspaper front page built
for the make.fun news-image-20261123 bounty; its lead story covers the
US Army plan to detonate unstable explosives in Iowa. The finished page
sits next to this file as entry.png. This program's only task is to hand
that page over untouched: verify the bytes against the recorded size and
digest, then copy them into the output directory.

Nothing here draws or edits pixels. The standard library is all it uses
(hashlib, os, sys), and repeated runs emit byte-identical output.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 299037
EXPECTED_SHA256 = "57b58cf991b0b238a5b4850b52f4954d3d7158e6bb858bc06ca7e2dbdf851c0b"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def load_page(path):
    with open(path, "rb") as stream:
        return stream.read()


def verify_page(blob):
    """Refuse to ship anything that is not the recorded front page."""
    if not blob.startswith(PNG_SIGNATURE):
        sys.exit("entry.png: missing PNG signature")
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        sys.exit("entry.png: IHDR chunk not found at the expected offset")
    dims = (int.from_bytes(blob[16:20], "big"), int.from_bytes(blob[20:24], "big"))
    if dims != (1024, 1024):
        sys.exit("entry.png: page is %dx%d, expected 1024x1024" % dims)
    if len(blob) > MAX_BYTES:
        sys.exit("entry.png: %d bytes exceeds the 1 MiB ceiling" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        sys.exit(
            "entry.png: size drifted to %d bytes, recorded %d"
            % (len(blob), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png: sha256 %s does not match the recorded digest" % digest)
    return digest


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = os.path.join(out_dir, "entry.png")

    blob = load_page(source)
    digest = verify_page(blob)

    # Copy in two halves so a truncated write is easy to spot in the log.
    os.makedirs(out_dir, exist_ok=True)
    midpoint = len(blob) // 2
    with open(destination, "wb") as stream:
        stream.write(blob[:midpoint])
        stream.write(blob[midpoint:])

    written = os.path.getsize(destination)
    if written != len(blob):
        sys.exit("entry.png: wrote %d of %d bytes" % (written, len(blob)))

    sys.stderr.write("THE FRONT PAGE delivered: %d bytes sha256=%s\n" % (len(blob), digest))


if __name__ == "__main__":
    main()
