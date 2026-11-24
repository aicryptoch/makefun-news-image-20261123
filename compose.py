#!/usr/bin/env python3
"""THE FRONT PAGE — NI23 G3, akun19 (@retteangs1).

One-page newspaper front page for Monday 23 November 2026.
Lead story: pool #45, the US Army plan to detonate unstable explosives
in Iowa. Trio partners chosen by this builder: #43 (Democrats take the
House 258-173) and #25 (India 720/9d at Wellington). All facts and
figures come only from the locked NI23 pool. Original simple drawings.
Variants: a = bright white / dark-red ink / black accent (assigned),
b = cream sheet / dark-red ink / slate accent,
c = white sheet / black ink / dark-red masthead band.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
PF_BLACK = FD + "PlayfairDisplay-Black.ttf"
PF_BOLD = FD + "PlayfairDisplay-Bold.ttf"
AR = FD + "Archivo.ttf"
AR_B = FD + "Archivo-Bold.ttf"

W = H = 1024
M = 26

REGIONS = {
    "MIDDLE EAST": (176, 84, 20),
    "NORTH AMERICA": (20, 90, 160),
    "EUROPE": (30, 120, 70),
    "SOUTH ASIA": (200, 130, 20),
    "SOUTHEAST ASIA": (140, 60, 160),
    "GLOBAL": (90, 90, 90),
    "AFRICA": (180, 100, 40),
    "ASIA-PACIFIC": (20, 140, 140),
}

NUMS = [
    ("258-173", "US HOUSE DEMOCRATS WIN"),
    ("720/9d", "INDIA AT WELLINGTON"),
    ("7 + 50", "FOUND + MISSING INDONESIA"),
    ("14", "MISSING IN KYIV"),
    ("$3,538", "GOLD PER OUNCE"),
    ("Rs 28,000 cr", "TATA STEEL PIPE DEAL"),
]

TL = [
    ("00:02 UTC", "UN lethal-AI talks continue"),
    ("02:00 UTC", "Albanese on COP31 failure"),
    ("MORNING", "Hormuz tankers burn"),
    ("MIDDAY", "Kyiv: 6 dead, 14 missing"),
    ("EVENING", "Iowa detonation readied"),
]

# grid cards: (num, region, topic, src, head, deck, kind)
grid = [
    (4, "EUROPE", "climate talks", "BBC / AP", "COP31 Ends With No Deal",
     "Final draft in Turkiye omits fossil fuels - BBC.", "cloud"),
    (5, "EUROPE", "kyiv rescue", "BBC", "Kyiv Boy, 7, Pulled Alive From Rubble",
     "Boy aged 7 freed after hours; 6 killed in Kyiv.", "rubble"),
    (6, "EUROPE", "kyiv missing", "JAGRANJOSH", "14 Missing After Kyiv Drone Strike",
     "Kyiv says Zelenskiy: 14 missing.", "drone"),
    (7, "MIDDLE EAST", "hormuz tankers", "AP LIVE", "Tankers Burn in the Strait of Hormuz",
     "IRGC warns as Iran-US war widens to Gulf.", "ship"),
    (8, "SOUTHEAST ASIA", "icj ruling", "GUARDIAN / NYT", "ICJ Rules Myanmar Guilty of Genocide",
     "Rohingya campaign of 2017: 700,000+ fled.", "scale"),
    (9, "GLOBAL", "gold price", "OBSERVERVOICE", "Gold Slides to $3,538 an Ounce",
     "Down $2,000+ from the 2026 record of $5,595.", "gold"),
    (10, "SOUTHEAST ASIA", "factory fire", "JAGRANJOSH", "Indonesia: 7 Found, 50 Still Missing",
     "7 found dead; 50 missing in Indonesia.", "factory"),
    (11, "SOUTH ASIA", "steel deal", "OBSERVERVOICE", "Tata Steel Sells Pipe Business",
     "Pipe unit sold to APL Apollo for Rs 28,000 cr.", "pipe"),
    (12, "EUROPE", "ship fire", "BBC / JAGRANJOSH", "Russian Cargo Ship Still Burns Off Finland",
     "The Russian ship burns off Finland - BBC wire.", "ship"),
]

BRIEFS = [
    "IRGC claims 2 Patriot radars in Bahrain",
    "Houthi missile intercepted over Saudi",
    "Swimmer crosses Hormuz for wildlife",
    "US releases more UFO footage",
    "Albanese: COP31 failure a hard sign",
    "Ship towed after Gulf of Finland hit",
    "Blast hits Russian ship in Benghazi",
    "UK-EU reset deal called a landmark",
    "Lisbon marches over cost of living",
    "Myanmar junta calls ASEAN unfair",
    "Cameroon ex-rebels trapped, promises",
    "Escaped lion frightens Turkiye town",
    "Nepal PM Shah in talks with Modi",
    "India, Bulgaria discuss IMEC, Black Sea",
    "Guru Nanak Jayanti across India",
    "UP air-raid drills in 75 districts",
    "India chase famous win; NZ 119/2",
    "India win ODI series in NZ 3-2",
    "Anupama defends world snooker title",
    "World Chess Championship draws crowds",
    "Kota pilgrim bus tragedy: 9 dead",
    "SpiceJet audit call; IndiGo at 65.9%",
    "Modi opens IIT Patna AI Centre",
    "Google gives $5m to IIT Kharagpur AI",
    "FBI probes hack of justice database",
    "Trump attacks Schumer over leadership",
    "Miley Cyrus marries Maxx Morando",
    "Mets sign Ewing: $95m, 8 years",
]

dc = ("Xi-Trump-Putin summit - 19 Nov 2026 \u00b7 Russian missiles fall in Poland - 20 Nov 2026 \u00b7 "
      "SpiceJet Rs 5,500 cr fundraise - 18 Nov 2026 \u00b7 Hyderabad bomb-threat email - 21 Nov 2026 \u00b7 "
      "Paolo Bulgari dies - reported 22 Nov 2026 \u00b7 Bolsonaro 'stable' in ICU - 22 Nov 2026")
DATE_CHECK = [s.strip() for s in dc.split("\u00b7")]

PINS = [(1, 70, 44), (2, 90, 50), (3, 330, 78), (4, 172, 24), (5, 202, 22), (6, 224, 30),
        (7, 238, 47), (8, 274, 61), (9, 148, 54), (10, 284, 66), (11, 254, 55), (12, 188, 38)]

MAP_NOTE = "Dotted world map: numbered pins mark every card story on this page."


def F(path, size):
    return ImageFont.truetype(path, size)


def fb(size):
    return F(AR_B, size)


def fr(size):
    return F(AR, size)


def fsr(size):
    return F(AR, size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def icon(d, kind, x, y, s, ink, acc):
    """Tiny original line drawings, one per card."""
    if kind == "burst":
        cx, cy = x + s // 2, y + s // 2 - 4
        for i in range(12):
            a = math.pi * i / 6
            r1, r2 = s * 0.16, s * (0.46 if i % 2 == 0 else 0.30)
            d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                    cx + r2 * math.cos(a), cy + r2 * math.sin(a)], fill=acc, width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=ink)
        d.line([x + 2, y + s - 4, x + s - 2, y + s - 4], fill=ink, width=3)
    elif kind == "ballot":
        d.rectangle([x + 4, y + s * 0.35, x + s - 4, y + s - 4], outline=ink, width=3)
        d.rectangle([x + s * 0.3, y + 4, x + s * 0.7, y + s * 0.35], outline=acc, width=3)
    elif kind == "cricket":
        d.line([x + s * 0.3, y + 4, x + s * 0.55, y + s - 6], fill=ink, width=5)
        d.ellipse([x + s * 0.6, y + s * 0.55, x + s * 0.85, y + s * 0.8], fill=acc)
        d.line([x + 4, y + s - 4, x + s - 4, y + s - 4], fill=ink, width=2)
    elif kind == "cloud":
        d.ellipse([x + 4, y + s * 0.3, x + s * 0.6, y + s * 0.75], outline=ink, width=3)
        d.ellipse([x + s * 0.35, y + s * 0.15, x + s - 4, y + s * 0.75], outline=ink, width=3)
        d.line([x + s * 0.3, y + s * 0.85, x + s * 0.42, y + s - 2], fill=acc, width=3)
        d.line([x + s * 0.55, y + s * 0.85, x + s * 0.67, y + s - 2], fill=acc, width=3)
    elif kind == "rubble":
        d.polygon([(x + 4, y + s - 4), (x + s * 0.4, y + s * 0.3), (x + s * 0.62, y + s - 4)], outline=ink, width=3)
        d.polygon([(x + s * 0.45, y + s - 4), (x + s * 0.7, y + s * 0.45), (x + s - 4, y + s - 4)], outline=acc, width=3)
        d.ellipse([x + s * 0.42, y + s * 0.18, x + s * 0.58, y + s * 0.34], fill=acc)
    elif kind == "drone":
        d.rectangle([x + s * 0.35, y + s * 0.4, x + s * 0.65, y + s * 0.6], outline=ink, width=3)
        for (ex, ey) in [(0.15, 0.2), (0.85, 0.2), (0.15, 0.8), (0.85, 0.8)]:
            d.ellipse([x + s * ex - 6, y + s * ey - 3, x + s * ex + 6, y + s * ey + 3], outline=acc, width=2)
        d.line([x + s * 0.5, y + s * 0.6, x + s * 0.5, y + s * 0.85], fill=acc, width=3)
    elif kind == "ship":
        d.polygon([(x + 4, y + s * 0.6), (x + s - 4, y + s * 0.6), (x + s * 0.8, y + s * 0.85), (x + s * 0.2, y + s * 0.85)], outline=ink, width=3)
        d.rectangle([x + s * 0.4, y + s * 0.35, x + s * 0.62, y + s * 0.6], outline=ink, width=2)
        d.polygon([(x + s * 0.48, y + s * 0.05), (x + s * 0.56, y + s * 0.28), (x + s * 0.42, y + s * 0.28)], fill=acc)
    elif kind == "scale":
        d.line([x + s * 0.5, y + 6, x + s * 0.5, y + s - 8], fill=ink, width=3)
        d.line([x + s * 0.15, y + s * 0.25, x + s * 0.85, y + s * 0.25], fill=ink, width=3)
        d.arc([x + s * 0.05, y + s * 0.25, x + s * 0.35, y + s * 0.62], 0, 180, fill=acc, width=3)
        d.arc([x + s * 0.65, y + s * 0.25, x + s * 0.95, y + s * 0.62], 0, 180, fill=acc, width=3)
        d.line([x + s * 0.3, y + s - 6, x + s * 0.7, y + s - 6], fill=ink, width=3)
    elif kind == "gold":
        d.polygon([(x + s * 0.2, y + s * 0.3), (x + s * 0.8, y + s * 0.3), (x + s * 0.68, y + s * 0.52), (x + s * 0.32, y + s * 0.52)], outline=ink, width=3)
        d.polygon([(x + s * 0.12, y + s * 0.58), (x + s * 0.88, y + s * 0.58), (x + s * 0.74, y + s * 0.82), (x + s * 0.26, y + s * 0.82)], fill=acc)
        d.line([x + s * 0.5, y + 4, x + s * 0.38, y + s * 0.2], fill=ink, width=3)
        d.line([x + s * 0.38, y + s * 0.2, x + s * 0.62, y + s * 0.2], fill=ink, width=3)
    elif kind == "factory":
        d.rectangle([x + 4, y + s * 0.45, x + s - 4, y + s - 4], outline=ink, width=3)
        d.rectangle([x + s * 0.15, y + s * 0.12, x + s * 0.3, y + s * 0.45], outline=ink, width=2)
        d.ellipse([x + s * 0.55, y + s * 0.08, x + s * 0.8, y + s * 0.3], outline=acc, width=3)
        d.line([x + s * 0.62, y + s * 0.3, x + s * 0.72, y + s * 0.45], fill=acc, width=3)
    elif kind == "pipe":
        d.line([x + 4, y + s * 0.4, x + s - 4, y + s * 0.4], fill=ink, width=5)
        d.line([x + 4, y + s * 0.65, x + s - 4, y + s * 0.65], fill=ink, width=5)
        d.line([x + s * 0.3, y + s * 0.25, x + s * 0.3, y + s * 0.8], fill=acc, width=4)
        d.line([x + s * 0.68, y + s * 0.25, x + s * 0.68, y + s * 0.8], fill=acc, width=4)


def lead(d, x, y, w, h, num, region, src, head, deck, kind, ink, acc):
    """The big lead card."""
    d.rectangle([x, y, x + w, y + h], outline=acc, width=2)
    d.rectangle([x, y, x + 30, y + 30], fill=ink)
    d.text((x + 8, y + 4), str(num), font=fb(20), fill=(255, 255, 255))
    cf = fb(11)
    d.rectangle([x + 38, y + 6, x + 38 + d.textlength(region, font=cf) + 12, y + 24], fill=REGIONS[region])
    d.text((x + 44, y + 9), region, font=cf, fill=(255, 255, 255))
    d.text((x + w - d.textlength(src, font=cf) - 10, y + 8), src, font=cf, fill=acc)
    icon(d, kind, x + w - 76, y + 36, 64, ink, acc)
    ly = y + 34
    for ln in wrap(d, head, fb(24), w - 110):
        d.text((x + 10, ly), ln, font=fb(24), fill=ink)
        ly += 27
    d.text((x + 10, y + 118), deck, font=fr(14), fill=acc)


def mini(d, x, y, w, h, num, region, src, head, deck, kind, ink, acc, wide=False):
    """A trio card (normal or wide)."""
    d.rectangle([x, y, x + w, y + h], outline=acc, width=2)
    d.rectangle([x, y, x + 30, y + 30], fill=ink)
    d.text((x + 8, y + 4), str(num), font=fb(20), fill=(255, 255, 255))
    cf = fb(11)
    if wide:
        d.rectangle([x + 38, y + 6, x + 38 + d.textlength(region, font=cf) + 12, y + 24], fill=REGIONS[region])
        d.text((x + 44, y + 9), region, font=cf, fill=(255, 255, 255))
        d.text((x + w - d.textlength(src, font=cf) - 10, y + 8), src, font=cf, fill=acc)
        icon(d, kind, x + w - 62, y + 30, 54, ink, acc)
        d.text((x + 10, y + 32), head, font=fb(25), fill=ink)
        d.text((x + 10, y + 62), deck, font=fr(14), fill=acc)
    else:
        d.text((x + w - d.textlength(src, font=cf) - 10, y + 8), src, font=cf, fill=acc)
        ly = y + 36
        for ln in wrap(d, head, fb(24), w - 20):
            d.text((x + 10, ly), ln, font=fb(24), fill=ink)
            ly += 28
        for ln in wrap(d, deck, fr(14), w - 20):
            d.text((x + 10, ly + 2), ln, font=fr(14), fill=acc)
            ly += 18


def dotted_map(d, x, y, ink):
    """Original dotted world map with numbered pins = card numbers."""
    d.rectangle([x, y, x + 360, y + 84], outline=(17, 17, 17), width=1)
    d.text((x + 8, y + 4), "DOTTED MAP - NUMBERED PINS MARK EACH STORY", font=fb(11), fill=ink)
    blobs = [(70, 42, 34, 16), (105, 74, 14, 18), (185, 36, 22, 11), (192, 62, 20, 20),
             (245, 40, 46, 17), (272, 66, 16, 10), (322, 78, 15, 9)]
    for (bx, byy, rx, ry) in blobs:
        for ddx in range(0, 354, 7):
            for ddy in range(0, 58, 7):
                ex, ey = x + 6 + ddx, y + 22 + ddy
                if ((ex - (x + bx)) ** 2) / (rx * rx) + ((ey - (y + byy)) ** 2) / (ry * ry) <= 1:
                    d.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=(150, 150, 150))
    for (num, px_, py_) in PINS:
        cxp, cyp = x + px_, y + py_
        d.ellipse([cxp - 8, cyp - 8, cxp + 8, cyp + 8], fill=ink)
        s = str(num)
        d.text((cxp - d.textlength(s, font=fb(10)) / 2, cyp - 6), s, font=fb(10), fill=(255, 255, 255))


def build(variant, out):
    if variant == "a":
        bg, ink, acc, paper = (255, 255, 255), (122, 14, 20), (17, 17, 17), (250, 244, 238)
    elif variant == "b":
        bg, ink, acc, paper = (251, 246, 236), (122, 14, 20), (60, 70, 90), (255, 252, 246)
    else:
        bg, ink, acc, paper = (255, 255, 255), (17, 17, 17), (122, 14, 20), (244, 240, 235)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    kick = "40 STORIES \u00b7 8 REGIONS \u00b7 EVERY ONE FROM 23 NOVEMBER 2026"
    kf = fb(14)
    d.text(((W - d.textlength(kick, font=kf)) / 2, 12), kick, font=kf, fill=acc)
    d.line([M, 36, W - M, 36], fill=acc, width=2)

    mf = F(PF_BLACK, 92)
    title = "THE FRONT PAGE"
    while d.textlength(title, font=mf) > W - 2 * M - 10:
        mf = F(PF_BLACK, mf.size - 4)
    d.text(((W - d.textlength(title, font=mf)) / 2, 42), title, font=mf, fill=ink)
    df = F(PF_BOLD, 32)
    date = "Monday 23 November 2026"
    if variant == "c":
        d.rectangle([M, 140, W - M, 182], fill=ink)
        d.text(((W - d.textlength(date, font=df)) / 2, 146), date, font=df, fill=(255, 255, 255))
    else:
        d.text(((W - d.textlength(date, font=df)) / 2, 142), date, font=df, fill=acc)
    d.line([M, 186, W - M, 186], fill=acc, width=4)

    nf, lf = fb(24), fr(11)
    bw = (W - 2 * M - 5 * 6) / 6
    for i, (num, lab) in enumerate(NUMS):
        x = M + i * (bw + 6)
        d.rectangle([x, 194, x + bw, 256], fill=paper, outline=acc, width=1)
        tw = d.textlength(num, font=nf)
        d.text((x + (bw - tw) / 2, 199), num, font=nf, fill=ink)
        for j, ln in enumerate(lab.split("\n")):
            tw = d.textlength(ln, font=lf)
            d.text((x + (bw - tw) / 2, 228 + j * 13), ln, font=lf, fill=acc)
    d.line([M, 262, W - M, 262], fill=acc, width=2)

    main_r = 674
    lead(d, M, 270, 400, 140, 1, "NORTH AMERICA", "BBC",
         "US Army to Detonate Unstable Explosives in Iowa",
         "US Army to blow up unstable explosives in Iowa.", "burst", ink, acc)
    mini(d, 434, 270, main_r - 434, 140, 2, "NORTH AMERICA", "BBC",
         "Democrats Take the House 258-173",
         "Biggest House majority since 1992 after flipping a North Carolina seat.",
         "ballot", ink, acc)
    mini(d, M, 418, main_r - M, 86, 3, "SOUTH ASIA", "OBSERVERVOICE",
         "India Post Record 720/9d at Wellington",
         "Highest Test total in New Zealand, declared against the hosts at Wellington.",
         "cricket", ink, acc, wide=True)

    gx, gy, gw, gh, gap = M, 512, 210, 112, 9
    for idx, (num, region, topic, src, head, deck, kind) in enumerate(grid):
        cx = gx + (idx % 3) * (gw + gap)
        cy = gy + (idx // 3) * (gh + 6)
        d.rectangle([cx, cy, cx + gw, cy + gh], outline=acc, width=1)
        d.rectangle([cx, cy, cx + 24, cy + 24], fill=ink)
        d.text((cx + 5, cy + 3), str(num), font=fb(15), fill=(255, 255, 255))
        cw = d.textlength(region, font=fb(9))
        d.rectangle([cx + 28, cy + 4, cx + 32 + cw, cy + 20], fill=REGIONS[region])
        d.text((cx + 30, cy + 6), region, font=fb(9), fill=(255, 255, 255))
        d.text((cx + gw - d.textlength(src, font=fb(9)) - 6, cy + 6), src, font=fb(9), fill=ink)
        icon(d, kind, cx + gw - 32, cy + gh - 30, 26, ink, acc)
        ly = cy + 26
        for ln in wrap(d, head, fb(24), gw - 14)[:2]:
            d.text((cx + 7, ly), ln, font=fb(24), fill=ink)
            ly += 26
        for ln in wrap(d, deck, fr(14), gw - 42)[:2]:
            d.text((cx + 7, ly), ln, font=fr(14), fill=acc)
            ly += 16

    by = 868
    dotted_map(d, M, by, ink)
    dx = 394
    d.rectangle([dx, by, main_r, by + 84], outline=(200, 30, 30), width=2)
    d.text((dx + 8, by + 4), "DATE CHECK - NOT 23 NOV, LEFT OUT:", font=fb(12), fill=(200, 30, 30))
    dcf = fr(12)
    for i, item in enumerate(DATE_CHECK):
        d.text((dx + 8, by + 20 + i * 10), "\u00d7 " + item, font=dcf, fill=acc)

    ax, aw = 690, W - M - 690
    d.rectangle([ax, 270, ax + aw, 952], fill=paper, outline=acc, width=1)
    d.text((ax + 10, 278), "ALSO ON THE FRONT PAGE", font=fb(16), fill=ink)
    d.line([ax + 10, 302, ax + aw - 10, 302], fill=ink, width=2)
    af = fsr(13)
    ly = 310
    for i, item in enumerate(BRIEFS):
        d.text((ax + 10, ly), "%d." % (13 + i), font=fb(13), fill=ink)
        d.text((ax + 40, ly), wrap(d, item, af, aw - 48)[0], font=af, fill=acc)
        ly += 19
    ly += 2
    d.line([ax + 10, ly, ax + aw - 10, ly], fill=ink, width=1)
    d.text((ax + 10, ly + 6), "MAP LEGEND - REGION COLOURS", font=fb(11), fill=ink)
    ly += 26
    regs = list(REGIONS.items())
    for i in range(0, len(regs), 2):
        for j in range(2):
            if i + j < len(regs):
                name, col = regs[i + j]
                rx = ax + 10 + j * (aw // 2)
                d.rectangle([rx, ly + 2, rx + 10, ly + 12], fill=col)
                d.text((rx + 14, ly), name, font=fr(10), fill=acc)
        ly += 15

    ty = 958
    d.line([M, ty, W - M, ty], fill=acc, width=2)
    d.text((M, ty + 5), "TIMELINE (UTC)", font=fb(12), fill=ink)
    tx = M + 108
    tw = (W - M - tx) / 5
    tf_ = fr(12)
    for i, (slot, ev) in enumerate(TL):
        sx = tx + i * tw
        d.text((sx, ty + 5), slot, font=fb(12), fill=ink)
        d.text((sx, ty + 21), wrap(d, ev, tf_, tw - 8)[0], font=tf_, fill=acc)

    d.line([M, 996, W - M, 996], fill=acc, width=2)
    foot = ("Every story happened, or was first reported, on Monday 23 November 2026. "
            "Contested claims are attributed. \u00b7 Original drawings.")
    ff2 = fr(11)
    d.text(((W - d.textlength(foot, font=ff2)) / 2, 1002), foot, font=ff2, fill=acc)

    img.save(out)
    print("saved", out, img.size)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
