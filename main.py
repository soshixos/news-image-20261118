#!/usr/bin/env python3
"""THE WORLD TODAY - Wednesday 18 November 2026.

A one-page newspaper front page, drawn procedurally with the
standard library only. Writes entry.png to $MAKEFUN_OUTPUT_DIR
(or ./out). No network, no assets, no timestamps: two runs
produce byte-identical output."""

import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (25, 25, 25)
RED = (166, 30, 34)
BLUE = (31, 78, 121)
DOT = (74, 74, 74)
GRAY = (112, 110, 102)

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, one 5-bit row per line, MSB on the left.
def _g(*rows):
    return tuple(int(r, 2) for r in rows)

FONT = {
    "A": _g("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": _g("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": _g("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": _g("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": _g("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": _g("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": _g("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": _g("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": _g("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": _g("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": _g("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": _g("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": _g("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": _g("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": _g("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": _g("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": _g("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": _g("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": _g("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": _g("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": _g("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": _g("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": _g("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": _g("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": _g("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": _g("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": _g("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": _g("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": _g("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": _g("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": _g("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": _g("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": _g("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": _g("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": _g("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": _g("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": _g("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": _g("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": _g("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": _g("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": _g("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": _g("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": _g("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": _g("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': _g("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": _g("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": _g("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": _g("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": _g("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": _g("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": _g("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": _g("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "&": _g("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "$": _g("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "#": _g("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": _g("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "·": _g("00000", "00000", "00000", "01100", "01100", "00000", "00000"),
    "—": _g("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "×": _g("00000", "10001", "01010", "00100", "01010", "10001", "00000"),
}

# ---------------------------------------------------------------- map
# Coarse world land grid: 100 columns (lon -180..180), 30 rows
# (lat 77..-56). Each entry is a list of inclusive column ranges.
LAND = {
    0: [(6, 12), (18, 30), (38, 42), (54, 58), (66, 95)],
    1: [(4, 12), (14, 32), (37, 43), (52, 55), (60, 96)],
    2: [(3, 12), (13, 34), (36, 44), (50, 56), (58, 97)],
    3: [(2, 12), (12, 36), (44, 44), (50, 57), (58, 98)],
    4: [(2, 11), (12, 38), (45, 46), (51, 58), (58, 98)],
    5: [(3, 8), (12, 40), (45, 47), (48, 60), (60, 98)],
    6: [(12, 42), (46, 62), (62, 98)],
    7: [(10, 42), (45, 60), (62, 90), (93, 95)],
    8: [(8, 42), (46, 58), (60, 92), (94, 96)],
    9: [(8, 40), (45, 58), (58, 66), (70, 90), (94, 95)],
    10: [(8, 38), (45, 58), (58, 68), (70, 76), (78, 86), (88, 92)],
    11: [(6, 14), (14, 38), (44, 58), (60, 66), (70, 76), (78, 88)],
    12: [(6, 12), (16, 22), (44, 60), (60, 67), (70, 77), (78, 88)],
    13: [(8, 14), (44, 62), (71, 75), (78, 88)],
    14: [(10, 14), (44, 50), (56, 64), (71, 74), (79, 88)],
    15: [(10, 16), (44, 50), (58, 64), (80, 88)],
    16: [(12, 20), (44, 49), (50, 58), (80, 90)],
    17: [(13, 18), (20, 30), (45, 58), (80, 92), (93, 97)],
    18: [(14, 18), (20, 32), (46, 58), (81, 90), (93, 96)],
    19: [(15, 33), (47, 57), (82, 89)],
    20: [(17, 34), (47, 56), (60, 61), (84, 92)],
    21: [(18, 34), (47, 55), (60, 61), (82, 94)],
    22: [(19, 33), (47, 54), (80, 95)],
    23: [(20, 32), (48, 53), (79, 95)],
    24: [(20, 28), (48, 52), (80, 94), (96, 97)],
    25: [(20, 26), (82, 92), (96, 96)],
    26: [(21, 24), (88, 90)],
    27: [(21, 23)],
    28: [(21, 22)],
    29: [(21, 21)],
}

# (grid col, grid row, label) for the numbered story markers.
MARKERS = [
    (81, 12, "1"),  # Shenzhen - APEC opens
    (83, 13, "2"),  # Manila - QUAD
    (60, 7, "3"),   # Kerch - bridge aftermath
    (64, 11, "4"),  # Bahrain - Gulf drones
    (29, 8, "5"),   # New York - markets
    (72, 13, "6"),  # Andhra Pradesh - cyclone
    (82, 8, "7"),   # Beijing - Canada-China trade
    (50, 5, "8"),   # London - sanctions
]

# ---------------------------------------------------------------- canvas
px = bytearray(bytes(PAPER) * W * H)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = color


def fill_rect(x, y, w, h, color):
    for yy in range(y, y + h):
        if 0 <= yy < H:
            xa = max(x, 0)
            xb = min(x + w, W)
            if xb > xa:
                i = (yy * W + xa) * 3
                px[i:(yy * W + xb) * 3] = bytes(color) * (xb - xa)


def hline(x, y, w, color, t=1):
    fill_rect(x, y, w, t, color)


def text_width(text, scale):
    return (len(text) * 6 - 1) * scale if text else 0


def draw_text(x, y, text, scale, color, align="left"):
    text = text.upper()
    if align == "center":
        x -= text_width(text, scale) // 2
    elif align == "right":
        x -= text_width(text, scale)
    cx = x
    for ch in text:
        glyph = FONT.get(ch)
        if glyph:
            for r, bits in enumerate(glyph):
                for c in range(5):
                    if bits & (1 << (4 - c)):
                        fill_rect(cx + c * scale, y + r * scale, scale, scale, color)
        cx += 6 * scale


def wrap(text, scale, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        fill_rect(cx - dx, cy + dy, dx * 2 + 1, 1, color)


# ---------------------------------------------------------------- page
def draw():
    # outer frame
    fill_rect(8, 8, W - 16, 3, INK)
    fill_rect(8, H - 11, W - 16, 3, INK)
    fill_rect(8, 8, 3, H - 16, INK)
    fill_rect(W - 11, 8, 3, H - 16, INK)

    # masthead
    draw_text(W // 2, 26, "THE WORLD TODAY", 9, INK, "center")
    hline(24, 100, W - 48, INK, 2)

    # dateline
    draw_text(24, 110, "WEDNESDAY, 18 NOVEMBER 2026", 2, INK)
    draw_text(W - 24, 110, "6 CONTINENTS · ONE FRONT PAGE", 2, INK, "right")

    # markets ticker
    fill_rect(24, 132, W - 48, 28, INK)
    draw_text(
        W // 2, 140,
        "DOW -849 · S&P 500 LOWEST SINCE LATE JULY · NVIDIA SALES DOUBLE TO $115.8BN",
        2, PAPER, "center",
    )

    # lead headline + deck
    draw_text(W // 2, 174, "THREE SUMMITS, ONE DAY", 6, RED, "center")
    draw_text(W // 2, 226, "APEC OPENS IN SHENZHEN · TRUMP IN MANILA FOR QUAD", 3, INK, "center")
    draw_text(W // 2, 252, "XI, TRUMP AND PUTIN MEET TOMORROW", 3, INK, "center")

    # dotted world map
    mx, my, sx, sy = 28, 288, 9.7, 9.2
    for row, ranges in LAND.items():
        for c0, c1 in ranges:
            for c in range(c0, c1 + 1):
                dx = int(mx + c * sx)
                dy = int(my + row * sy)
                fill_rect(dx - 2, dy - 2, 5, 5, DOT)
    for c, r, label in MARKERS:
        cx = int(mx + c * sx)
        cy = int(my + r * sy)
        draw_circle(cx, cy, 10, RED)
        draw_text(cx, cy - 7, label, 2, PAPER, "center")

    # map legend
    draw_text(W // 2, 574, "1 SHENZHEN · 2 MANILA · 3 KERCH · 4 BAHRAIN · 5 NEW YORK", 2, GRAY, "center")
    draw_text(W // 2, 592, "6 ANDHRA PRADESH · 7 BEIJING · 8 LONDON", 2, GRAY, "center")

    hline(24, 614, W - 48, INK, 2)

    # story grid: 2 x 2
    stories = [
        (24, 626, "3 · BRIDGE AFTERMATH",
         "KERCH ROAD SPAN DOWN, RAIL PARTLY BACK. KREMLIN VOWS REBUILD \"EVEN BETTER\". RECORD 1,441-DRONE NIGHT."),
        (528, 626, "4 · GULF ON EDGE",
         "DRONES OVER BAHRAIN AND KUWAIT OVERNIGHT. US AND IRAN TRADE STRIKES ON QESHM AND BAHRAIN. BAHRAIN ALL-CLEAR."),
        (24, 746, "5 · MARKETS TUMBLE",
         "DOW -849 IN TECH ROUT BEFORE NVIDIA RESULTS. NVIDIA SALES DOUBLE TO $115.8BN, BOARD BARS HUANG RETURN."),
        (528, 746, "6 · CYCLONE AKVAN",
         "STORM BEARS DOWN ON ANDHRA PRADESH, LANDFALL DUE 20 NOV. DHONI RETIRES FROM IPL, BECOMES CSK MENTOR."),
    ]
    for x, y, head, body in stories:
        draw_text(x, y, head, 3, RED)
        lines = wrap(body, 2, 472)
        for i, line in enumerate(lines[:4]):
            draw_text(x, y + 30 + i * 17, line, 2, INK)
    # grid rules
    fill_rect(511, 626, 2, 238, GRAY)
    hline(24, 736, W - 48, GRAY, 1)

    # in brief
    draw_text(24, 878, "IN BRIEF", 3, RED)
    brief = ("CANADA AND CHINA EXTEND TRADE DEALS AS XI MEETS CARNEY · BRITAIN SANCTIONS "
             "ISRAELI SETTLEMENT FIRMS · BOARD OF PEACE WARNS GAZA CEASEFIRE FACES "
             "\"IMMINENT COLLAPSE\" · UN: 372 CIVILIANS KILLED IN UKRAINE IN OCTOBER · "
             "AMAZON PUTS $7BN INTO INDIA RENEWABLES")
    for i, line in enumerate(wrap(brief, 2, W - 48)):
        draw_text(24, 906 + i * 17, line, 2, INK)

    # footer
    hline(24, 982, W - 48, INK, 2)
    draw_text(W // 2, 992, "THE WORLD TODAY · WEDNESDAY, 18 NOVEMBER 2026 · ALL STORIES REPORTED TODAY",
              2, GRAY, "center")


# ---------------------------------------------------------------- png
def chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    return out + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def save_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += px[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


def main():
    draw()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(outdir, exist_ok=True)
    save_png(os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
