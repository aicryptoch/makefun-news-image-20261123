#!/usr/bin/env python3
"""THE COMPLETE RECORD — NI23 G4 akun19 front page composer.

Draws a 1024x1024 newspaper front page for Monday 23 November 2026.
Local-only renderer (PIL allowed here; the submitted main.py is stdlib).
Usage: python3 compose.py [A|B] [out.png]
Variant A: lead card + map on the top row, 3-col card grid.
Variant B: two lead cards on the top row, map + date check in a right rail.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024

WHITE = (253, 253, 250)
PAPER = (255, 255, 255)
INK = (122, 14, 14)        # dark red ink
INK_SOFT = (150, 40, 34)
BLACK = (18, 18, 18)
GREY = (84, 84, 84)
LIGHT = (250, 244, 238)
CARD_LINE = (196, 178, 168)
RED_BOX = (146, 22, 18)

REGION_COLORS = {
    "EUROPE": (29, 78, 137),
    "MIDDLE EAST": (192, 86, 11),
    "NORTH AMERICA": (14, 124, 123),
    "SOUTH ASIA": (46, 125, 50),
    "SOUTHEAST ASIA": (106, 63, 160),
    "AFRICA": (141, 90, 43),
    "GLOBAL & PACIFIC": (96, 96, 96),
}

STATUS_FILL = {
    "REPORTED": (29, 78, 137),
    "CLAIM": (178, 34, 34),
    "DENIAL": (178, 34, 34),
    "ONGOING": (192, 86, 11),
    "OFFICIAL": (46, 125, 50),
    "ON RECORD": (106, 63, 160),
    "CONFIRMED": (46, 125, 50),
}


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def pf_black(size):
    return font("PlayfairDisplay-Black.ttf", size)


def pf_bold(size):
    return font("PlayfairDisplay-Bold.ttf", size)


def bold(size):
    return font("Archivo-Bold.ttf", size)


def reg(size):
    return font("Archivo.ttf", size)


def tw(d, text, fnt):
    return d.textlength(text, font=fnt)


def fit_font(d, text, name, start, minimum):
    """Largest Archivo-Bold size <= start that fits; returns (font, size)."""
    size = start
    while size > minimum:
        f = font(name, size)
        if tw(d, text, f) <= fit_font.maxw:
            return f, size
        size -= 1
    return font(name, minimum), minimum


# ---------------------------------------------------------------- stories
# (location, region, category, status, title, fact, source, icon)
LEAD = (
    "KYIV REGION, UKRAINE", "EUROPE", "WAR", "ON RECORD",
    "Fourteen Missing After Kyiv Strike, Zelenskiy Says",
    "Russian drones hit a Kyiv region block, leaving 14 missing; "
    "rescuers search the rubble, Zelenskiy said.",
    "Jagran Josh wire, 23 Nov", "building",
)

CARDS = [
    ("ANTALYA, TURKIYE", "EUROPE", "CLIMATE", "OFFICIAL",
     "COP31 Ends, No Deal",
     "Final Turkiye text omits fossil fuels - BBC.",
     "BBC / AP, 23 Nov", "globe"),
    ("STRAIT OF HORMUZ", "MIDDLE EAST", "WAR", "REPORTED",
     "Hormuz Tankers Burn",
     "Tankers ablaze as Iran-US war widens - AP.",
     "AP live, 23 Nov", "ship"),
    ("BAHRAIN", "MIDDLE EAST", "WAR", "CLAIM",
     "IRGC Claims Radar Hit",
     "Tehran claims 2 Patriot radars destroyed.",
     "AP / AFP wire, 23 Nov", "radar"),
    ("KYIV, UKRAINE", "EUROPE", "WAR", "REPORTED",
     "Boy, 7, Pulled Alive",
     "Boy, 7, freed after hours; 6 killed - BBC.",
     "BBC, 23 Nov", "building"),
    ("GULF OF FINLAND", "EUROPE", "SEA", "ONGOING",
     "Cargo Ship Still Burns",
     "Russian ship ablaze off Finland - BBC.",
     "BBC, 23 Nov", "ship"),
    ("WASHINGTON, US", "NORTH AMERICA", "POLITICS", "OFFICIAL",
     "Democrats Win the House",
     "Majority confirmed 23 Nov: 258-173.",
     "BBC, 23 Nov", "ballot"),
    ("WELLINGTON, NZ", "SOUTH ASIA", "CRICKET", "REPORTED",
     "India Declare on 720/9",
     "Highest Test total ever made in Wellington.",
     "Observer Voice, 23 Nov", "cricket"),
    ("THE HAGUE", "SOUTHEAST ASIA", "COURT", "OFFICIAL",
     "ICJ: Myanmar Genocide",
     "Guilty over 2017 Rohingya campaign.",
     "Guardian / NYT wire, 23 Nov", "scale"),
    ("IOWA, US", "NORTH AMERICA", "SAFETY", "REPORTED",
     "Iowa Explosives Plan",
     "US Army to blast unstable explosives - BBC.",
     "BBC, 23 Nov", "burst"),
    ("WORLD MARKETS", "GLOBAL & PACIFIC", "MONEY", "REPORTED",
     "Gold Slides to $3,538",
     "Down $2,000+ from the 2026 record high.",
     "Observer Voice, 23 Nov", "coin"),
    ("WASHINGTON, US", "NORTH AMERICA", "CRIME", "REPORTED",
     "FBI Probes Alleged Hack",
     "FBI probes alleged Justice hack - AP.",
     "AP wire, 23 Nov", "shield"),
    ("TURIN, ITALY", "EUROPE", "TENNIS", "REPORTED",
     "Alcaraz Wins ATP Finals",
     "Beats Zverev for first ATP Finals crown.",
     "BBC, 23 Nov", "ball"),
]

# fleet grid mirror: (num, region, topic, src, head, deck, kind)
grid = [
    (2, "EUROPE", "CLIMATE", "BBC / AP, 23 Nov", "COP31 Ends, No Deal",
     "Final Turkiye text omits fossil fuels - BBC.", "globe"),
    (3, "MIDDLE EAST", "WAR", "AP live, 23 Nov", "Hormuz Tankers Burn",
     "Tankers ablaze as Iran-US war widens - AP.", "ship"),
    (4, "MIDDLE EAST", "WAR", "AP / AFP wire, 23 Nov", "IRGC Claims Radar Hit",
     "Tehran claims 2 Patriot radars destroyed.", "radar"),
    (5, "EUROPE", "WAR", "BBC, 23 Nov", "Boy, 7, Pulled Alive",
     "Boy, 7, freed after hours; 6 killed - BBC.", "building"),
    (6, "EUROPE", "SEA", "BBC, 23 Nov", "Cargo Ship Still Burns",
     "Russian ship ablaze off Finland - BBC.", "ship"),
    (7, "NORTH AMERICA", "POLITICS", "BBC, 23 Nov", "Democrats Win the House",
     "Majority confirmed 23 Nov: 258-173.", "ballot"),
    (8, "SOUTH ASIA", "CRICKET", "Observer Voice, 23 Nov",
     "India Declare on 720/9", "Highest Test total ever made in Wellington.",
     "cricket"),
    (9, "SOUTHEAST ASIA", "COURT", "Guardian / NYT wire, 23 Nov",
     "ICJ: Myanmar Genocide", "Guilty over 2017 Rohingya campaign.", "scale"),
    (10, "NORTH AMERICA", "SAFETY", "BBC, 23 Nov", "Iowa Explosives Plan",
     "US Army to blast unstable explosives - BBC.", "burst"),
    (11, "GLOBAL & PACIFIC", "MONEY", "Observer Voice, 23 Nov",
     "Gold Slides to $3,538", "Down $2,000+ from the 2026 record high.", "coin"),
    (12, "NORTH AMERICA", "CRIME", "AP wire, 23 Nov", "FBI Probes Alleged Hack",
     "FBI probes alleged Justice hack - AP.", "shield"),
    (13, "EUROPE", "TENNIS", "BBC, 23 Nov", "Alcaraz Wins ATP Finals",
     "Beats Zverev for first ATP Finals crown.", "ball"),
]

dc = ("Xi-Trump-Putin summit - 19 Nov · Russian missiles fall in Poland - "
      "20 Nov · Paolo Bulgari death reported - 22 Nov · Kim Jong-un in "
      "Seoul - 22 Nov · Kerch Bridge strike reported - 22 Nov · S. Korea "
      "minister quits - first reported 22 Nov · Indonesia candy-factory "
      "fire itself - 22 Nov")

BRIEFS = [
    "Houthi missile intercepted over Saudi west",
    "UN: killer-AI talks to continue",
    "US releases more UFO footage files",
    "Albanese: COP31 failure, hard times",
    "Russia-bound ship towed after Finland attack",
    "Benghazi: suspected drone strike on ship",
    "UK-EU Brexit reset: Burnham hails 'landmark'",
    "Thousands march in Lisbon over cost of living",
    "Myanmar junta calls ASEAN ruling unfair",
    "Escaped lion spreads fear in Turkiye",
    "Nepal PM Shah holds talks with Modi in Delhi",
    "India, Bulgaria discuss IMEC and Black Sea",
    "Guru Nanak Jayanti marked across India",
    "UP air-raid + blackout drill, 75 districts",
    "Indonesia fire update: 7 found, 50 missing",
    "Wellington Test day 5: India hunt win",
    "India win ODI series 3-2; Phillips stars",
    "Anupama defends IBSF world snooker crown",
    "World Chess Championship draws the fans in",
    "Rajya Sabha MP Wadkute dies of heart attack",
    "Kota pilgrim bus tragedy: nine killed",
    "Tata Steel pipe sale: Rs 28,000 crore",
    "SpiceJet audit call; IndiGo at 65.9%",
    "IFFI 2026 hosts BRICS roundtable in Goa",
    "Modi opens AI centre at IIT Patna",
    "Shah launches Rs 4,000 crore Arunachal push",
    "Chief Justice: AI rules for law schools",
]

NUMS = [
    ("258-173", "HOUSE SEATS, CARD 7"),
    ("720/9", "INDIA DECLARED, CARD 8"),
    ("14", "MISSING IN KYIV, CARD 1"),
    ("$3,538", "GOLD PER OUNCE, CARD 11"),
    ("Rs 28,000 cr", "TATA STEEL SALE, NO. 35"),
    ("65.9%", "INDIGO SHARE, NO. 36"),
]

DATE_CHECKS = [
    "Xi-Trump-Putin summit - 19 Nov",
    "Russian missiles fall in Poland - 20 Nov",
    "Paolo Bulgari death reported - 22 Nov",
    "Kim Jong-un in Seoul - 22 Nov",
    "Kerch Bridge strike reported - 22 Nov",
    "S. Korea minister quits - first reported 22 Nov",
    "Indonesia candy-factory fire itself - 22 Nov",
]

REGIONS_LINE = [
    ("EUROPE", 10), ("MIDDLE EAST", 3), ("NORTH AMERICA", 4),
    ("SOUTH ASIA", 15), ("SOUTHEAST ASIA", 3), ("AFRICA", 1),
    ("GLOBAL & PACIFIC", 4),
]

TL = [
    ("00:02 UTC", "UN keeps AI talks going"),
    ("EARLY", "COP31 closes, no deal"),
    ("MORNING", "Kyiv boy pulled alive"),
    ("MIDDAY", "House 258-173 confirmed"),
    ("AFTERNOON", "Gold slides to $3,538"),
    ("EVENING", "Alcaraz lifts ATP title"),
]

# coarse dotted-world land grid (100 x 34), X = land
LAND = [
    "          XXXXXX                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                ",
    "        XXXXXXXXXXX            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                           ",
    "       XXXXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                          ",
    "      XXXXXXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                         ",
    "       XXXXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                        ",
    "        XXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                        ",
    "         XXXXXXXXX          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                        ",
    "          XXXXXXX            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                          ",
    "          XXXXXX              XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                           ",
    "           XXXXX               XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                            ",
    "           XXXX                 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                             ",
    "           XXX                   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                              ",
    "           XX                     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                ",
    "           XX                      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                  ",
    "          XXX                       XXXXXXXXXXXXXXXXXXXXXXXXXXXX                                    ",
    "          XXX                        XXXXXXXXXXXXXXXXXXXXXXXXX                                      ",
    "          XXXX                        XXXXXXXXXXXXXXXXXXXXXX                                        ",
    "          XXXX                         XXXXXXXXXXXXXXXXXXX                                          ",
    "          XXXX                          XXXXXXXXXXXXXXXXX                                           ",
    "          XXX                            XXXXXXXXXXXXXXX                                            ",
    "          XXX                             XXXXXXXXXXXXX                                             ",
    "          XX                               XXXXXXXXXXX                                              ",
    "          XX                                XXXXXXXXX                                               ",
    "          X                                  XXXXXXX                                                ",
    "                                             XXXXX                                                  ",
    "                                              XXX                                                   ",
    "                                              XX                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
]

# dotted-world land spans: row -> [(col_start, col_end), ...] on a 100x34 grid
# (overrides the coarse LAND sketch above with a geographically placed grid)
SPANS = {
    0: [(4, 10), (14, 32), (62, 95)],
    1: [(4, 12), (13, 33), (60, 97)],
    2: [(5, 13), (12, 34), (59, 98)],
    3: [(6, 13), (12, 34), (48, 55), (58, 96)],
    4: [(7, 12), (13, 33), (47, 53), (54, 59), (60, 90)],
    5: [(8, 12), (14, 32), (47, 57), (58, 90)],
    6: [(9, 12), (15, 31), (48, 59), (60, 88)],
    7: [(10, 12), (16, 30), (48, 56), (60, 86)],
    8: [(17, 29), (49, 55), (61, 84)],
    9: [(17, 29), (49, 54), (62, 82)],
    10: [(16, 22), (18, 28), (47, 53), (57, 62), (64, 80)],
    11: [(16, 21), (18, 27), (54, 64), (66, 78)],
    12: [(19, 26), (27, 28), (52, 58), (60, 66), (68, 77), (79, 80)],
    13: [(17, 19), (20, 24), (56, 63), (68, 76), (77, 80)],
    14: [(20, 23), (57, 62), (69, 75), (77, 79)],
    15: [(29, 33), (58, 62), (70, 74), (77, 78)],
    16: [(28, 35), (59, 61), (70, 73), (76, 77)],
    17: [(28, 36), (60, 61), (71, 72)],
    18: [(29, 37), (60, 60)],
    19: [(29, 37), (76, 78), (81, 83), (85, 86)],
    20: [(30, 36)],
    21: [(30, 35)],
    22: [(30, 34), (82, 90)],
    23: [(31, 34), (81, 92)],
    24: [(31, 33), (82, 92)],
    25: [(31, 33), (83, 90)],
    26: [(31, 32), (84, 88)],
    27: [(31, 32), (96, 97)],
    28: [(31, 31), (97, 98)],
    29: [(97, 97)],
}
LAND = []
for _r in range(34):
    _row = [" "] * 100
    for _c0, _c1 in SPANS.get(_r, []):
        for _c in range(_c0, _c1 + 1):
            _row[_c] = "X"
    LAND.append("".join(_row))

# pins: card number -> (lon, lat)
PINS = {
    1: (31.5, 50.4), 2: (30.7, 36.9), 3: (56.5, 26.5), 4: (50.5, 26.2),
    5: (29.0, 49.0), 6: (27.0, 60.0), 7: (-77.0, 38.9), 8: (174.8, -41.3),
    9: (96.0, 21.9), 10: (-93.5, 42.0), 11: (0.0, 51.5), 12: (-79.0, 37.0),
    13: (7.7, 45.1),
}


# ---------------------------------------------------------------- drawing
def chip(d, x, y, text):
    f = bold(11)
    wdt = tw(d, text, f) + 12
    d.rounded_rectangle([x, y, x + wdt, y + 16], 4,
                        fill=STATUS_FILL.get(text, BLACK))
    d.text((x + 6, y + 2), text, font=f, fill=(255, 255, 255))
    return wdt


def icon(d, kind, x, y, s, color):
    """Tiny flat pictogram inside an s x s box at (x, y)."""
    if kind == "building":
        d.rectangle([x + 4, y + 8, x + s - 10, y + s - 2], outline=color, width=2)
        d.polygon([(x + 2, y + 8), (x + s - 12, y + 8), (x + s // 2 - 5, y + 1)],
                  outline=color)
        for r in range(2):
            for c in range(2):
                d.rectangle([x + 8 + c * 8, y + 12 + r * 7,
                             x + 12 + c * 8, y + 16 + r * 7], fill=color)
        d.polygon([(x + s - 9, y + 2), (x + s - 3, y + 8), (x + s - 9, y + 8)],
                  fill=INK)
    elif kind == "ship":
        d.polygon([(x + 2, y + s - 10), (x + s - 2, y + s - 10),
                   (x + s - 7, y + s - 3), (x + 7, y + s - 3)], fill=color)
        d.rectangle([x + 10, y + s - 17, x + s - 12, y + s - 11], fill=color)
        d.polygon([(x + s // 2, y + 2), (x + s // 2 + 5, y + 10),
                   (x + s // 2 - 2, y + 10)], fill=(230, 110, 20))
    elif kind == "globe":
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=color, width=2)
        d.line([x + 3, y + s // 2, x + s - 3, y + s // 2], fill=color, width=1)
        d.ellipse([x + s // 2 - 5, y + 3, x + s // 2 + 5, y + s - 3],
                  outline=color, width=1)
    elif kind == "radar":
        d.arc([x + 2, y + 2, x + s - 8, y + s - 8], 200, 320, fill=color, width=2)
        d.arc([x + 7, y + 7, x + s - 13, y + s - 13], 200, 320, fill=color, width=2)
        d.line([x + s // 2 - 3, y + s - 4, x + s // 2 - 3, y + 8], fill=color, width=2)
        d.ellipse([x + s - 8, y + 2, x + s - 3, y + 7], fill=INK)
    elif kind == "ballot":
        d.rectangle([x + 5, y + 8, x + s - 5, y + s - 3], outline=color, width=2)
        d.rectangle([x + 10, y + 2, x + s - 10, y + 9], fill=color)
        d.line([x + 9, y + 16, x + 13, y + 20], fill=INK, width=2)
        d.line([x + 13, y + 20, x + s - 10, y + 12], fill=INK, width=2)
    elif kind == "cricket":
        d.line([x + 8, y + 3, x + 13, y + s - 8], fill=color, width=4)
        d.ellipse([x + s - 13, y + s - 13, x + s - 5, y + s - 5], fill=INK)
        for i in range(3):
            d.line([x + s - 6 + i * 3, y + 4, x + s - 6 + i * 3, y + 12],
                   fill=color, width=2)
    elif kind == "scale":
        d.line([x + s // 2, y + 3, x + s // 2, y + s - 6], fill=color, width=2)
        d.line([x + 5, y + 7, x + s - 5, y + 7], fill=color, width=2)
        d.polygon([(x + 5, y + 7), (x + 1, y + 15), (x + 9, y + 15)], fill=color)
        d.polygon([(x + s - 5, y + 7), (x + s - 9, y + 15), (x + s - 1, y + 15)],
                  fill=color)
        d.line([x + 9, y + s - 4, x + s - 9, y + s - 4], fill=color, width=2)
    elif kind == "burst":
        import math
        cx, cy = x + s // 2, y + s // 2
        for k in range(8):
            a = k * 3.14159 / 4
            d.line([cx, cy, cx + int(11 * math.cos(a)), cy + int(11 * math.sin(a))],
                   fill=(230, 110, 20), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    elif kind == "coin":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=color, width=2)
        d.text((x + s // 2 - 5, y + 7), "$", font=bold(16), fill=INK)
    elif kind == "shield":
        d.polygon([(x + s // 2, y + 2), (x + s - 5, y + 6), (x + s - 5, y + s - 10),
                   (x + s // 2, y + s - 2), (x + 5, y + s - 10), (x + 5, y + 6)],
                  outline=color, width=2)
        d.line([x + 10, y + 14, x + 14, y + 18], fill=INK, width=2)
        d.line([x + 14, y + 18, x + s - 10, y + 10], fill=INK, width=2)
    elif kind == "ball":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=color, width=2)
        d.arc([x + 1, y + 4, x + 14, y + s - 4], 270, 90, fill=INK, width=1)
        d.arc([x + s - 14, y + 4, x + s - 1, y + s - 4], 90, 270, fill=INK, width=1)


def fb(n):
    """Headline font (Playfair Display Bold)."""
    return font("PlayfairDisplay-Bold.ttf", n)


def fr(n):
    """Deck font (Archivo regular)."""
    return font("Archivo.ttf", n)


def fsr(n):
    """Brief font (Archivo regular)."""
    return font("Archivo.ttf", n)


def _card_frame(d, x, y, wdt, hgt, meta, region, kind, big):
    num, loc, cat, status = meta.split("|")
    d.rectangle([x, y, x + wdt, y + hgt], fill=PAPER, outline=CARD_LINE, width=1)
    d.rectangle([x, y, x + wdt, y + 4], fill=REGION_COLORS[region])
    nf = bold(15 if big else 13)
    d.text((x + 7, y + 8), num, font=nf, fill=INK)
    icon(d, kind, x + 26, y + 6, 22, REGION_COLORS[region])
    lf = bold(13 if big else 12)
    d.text((x + 52, y + 9), loc, font=lf, fill=BLACK)
    chw = tw(d, status, bold(11)) + 12
    chip(d, x + wdt - chw - 6, y + 7, status)
    cf = reg(11 if big else 10)
    d.text((x + 7, y + 25), "%s · %s" % (region, cat), font=cf, fill=GREY)


def lead(d, x, y, wdt, hgt, meta, region, src, head, deck, kind):
    """The big lead card (card 1). meta = 'num|loc|cat|status'."""
    _card_frame(d, x, y, wdt, hgt, meta, region, kind, True)
    tf = fb(31)
    words, lines, cur = head.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, tf) <= wdt - 170:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    ty = y + 40
    for ln in lines[:2]:
        d.text((x + 8, ty), ln, font=tf, fill=BLACK)
        ty += 34
    # big illustration: burning block + drone, right side
    bx, by = x + wdt - 140, y + 42
    d.rectangle([bx, by + 26, bx + 62, by + 96], outline=BLACK, width=2)
    for r in range(3):
        for c in range(3):
            d.rectangle([bx + 8 + c * 17, by + 34 + r * 19,
                         bx + 18 + c * 17, by + 44 + r * 19], fill=INK_SOFT)
    d.polygon([(bx + 16, by + 96), (bx + 30, by + 70), (bx + 44, by + 96)],
              fill=(120, 120, 120))
    d.polygon([(bx + 88, by + 6), (bx + 104, by + 6), (bx + 96, by + 14)],
              fill=BLACK)
    d.line([bx + 80, by + 10, bx + 112, by + 10], fill=BLACK, width=2)
    d.polygon([(bx + 92, by + 30), (bx + 100, by + 18), (bx + 108, by + 30)],
              fill=(230, 110, 20))
    ff = fr(15)
    fy = ty + 1
    words, cur = deck.split(), ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, ff) <= wdt - 170:
            cur = t
        else:
            d.text((x + 8, fy), cur, font=ff, fill=(40, 40, 40))
            fy += 17
            cur = wd
    d.text((x + 8, fy), cur, font=ff, fill=(40, 40, 40))
    sfnt = reg(11)
    stxt = "Source: " + src
    d.text((x + wdt - 8 - tw(d, stxt, sfnt), y + hgt - 15), stxt,
           font=sfnt, fill=GREY)


def mini(d, x, y, wdt, hgt, meta, region, src, head, deck, kind):
    """A standard grid card. meta = 'num|loc|cat|status'."""
    _card_frame(d, x, y, wdt, hgt, meta, region, kind, False)
    tf = fb(28)
    if tw(d, head, tf) > wdt - 14:
        alt = font("Archivo-Bold.ttf", 28)
        if tw(d, head, alt) <= wdt - 14:
            tf = alt
        else:
            fit_font.maxw = wdt - 14
            tf, _ = fit_font(d, head, "Archivo-Bold.ttf", 27, 20)
    d.text((x + 7, y + 37), head, font=tf, fill=BLACK)
    d.text((x + 7, y + 67), deck, font=fr(15), fill=(40, 40, 40))
    d.text((x + 7, y + hgt - 12), "Source: " + src, font=reg(10), fill=GREY)


def draw_map(d, x, y, wdt, hgt):
    """dotted_map: dotted world map; pins mark the numbered stories."""
    d.rectangle([x, y, x + wdt, y + hgt], fill=LIGHT, outline=CARD_LINE, width=1)
    d.text((x + 7, y + 4), "WHERE THE DAY HAPPENED", font=bold(11), fill=INK)
    d.text((x + 7, y + 17), "PINS MARK THE NUMBERED STORIES · DOTS = LAND",
           font=reg(9), fill=GREY)
    rows = len(LAND)
    cols = max(len(r) for r in LAND)
    gx, gy = x + 8, y + 28
    gw, gh = wdt - 16, hgt - 54
    cell_w = gw / cols
    cell_h = gh / rows
    dot = max(1, int(min(cell_w, cell_h) * 0.42))
    for r, row in enumerate(LAND):
        for c, ch in enumerate(row):
            if ch == "X":
                cx = gx + c * cell_w
                cy = gy + r * cell_h
                d.ellipse([cx, cy, cx + dot, cy + dot], fill=(150, 130, 120))
    for num, (lon, lat) in PINS.items():
        px = gx + (lon + 180) / 360.0 * gw
        py = gy + (75 - lat) / 135.0 * gh
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=INK)
        t = str(num)
        tf = bold(9)
        d.text((px - tw(d, t, tf) / 2, py - 5), t, font=tf, fill=(255, 255, 255))
    tf = reg(9)
    for row_i, group in enumerate((REGIONS_LINE[:4], REGIONS_LINE[4:])):
        ly = y + hgt - 24 + row_i * 11
        lx = x + 7
        for name, _n in group:
            col = REGION_COLORS[name]
            d.rectangle([lx, ly + 1, lx + 7, ly + 8], fill=col)
            d.text((lx + 10, ly), name.title(), font=tf, fill=GREY)
            lx += 10 + tw(d, name.title(), tf) + 8


def numbers_strip(d, x, y, wdt, hgt):
    d.rectangle([x, y, x + wdt, y + hgt], fill=BLACK)
    d.text((x + 8, y + 4), "THE DAY IN NUMBERS", font=bold(11), fill=(255, 214, 150))
    cw = (wdt - 16) / 6.0
    for i, (big, label) in enumerate(NUMS):
        cx = x + 8 + i * cw
        fit_font.maxw = cw - 14
        nf, _ = fit_font(d, big, "Archivo-Bold.ttf", 26, 15)
        d.text((cx, y + 13), big, font=nf, fill=(255, 255, 255))
        d.text((cx, y + hgt - 10), label, font=reg(9), fill=(200, 200, 200))


def numbers_box(d, x, y, wdt, hgt):
    d.rectangle([x, y, x + wdt, y + hgt], fill=BLACK)
    d.text((x + 9, y + 6), "THE DAY IN NUMBERS", font=bold(12), fill=(255, 214, 150))
    cw = (wdt - 18) / 2.0
    rh = (hgt - 30) / 3.0
    for i, (big, label) in enumerate(NUMS):
        cx = x + 9 + (i % 2) * cw
        cy = y + 28 + (i // 2) * rh
        fit_font.maxw = cw - 6
        nf, _ = fit_font(d, big, "Archivo-Bold.ttf", 26, 16)
        d.text((cx, cy), big, font=nf, fill=(255, 255, 255))
        d.text((cx, cy + 27), label, font=reg(8), fill=(200, 200, 200))


def date_check_band(d, x, y, wdt):
    d.rectangle([x, y, x + wdt, y + 32], fill=(252, 238, 236),
                outline=RED_BOX, width=1)
    lab = "DATE CHECK - CHECKED & LEFT OUT:"
    d.text((x + 7, y + 5), lab, font=bold(11), fill=RED_BOX)
    tx = x + 7 + tw(d, lab, bold(11)) + 8
    tf = reg(10)
    d.text((tx, y + 5), "  ·  ".join(DATE_CHECKS[:3]), font=tf,
           fill=(90, 30, 26))
    d.text((x + 7, y + 18), "  ·  ".join(DATE_CHECKS[3:]), font=tf,
           fill=(90, 30, 26))


def date_check_box(d, x, y, wdt, hgt):
    d.rectangle([x, y, x + wdt, y + hgt], fill=(252, 238, 236),
                outline=RED_BOX, width=1)
    d.text((x + 8, y + 6), "DATE CHECK - CHECKED & LEFT OUT", font=bold(12),
           fill=RED_BOX)
    tf = reg(12)
    ty = y + 28
    for item in DATE_CHECKS:
        d.text((x + 8, ty), "x " + item, font=tf, fill=(90, 30, 26))
        ty += 19


def also_block(d, x, y, wdt, cols, start_num=14):
    d.text((x, y), "ALSO ON MONDAY - THE REST OF THE DAY, NUMBERED",
           font=bold(13), fill=INK)
    rows = (len(BRIEFS) + cols - 1) // cols
    cw = wdt / cols
    base = fsr(13)
    for i, item in enumerate(BRIEFS):
        cx = x + (i // rows) * cw
        cy = y + 18 + (i % rows) * 12
        label = "%d. %s" % (start_num + i, item)
        f2 = base
        if tw(d, label, f2) > cw - 8:
            fit_font.maxw = cw - 8
            f2, _ = fit_font(d, label, "Archivo.ttf", 12, 10)
        d.text((cx, cy), label, font=f2, fill=(30, 30, 30))


def header_and_strips(d):
    # top bar
    d.text((16, 6), "THE COMPLETE RECORD", font=bold(14), fill=INK)
    kick = "40 STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    kf = bold(13)
    d.text((W - 16 - tw(d, kick, kf), 7), kick, font=kf, fill=BLACK)
    d.line([16, 27, W - 16, 27], fill=BLACK, width=2)
    # masthead
    nf = pf_black(38)
    name = "THE COMPLETE RECORD"
    d.text(((W - tw(d, name, nf)) / 2, 30), name, font=nf, fill=INK)
    df = pf_black(68)
    date = "Monday 23 November 2026"
    d.text(((W - tw(d, date, df)) / 2, 64), date, font=df, fill=BLACK)
    sub = ("Fourteen missing in Kyiv, Zelenskiy says  ·  COP31 ends with no "
           "deal  ·  Tankers burn in the Strait of Hormuz")
    sf = reg(15)
    d.text(((W - tw(d, sub, sf)) / 2, 148), sub, font=sf, fill=INK_SOFT)
    d.line([16, 168, W - 16, 168], fill=INK, width=2)
    # region strip
    rx = 16
    ry = 174
    for rname, cnt in REGIONS_LINE:
        col = REGION_COLORS[rname]
        label = "%s %d" % (rname, cnt)
        lf = bold(12)
        wdt = tw(d, label, lf) + 22
        d.rectangle([rx, ry, rx + wdt, ry + 20], fill=col)
        d.text((rx + 8, ry + 4), label, font=lf, fill=(255, 255, 255))
        rx += wdt + 8
    # timeline strip
    ty = 200
    d.rectangle([16, ty, W - 16, ty + 34], fill=LIGHT, outline=CARD_LINE, width=1)
    sw = (W - 32) / 6.0
    for i, (when, what) in enumerate(TL):
        sx = 22 + i * sw
        d.text((sx, ty + 3), when, font=bold(12), fill=INK)
        d.text((sx, ty + 18), what, font=reg(12), fill=(40, 40, 40))


def footer(d):
    y = 994
    d.line([16, y - 4, W - 16, y - 4], fill=BLACK, width=1)
    l1 = ("HOW SURE: REPORTED = confirmed by named outlets · CLAIM = one "
          "side's account, labelled as such · ON RECORD = said publicly by "
          "an official · ONGOING = still unfolding")
    d.text((16, y), l1, font=reg(11), fill=BLACK)
    l2 = ("Every story happened, or was first reported, on Monday 23 "
          "November 2026. Contested claims are attributed. · Original drawings.")
    d.text((16, y + 14), l2, font=reg(11), fill=BLACK)


def build(variant):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    header_and_strips(d)
    if variant == "A":
        # lead row: card 1 + map on the right
        lead(d, 16, 242, 636, 148,
             "1|KYIV REGION, UKRAINE|WAR|ON RECORD", "EUROPE",
             "Jagran Josh wire, 23 Nov",
             "Fourteen Missing After Kyiv Strike, Zelenskiy Says",
             "Russian drones hit a Kyiv region block, leaving 14 missing; "
             "rescuers search the rubble, Zelenskiy said.", "building")
        draw_map(d, 660, 242, 348, 148)
        numbers_strip(d, 16, 396, W - 32, 50)
        # grid cards 2..13: 3 cols x 4 rows, row-major
        gx, gy = 16, 452
        cw, chh, gap = 328, 94, 4
        for i, story in enumerate(CARDS):
            loc, region, cat, status, head, deck, src, kind = story
            meta = "%d|%s|%s|%s" % (i + 2, loc, cat, status)
            cx = gx + (i % 3) * (cw + gap)
            cy = gy + (i // 3) * (chh + gap)
            mini(d, cx, cy, cw, chh, meta, region, src, head, deck, kind)
        also_block(d, 16, 846, W - 32, 4)
        date_check_band(d, 16, 954, W - 32)
    else:
        # lead row: map on the LEFT, card 1 on the right
        draw_map(d, 16, 242, 348, 148)
        _loc, _region, _cat, _status, _head, _deck, _src, _kind = LEAD
        _meta = "1|%s|%s|%s" % (_loc, _cat, _status)
        lead(d, 372, 242, 636, 148, _meta, _region, _src, _head, _deck, _kind)
        numbers_strip(d, 16, 396, W - 32, 50)
        # grid cards 2..13: 3 cols x 4 rows, column-major fill
        gx, gy = 16, 452
        cw, chh, gap = 328, 94, 4
        for i, story in enumerate(CARDS):
            loc, region, cat, status, head, deck, src, kind = story
            meta = "%d|%s|%s|%s" % (i + 2, loc, cat, status)
            cx = gx + (i // 4) * (cw + gap)
            cy = gy + (i % 4) * (chh + gap)
            mini(d, cx, cy, cw, chh, meta, region, src, head, deck, kind)
        also_block(d, 16, 846, W - 32, 4)
        date_check_band(d, 16, 954, W - 32)
    footer(d)
    return img


def compact_card(d, x, y, wdt, hgt, num, story):
    loc, region, cat, status, title, fact, source, ic = story
    d.rectangle([x, y, x + wdt, y + hgt], fill=PAPER, outline=CARD_LINE, width=1)
    d.rectangle([x, y, x + wdt, y + 3], fill=REGION_COLORS[region])
    d.text((x + 6, y + 6), "%d" % num, font=bold(12), fill=INK)
    icon(d, ic, x + 22, y + 4, 18, REGION_COLORS[region])
    d.text((x + 44, y + 7), loc, font=bold(11), fill=BLACK)
    chw = tw(d, status, bold(10)) + 10
    d.rounded_rectangle([x + wdt - chw - 5, y + 5, x + wdt - 5, y + 19], 3,
                        fill=STATUS_FILL.get(status, BLACK))
    d.text((x + wdt - chw, y + 7), status, font=bold(10), fill=(255, 255, 255))
    fit_font.maxw = wdt - 12
    tf, _ = fit_font(d, title, "Archivo-Bold.ttf", 24, 18)
    d.text((x + 6, y + 22), title, font=tf, fill=BLACK)
    d.text((x + 6, y + hgt - 13), fact, font=reg(11), fill=(40, 40, 40))


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-akun19-%s.png" % variant
    im = build(variant)
    # flat art quantizes cleanly; palette PNG keeps the file in the target band
    im = im.quantize(colors=256, method=Image.MEDIANCUT)
    im.save(out, optimize=True)
    print(out, im.size)
