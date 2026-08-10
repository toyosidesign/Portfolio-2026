#!/usr/bin/env python3
"""Condueet 'empty & loading, made intentional' — dark+pink diagram.
Same Logs surface in two honest states: a designed empty state and a
layout-holding loading skeleton."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1500
BG      = (11, 10, 10)
PANEL   = (17, 15, 14)
SUB     = (26, 23, 21)
BORDER  = (44, 40, 36)
BORDER2 = (58, 53, 47)
WHITE   = (245, 244, 242)
GRAY    = (154, 150, 143)
DIM     = (111, 107, 100)
PINK    = (255, 216, 228)
SKEL    = (40, 37, 34)
SKEL2   = (52, 48, 44)

F  = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FI = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
def f(p, s): return ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def rr(box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def text(xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def panel(x0, y0, x1, y1, state):
    rr([x0, y0, x1, y1], 24, fill=PANEL, outline=BORDER, width=2)
    ix0, ix1 = x0 + 44, x1 - 44
    # header
    d.ellipse([ix0, y0 + 40, ix0 + 22, y0 + 62], outline=PINK, width=3)
    text((ix0 + 36, y0 + 38), "Logs", f(FB, 32), WHITE)
    # state badge
    label = "EMPTY" if state == "empty" else "LOADING"
    bw = 150
    rr([ix1 - bw, y0 + 38, ix1, y0 + 76], 19, fill=SUB, outline=BORDER2, width=2)
    text(((ix1 - bw + ix1) / 2, y0 + 57), label, f(FB, 22), PINK, anchor="mm")
    d.line([ix0, y0 + 100, ix1, y0 + 100], fill=BORDER, width=2)

    # stat row (present in both states, layout held steady)
    stats = ["Requests today", "Error rate", "p95 latency"]
    gap = 24
    cw = (ix1 - ix0 - 2 * gap) / 3
    sy0, sy1 = y0 + 128, y0 + 250
    for i, lab in enumerate(stats):
        cx0 = ix0 + i * (cw + gap)
        rr([cx0, sy0, cx0 + cw, sy1], 14, fill=SUB, outline=BORDER, width=2)
        if state == "empty":
            text((cx0 + 24, sy0 + 22), lab, f(F, 22), DIM)
            text((cx0 + 24, sy0 + 56), "—", f(FB, 40), (70, 66, 61))
        else:
            rr([cx0 + 24, sy0 + 28, cx0 + 24 + cw * 0.55, sy0 + 46], 9, fill=SKEL)
            rr([cx0 + 24, sy0 + 64, cx0 + 24 + cw * 0.4, sy0 + 96], 9, fill=SKEL2)

    # content zone
    zy0, zy1 = y0 + 288, y1 - 44
    if state == "empty":
        cx = (ix0 + ix1) / 2
        cy = zy0 + 150
        # icon: a log/receipt card with lines
        iw, ih = 92, 108
        rr([cx - iw/2, cy - ih/2, cx + iw/2, cy + ih/2], 12, outline=PINK, width=3)
        for k in range(3):
            ly = cy - 26 + k * 24
            d.line([cx - 24, ly, cx + 24, ly], fill=PINK, width=3)
        # headline + subtext
        text((cx, cy + 96), "No requests yet", f(FB, 40), WHITE, anchor="ma")
        text((cx, cy + 150), "Make your first call and it lands here,", f(F, 25), GRAY, anchor="ma")
        text((cx, cy + 184), "with the full request and response.", f(F, 25), GRAY, anchor="ma")
        # pink button
        btw, bth = 300, 64
        bx0, by0b = cx - btw/2, cy + 236
        rr([bx0, by0b, bx0 + btw, by0b + bth], 13, fill=PINK)
        text((cx, by0b + bth/2), "Go to Quickstart", f(FB, 27), (30, 16, 22), anchor="mm")
        # caption
        text((cx, zy1 - 30), "designed, not a blank page", f(FI, 23), DIM, anchor="ma")
    else:
        # skeleton request rows — same list layout the data will fill
        ry = zy0 + 10
        for i in range(6):
            rr([ix0, ry, ix1, ry + 84], 12, fill=SUB, outline=BORDER, width=2)
            # status pill
            rr([ix0 + 22, ry + 27, ix0 + 96, ry + 57], 15, fill=SKEL2)
            # path bar (varied width per row so it reads live)
            pw = [0.52, 0.44, 0.6, 0.5, 0.4, 0.56][i]
            rr([ix0 + 120, ry + 30, ix0 + 120 + (ix1 - ix0) * pw, ry + 52], 9, fill=SKEL)
            # right time bar
            rr([ix1 - 150, ry + 30, ix1 - 40, ry + 52], 9, fill=SKEL2)
            ry += 100
        text(((ix0 + ix1) / 2, zy1 - 30), "a shape, never a spinner", f(FI, 23), DIM, anchor="ma")

M, GAP = 60, 60
pw = (W - 2 * M - GAP) / 2
PY0, PY1 = 96, 1360
panel(M, PY0, M + pw, PY1, "empty")
panel(M + pw + GAP, PY0, W - M, PY1, "loading")

# footer note
text((W / 2, PY1 + 56),
     "SAME VIEW, TWO HONEST STATES   ·   EMPTY EXPLAINS ITSELF   ·   LOADING HOLDS THE LAYOUT",
     f(FB, 24), DIM, anchor="mm")

img.save("/Users/macbookpro/Desktop/Portfolio-2026/assets/condueet-v2-states-empty-loading.png")
print("saved", img.size)
