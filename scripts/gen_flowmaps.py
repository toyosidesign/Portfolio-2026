#!/usr/bin/env python3
"""Condueet flow maps — one rail per seat, dark+pink.
Exact per-role sidebar pages; Wallet & Settings pinned on every rail."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1350
BG      = (11, 10, 10)
PANEL   = (17, 15, 14)
NODE    = (26, 23, 21)
BORDER  = (44, 40, 36)
BORDER2 = (58, 53, 47)
WHITE   = (245, 244, 242)
GRAY    = (154, 150, 143)
DIM     = (111, 107, 100)
PINK    = (255, 216, 228)
PINKDIM = (150, 120, 130)
PINKBG  = (36, 27, 31)

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

# shared surfaces that appear on more than one rail
SHARED = {"API Reference", "Webhooks"}

cols = [
    ("DEVELOPER", "Prove it works",
     ["Quickstart", "Link Flow", "Workbench", "Logs", "API", "API Reference", "Webhooks"]),
    ("BUSINESS", "Keep it flowing",
     ["Overview", "Customers", "Reports", "Activation"]),
    ("OWNER", "Hold the risk",
     ["Team", "API Keys", "API Reference", "Webhooks", "Billing", "Audit Log"]),
]

MARGIN = 70
GAP = 54
CW = (W - 2 * MARGIN - 2 * GAP) / 3     # column width
PY0, PY1 = 96, 1262                      # panel top/bottom
NODE_H = 60
PITCH = 90                              # node-to-node vertical pitch
FLOW_TOP = PY0 + 172                     # first node y
PIN_TOP = 1044                           # pinned group top (aligned across cols)

for ci, (role, tag, pages) in enumerate(cols):
    x0 = MARGIN + ci * (CW + GAP)
    x1 = x0 + CW
    rr([x0, PY0, x1, PY1], 22, fill=PANEL, outline=BORDER, width=2)

    # header
    d.ellipse([x0 + 34, PY0 + 40, x0 + 58, PY0 + 64], fill=PINK)
    text((x0 + 74, PY0 + 38), role, f(FB, 30), PINK)
    text((x0 + 74, PY0 + 82), tag, f(FI, 24), GRAY)
    d.line([x0 + 34, PY0 + 130, x1 - 34, PY0 + 130], fill=BORDER, width=2)

    nx0, nx1 = x0 + 40, x1 - 40
    # flow nodes
    for i, page in enumerate(pages):
        ny = FLOW_TOP + i * PITCH
        shared = page in SHARED
        entry = (i == 0)
        fill = PINKBG if entry else NODE
        oc = PINK if (entry or shared) else BORDER2
        rr([nx0, ny, nx1, ny + NODE_H], 14, fill=fill, outline=oc, width=2)
        # marker dot
        mc = PINK if entry else (PINKDIM if shared else GRAY)
        d.ellipse([nx0 + 26, ny + NODE_H/2 - 6, nx0 + 38, ny + NODE_H/2 + 6],
                  fill=mc if entry else None, outline=mc, width=3)
        text((nx0 + 62, ny + NODE_H/2), page, f(FB, 27), WHITE, anchor="lm")
        if shared:
            text((nx1 - 24, ny + NODE_H/2), "shared", f(FI, 20), PINKDIM, anchor="rm")
        # connector arrow to next
        if i < len(pages) - 1:
            cx = nx0 + 32
            ay0 = ny + NODE_H
            ay1 = ny + PITCH
            d.line([cx, ay0, cx, ay1], fill=BORDER2, width=3)
            d.polygon([(cx - 6, ay1 - 9), (cx + 6, ay1 - 9), (cx, ay1 - 1)], fill=BORDER2)

    # pinned group: Wallet + Settings
    d.line([nx0, PIN_TOP - 26, nx1, PIN_TOP - 26], fill=BORDER, width=2)
    text((nx0, PIN_TOP - 20), "PINNED", f(FB, 18), DIM)
    for j, page in enumerate(["Wallet", "Settings"]):
        ny = PIN_TOP + 6 + j * 74
        rr([nx0, ny, nx1, ny + 58], 14, fill=NODE, outline=BORDER, width=2)
        d.rounded_rectangle([nx0 + 24, ny + 20, nx0 + 40, ny + 38], radius=4,
                            outline=PINK, width=3)
        text((nx0 + 60, ny + 29), page, f(FB, 26), GRAY, anchor="lm")

# footer note
text((W/2, PY1 + 44), "WALLET · SETTINGS PINNED ON EVERY RAIL   ·   API REFERENCE + WEBHOOKS SHARED ACROSS SEATS",
     f(FB, 22), DIM, anchor="mm")

img.save("/Users/macbookpro/Desktop/Portfolio-2026/assets/condueet-v2-flowmaps.png")
print("saved", img.size)
