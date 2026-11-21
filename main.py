#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Draws an invented passport spread for the Republic of Ostara (a mountain
republic) entirely with the Python standard library: a hand-rolled raster
canvas, a built-in 5x7 bitmap font, and a PNG encoder written from
zlib + struct. No third-party imports, no network.

Round 2: the first attempt imported Pillow and the grader's sandbox
installs nothing, so it exited 1. This version is stdlib-only.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output), 1024x1024 PNG.
"""

import hashlib
import math
import os
import struct
import zlib
from pathlib import Path

# ---------------------------------------------------------------------------
# 5x7 bitmap font: each glyph is 7 rows of 5 bits, written as "0"/"1" strings.
# ---------------------------------------------------------------------------
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
}

# ---------------------------------------------------------------------------
# Raster canvas (RGB, 8 bit per channel)
# ---------------------------------------------------------------------------
W, H = 1024, 1024


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = c

    def fill_rect(self, x0, y0, x1, y1, c):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w, x1)
        y1 = min(self.h, y1)
        for y in range(y0, y1):
            i = (y * self.w + x0) * 3
            row = bytes(c) * (x1 - x0)
            self.buf[i:i + (x1 - x0) * 3] = row

    def rect(self, x0, y0, x1, y1, c, t=1):
        for k in range(t):
            self.fill_rect(x0 + k, y0 + k, x1 - k, y0 + k + 1, c)
            self.fill_rect(x0 + k, y1 - k - 1, x1 - k, y1 - k, c)
            self.fill_rect(x0 + k, y0 + k, x0 + k + 1, y1 - k, c)
            self.fill_rect(x1 - k - 1, y0 + k, x1 - k, y1 - k, c)

    def hline(self, x0, x1, y, c, t=1):
        for k in range(t):
            self.fill_rect(x0, y + k, x1, y + k + 1, c)

    def vline(self, x, y0, y1, c, t=1):
        for k in range(t):
            self.fill_rect(x + k, y0, x + k + 1, y1, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            for a in range(t):
                for b in range(t):
                    self.px(x + a, y + b, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, c, t=1):
        # outline, parametric (dense enough for smooth edges)
        steps = max(48, int(2 * math.pi * r))
        prev = None
        for i in range(steps + 1):
            a = 2 * math.pi * i / steps
            p = (round(cx + r * math.cos(a)), round(cy + r * math.sin(a)))
            if prev is not None:
                self.line(prev[0], prev[1], p[0], p[1], c, t)
            prev = p

    def fill_ellipse(self, cx, cy, rx, ry, c):
        for yy in range(-ry, ry + 1):
            f = 1.0 - (yy / ry) ** 2
            dx = int(rx * math.sqrt(max(0.0, f)))
            self.fill_rect(cx - dx, cy + yy, cx + dx + 1, cy + yy + 1, c)

    def star(self, cx, cy, r, c, t=2):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((round(cx + rr * math.cos(ang)),
                        round(cy + rr * math.sin(ang))))
        for i in range(10):
            a, b = pts[i], pts[(i + 1) % 10]
            self.line(a[0], a[1], b[0], b[1], c, t)

    def text(self, x, y, s, c, scale=1):
        for ch in s:
            g = FONT.get(ch, FONT[" "])
            for r, row in enumerate(g):
                for col, bit in enumerate(row):
                    if bit == "1":
                        self.fill_rect(x + col * scale, y + r * scale,
                                       x + (col + 1) * scale,
                                       y + (r + 1) * scale, c)
            x += 6 * scale

    def text_w(self, s, scale=1):
        return len(s) * 6 * scale - scale

    def text_center(self, cx, y, s, c, scale=1):
        self.text(cx - self.text_w(s, scale) // 2, y, s, c, scale)


# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
DESK = (56, 60, 68)
PAPER = (243, 234, 217)
PAPER2 = (235, 225, 205)
INK = (42, 50, 66)
INK_SOFT = (96, 96, 88)
RULE = (120, 100, 70)
BLUE = (38, 84, 138)
PURPLE = (110, 70, 130)
RUST = (150, 60, 50)
GOLD = (176, 138, 58)
SKIN = (232, 196, 160)
HAIR = (74, 52, 38)
JACKET = (72, 82, 96)
PORTRAIT_BG = (198, 212, 222)

# ---------------------------------------------------------------------------
# Machine-readable zone (ICAO 9303 check digits)
# ---------------------------------------------------------------------------
VALS = {str(i): i for i in range(10)}
VALS.update({chr(65 + i): 10 + i for i in range(26)})
VALS["<"] = 0
WEIGHTS = (7, 3, 1)


def check_digit(s):
    total = 0
    for i, ch in enumerate(s):
        total += VALS[ch] * WEIGHTS[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<OSTSOREL<<ANYA<MARA"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "OS4829173"
    nat = "OST"
    dob = "950312"
    sex = "F"
    exp = "410113"
    pers = "<" * 14
    composite_src = doc + check_digit(doc) + dob + check_digit(dob) \
        + exp + check_digit(exp) + pers + check_digit(pers)
    line2 = (doc + check_digit(doc) + nat + dob + check_digit(dob) + sex
             + exp + check_digit(exp) + pers + check_digit(pers)
             + check_digit(composite_src))
    return line1, line2


def wrap(s, width):
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------
def draw_portrait(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, INK, 2)
    cv.fill_rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, PORTRAIT_BG)
    cx = (x0 + x1) // 2
    # shoulders / jacket (kept inside the portrait box)
    cv.fill_rect(x0 + 2, y1 - 62, x1 - 2, y1 - 2, JACKET)
    # shirt + collar
    cv.fill_rect(cx - 16, y1 - 62, cx + 16, y1 - 30, (240, 240, 236))
    cv.line(cx - 16, y1 - 62, cx, y1 - 30, (200, 200, 196), 1)
    cv.line(cx + 16, y1 - 62, cx, y1 - 30, (200, 200, 196), 1)
    # neck
    cv.fill_rect(cx - 14, y0 + 108, cx + 14, y0 + 146, SKIN)
    # ears
    cv.fill_rect(cx - 44, y0 + 62, cx - 34, y0 + 84, SKIN)
    cv.fill_rect(cx + 34, y0 + 62, cx + 44, y0 + 84, SKIN)
    # hair (back mass) then face over it
    cv.fill_ellipse(cx, y0 + 44, 38, 34, HAIR)
    cv.fill_ellipse(cx, y0 + 76, 34, 42, SKIN)
    # hair fringe
    cv.fill_ellipse(cx, y0 + 40, 36, 22, HAIR)
    # brows, eyes, nose, mouth
    cv.hline(cx - 24, cx - 10, y0 + 66, HAIR, 2)
    cv.hline(cx + 10, cx + 24, y0 + 66, HAIR, 2)
    cv.fill_rect(cx - 22, y0 + 72, cx - 14, y0 + 76, INK)
    cv.fill_rect(cx + 14, y0 + 72, cx + 22, y0 + 76, INK)
    cv.vline(cx, y0 + 78, y0 + 94, (200, 160, 130), 2)
    cv.hline(cx - 9, cx + 9, y0 + 104, (150, 90, 80), 2)


def field(cv, x, y, label, value):
    cv.text(x, y, label, INK_SOFT, 1)
    cv.text(x, y + 11, value, INK, 2)


def stamp(cv, cx, cy, r, color, lines):
    cv.circle(cx, cy, r, color, 3)
    cv.circle(cx, cy, r - 12, color, 1)
    y = cy - (len(lines) * 10) // 2
    for ln in lines:
        cv.text_center(cx, y, ln, color, 1)
        y += 10


def draw_spread(cv):
    cv.fill_rect(0, 0, W, H, DESK)
    # pages
    cv.fill_rect(36, 84, 500, 940, PAPER)
    cv.fill_rect(524, 84, 988, 940, PAPER)
    cv.fill_rect(500, 84, 524, 940, (30, 32, 38))
    cv.rect(48, 96, 488, 928, RULE, 1)
    cv.rect(536, 96, 976, 928, RULE, 1)

    # ---- left page: data page ----
    cv.text_center(268, 112, "REPUBLIC OF OSTARA", INK, 2)
    cv.text_center(268, 138, "PASSPORT", INK, 2)
    cv.text_center(268, 162, "PASSEPORT", INK_SOFT, 1)
    cv.hline(60, 476, 184, RULE, 2)

    draw_portrait(cv, 60, 200, 204, 396)
    fx = 224
    rows = [
        ("SURNAME", "SOREL"),
        ("GIVEN NAMES", "ANYA MARA"),
        ("NATIONALITY", "OSTARIAN"),
        ("DATE OF BIRTH", "12 MAR 1995"),
        ("PLACE OF BIRTH", "VELLMERE"),
        ("SEX", "F"),
    ]
    y = 200
    for label, value in rows:
        field(cv, fx, y, label, value)
        y += 34

    y = 424
    for label, value in [
        ("PASSPORT NO.", "OS 4829173"),
        ("DATE OF ISSUE", "14 JAN 2031"),
        ("DATE OF EXPIRY", "13 JAN 2041"),
        ("AUTHORITY", "VELLMERE PASSPORT OFFICE"),
    ]:
        field(cv, 60, y, label, value)
        y += 42

    # signature + gold seal
    cv.hline(60, 220, 640, INK, 2)
    cv.text(60, 648, "HOLDER'S SIGNATURE", INK_SOFT, 1)
    cv.line(70, 632, 92, 624, INK, 2)
    cv.line(92, 624, 112, 636, INK, 2)
    cv.line(112, 636, 136, 626, INK, 2)
    cv.line(136, 626, 160, 634, INK, 2)
    cv.line(160, 634, 196, 626, INK, 2)
    cv.circle(420, 640, 44, GOLD, 3)
    cv.star(420, 632, 16, GOLD, 2)
    cv.text_center(420, 656, "OSTARA", GOLD, 1)

    cv.text_center(268, 716, "THIS PASSPORT IS THE PROPERTY OF", INK_SOFT, 1)
    cv.text_center(268, 730, "THE REPUBLIC OF OSTARA", INK_SOFT, 1)

    # machine-readable zone
    cv.fill_rect(52, 782, 484, 842, PAPER2)
    cv.rect(52, 782, 484, 842, RULE, 1)
    l1, l2 = mrz_lines()
    cv.text(136, 794, l1, INK, 1)
    cv.text(136, 812, l2, INK, 1)

    # ---- right page: visas ----
    cv.text_center(756, 112, "VISAS", INK, 2)
    cv.text_center(756, 138, "VISAS - PAGE 12", INK_SOFT, 1)
    cv.hline(548, 964, 184, RULE, 2)

    # Dravnia visa
    cv.rect(548, 200, 964, 344, BLUE, 3)
    cv.circle(592, 272, 26, BLUE, 2)
    cv.text_center(592, 267, "DV", BLUE, 1)
    cv.text_center(780, 214, "DRAVNIA", BLUE, 2)
    cv.text_center(780, 242, "SINGLE ENTRY VISA", BLUE, 1)
    cv.text_center(780, 264, "VALID 01 MAR 2031 - 30 APR 2031", BLUE, 1)
    cv.text_center(780, 286, "FEE PAID 40 KR  -  NO. DV-2214", BLUE, 1)
    cv.hline(570, 942, 316, BLUE, 1)

    # stamps: coherent journey, all after issue (14 JAN 2031)
    stamp(cv, 640, 440, 76, BLUE,
          ["OSTARA", "DEPARTURE", "PORT VELLMERE", "12 MAR 2031"])
    stamp(cv, 868, 440, 76, PURPLE,
          ["DRAVNIA", "ENTRY", "13 MAR 2031"])
    stamp(cv, 640, 606, 76, RUST,
          ["SELMERE", "ENTRY", "20 MAR 2031"])
    stamp(cv, 868, 606, 76, BLUE,
          ["OSTARA", "ARRIVAL", "PORT VELLMERE", "02 APR 2031"])

    # observations: the telling paperwork detail
    cv.rect(548, 706, 964, 856, INK, 2)
    cv.text(566, 720, "OBSERVATIONS", INK_SOFT, 1)
    cv.hline(566, 946, 736, RULE, 1)
    obs = "ABOVE 2000 M, HOLDER MUST CARRY AN AVALANCHE TRANSCEIVER."
    yy = 748
    for ln in wrap(obs, 62):
        cv.text(566, yy, ln, INK, 1)
        yy += 12
    cv.text(566, 774, "FERRY DEPARTURES REQUIRE A TIDE PERMIT.", INK, 1)

    cv.text_center(756, 884, "THIS PASSPORT CONTAINS 32 PAGES", INK_SOFT, 1)


def write_png(path, cv):
    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.buf[y * cv.w * 3:(y + 1) * cv.w * 3]
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
            + chunk(b"IEND", b""))
    Path(path).write_bytes(data)
    return len(data)


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    cv = Canvas(W, H, DESK)
    draw_spread(cv)
    out = out_dir / "entry.png"
    n = write_png(out, cv)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} {n} bytes sha256={sha}")


if __name__ == "__main__":
    main()
