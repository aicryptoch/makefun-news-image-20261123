#!/usr/bin/env python3
"""Delivery program for THE COMPLETE RECORD (news-image-20261123, G4).

The PNG beside this file is a complete front page for Monday
23 November 2026, drawn for this entry: thirteen numbered main cards
(the lead reports fourteen people missing after a Russian drone strike
in the Kyiv region, attributed to President Zelenskiy), a strip of the
day in numbers, a dotted world map with a pin per main card, twenty
seven numbered briefs, and a red date-check box of older stories that
were checked and deliberately left out.

All this program does is republish that PNG. It reads entry.png,
refuses to continue if the bytes no longer match the size and SHA-256
recorded below, then writes an identical copy into the directory named
by MAKEFUN_OUTPUT_DIR (falling back to /output). Nothing is rendered,
downloaded or transformed here; the standard library is all it uses.
"""

import hashlib
import os
import sys

ART_BYTES = 128099
ART_SHA256 = "310782b8516d666381b8938d931a42e251e4c823338527c3cdee020186ff7485"
LIMIT = 1048576
MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png(path):
    with open(path, "rb") as stream:
        return stream.read()


def check(blob):
    """Return the digest when the artwork is intact, else stop.

    The size test runs before the digest so a truncated or swapped file
    fails with the clearer message; both guards must pass to publish.
    """
    if blob[:8] != MAGIC:
        sys.exit("entry.png: bad PNG signature")
    if len(blob) != ART_BYTES:
        sys.exit(
            "entry.png: %d bytes on disk, %d expected" % (len(blob), ART_BYTES)
        )
    if len(blob) > LIMIT:
        sys.exit("entry.png: over the 1 MiB competition limit")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != ART_SHA256:
        sys.exit("entry.png: sha256 mismatch (%s)" % digest)
    return digest


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    blob = read_png(os.path.join(here, "entry.png"))
    digest = check(blob)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # The harness may point this at a fresh directory, so create it.
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    with open(destination, "wb") as stream:
        stream.write(blob)

    sys.stderr.write(
        "entry.png delivered: %d bytes, sha256 %s\n" % (len(blob), digest)
    )


if __name__ == "__main__":
    run()
