#!/usr/bin/env python3
"""Condueet 'Make your first call' shell diagram — dark+pink restyle,
exact data + structure from Inspiration 2."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1350
BG      = (11, 10, 10)
SIDE    = (13, 12, 12)
CARD    = (20, 18, 16)
SUB     = (27, 24, 21)
BORDER  = (44, 40, 36)
BORDER2 = (58, 53, 47)
WHITE   = (245, 244, 242)
GRAY    = (154, 150, 143)
DIM     = (111, 107, 100)
PINK    = (255, 216, 228)
PINKDIM = (120, 96, 104)
GREEN   = (126, 224, 168)
MONO    = (207, 202, 194)

F  = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FI = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FM = "/System/Library/Fonts/SFNSMono.ttf"
def f(p, s): return ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def rr(box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def text(xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

# ---------------- SIDEBAR ----------------
SX0, SX1 = 0, 372
d.rectangle([SX0, 0, SX1, H], fill=SIDE)
d.line([SX1, 0, SX1, H], fill=BORDER, width=2)

# logo
d.ellipse([40, 52, 74, 86], fill=PINK)
text((88, 50), "Condueet", f(FB, 34), WHITE)
# collapse icon
rr([300, 54, 336, 84], 7, outline=BORDER2, width=2)
d.line([318, 54, 318, 84], fill=BORDER2, width=2)

nav = ["Quickstart", "Link flow", "Workbench", "Logs", "API", "Wallet", "Settings"]
ny = 168
ITEM_H = 62
for i, item in enumerate(nav):
    yc = ny + i * ITEM_H
    active = (i == 0)
    if active:
        rr([24, yc, 348, yc + 48], 12, fill=(36, 27, 31))
    ic = PINK if active else GRAY
    # simple glyph
    d.ellipse([48, yc + 16, 68, yc + 36], outline=ic, width=3)
    text((92, yc + 8), item, f(FB if active else F, 27), WHITE if active else GRAY)

# avatar
d.ellipse([40, H - 84, 90, H - 34], fill=(42, 39, 36))
text((65, H - 59), "G", f(FB, 26), GRAY, anchor="mm")

# ---------------- MAIN AREA ----------------
MX = 430
RX = 2340  # right edge of content

# top bar
text((MX, 52), "gofoodie-web", f(FI, 30), GRAY)
tw = d.textlength("gofoodie-web", font=f(FI, 30))
px = MX + tw + 34
rr([px, 48, px + 190, 90], 21, fill=SUB, outline=BORDER, width=2)
d.ellipse([px + 20, 62, px + 36, 78], fill=GRAY)
text((px + 46, 54), "Test mode", f(F, 25), GRAY)

# right cluster of top bar
box_w, box_h = 260, 78
bx1 = RX
bx0 = bx1 - box_w
by0 = 42
rr([bx0, by0, bx1, by0 + box_h], 14, fill=CARD, outline=PINK, width=3)  # pink ring = hero control
text((bx0 + 60, by0 + 12), "VIEWING AS", f(F, 18), DIM)
text((bx0 + 60, by0 + 38), "Developer", f(FB, 28), WHITE)
d.polygon([(bx1 - 40, by0 + 46), (bx1 - 24, by0 + 46), (bx1 - 32, by0 + 56)], fill=GRAY)
# code glyph
text((bx0 + 22, by0 + 30), "</>", f(FB, 22), PINK, anchor="lm")
# links left of it
apx = bx0 - 40
text((apx, by0 + 24), "API reference", f(FB, 25), WHITE, anchor="ra")
apw = d.textlength("API reference", font=f(FB, 25))
text((apx - apw - 40, by0 + 24), "Typically 4 minutes", f(F, 25), GRAY, anchor="ra")
# hero-control caption under dropdown
text((bx1, by0 + box_h + 14), "switches the whole surface", f(FI, 22), PINK, anchor="ra")

# title
text((MX, 150), "Make your first call", f(FB, 66), WHITE)
sub = ["Three steps, all in sandbox. Nothing here bills you, and the data you get",
       "back is shaped exactly like production."]
text((MX, 240), sub[0], f(F, 29), GRAY)
text((MX, 280), sub[1], f(F, 29), GRAY)

# progress (right aligned)
text((RX - 250, 210), "1 of 3 done", f(F, 26), GRAY, anchor="ra")
rr([RX - 230, 214, RX, 236], 11, fill=(40, 37, 34))
rr([RX - 230, 214, RX - 155, 236], 11, fill=GREEN)

# ---------- layout columns ----------
CY = 370
LX0, LX1 = MX, 1690
RX0, RX1 = 1740, RX

# ===== Card 1: sandbox keys =====
c1 = [LX0, CY, LX1, CY + 300]
rr(c1, 20, fill=CARD, outline=BORDER, width=2)
d.ellipse([LX0 + 34, CY + 34, LX0 + 74, CY + 74], fill=GREEN)
text((LX0 + 54, CY + 54), "1", f(FB, 26), (12, 20, 14), anchor="mm")
text((LX0 + 96, CY + 36), "Your sandbox keys", f(FB, 34), WHITE)
text((LX1 - 34, CY + 42), "Ready", f(FB, 26), GREEN, anchor="ra")
text((LX0 + 96, CY + 84), "Already issued. The secret key is only shown here.", f(F, 25), GRAY)

def keyrow(y, label, key):
    rr([LX0 + 34, y, LX1 - 34, y + 66], 12, fill=SUB, outline=BORDER, width=2)
    text((LX0 + 60, y + 20), label, f(F, 24), DIM)
    text((LX0 + 240, y + 16), key, f(FM, 28), MONO)
    bw = 96
    rr([LX1 - 34 - bw - 16, y + 14, LX1 - 50, y + 52], 9, outline=BORDER2, width=2)
    text((LX1 - 34 - bw/2 - 16, y + 33), "Copy", f(F, 23), GRAY, anchor="mm")

keyrow(CY + 138, "Publishable", "pk_test_c47e8820b193")
keyrow(CY + 216, "Secret", "sk_test_9f21c40a7715")

# ===== Card 2: link a test customer =====
c2y = CY + 322
c2 = [LX0, c2y, LX1, c2y + 150]
rr(c2, 20, fill=CARD, outline=BORDER, width=2)
d.ellipse([LX0 + 34, c2y + 46, LX0 + 74, c2y + 86], fill=(46, 42, 38))
text((LX0 + 54, c2y + 66), "2", f(FB, 26), WHITE, anchor="mm")
text((LX0 + 96, c2y + 40), "Link a test customer", f(FB, 34), WHITE)
text((LX0 + 96, c2y + 88), "Opens the consent screen your customers will see.", f(F, 25), GRAY)
# pink button
btn_w = 250
rr([LX1 - 34 - btn_w, c2y + 48, LX1 - 34, c2y + 104], 12, fill=PINK)
text((LX1 - 34 - btn_w/2, c2y + 76), "Open link flow", f(FB, 26), (30, 16, 22), anchor="mm")

# ===== Card 3: pull the account =====
c3y = c2y + 172
c3 = [LX0, c3y, LX1, c3y + 452]
rr(c3, 20, fill=CARD, outline=BORDER, width=2)
d.ellipse([LX0 + 34, c3y + 34, LX0 + 74, c3y + 74], outline=BORDER2, width=3)
text((LX0 + 54, c3y + 54), "3", f(FB, 26), GRAY, anchor="mm")
text((LX0 + 96, c3y + 36), "Pull the account", f(FB, 34), WHITE)
text((LX0 + 96, c3y + 84), "Your key and the linked account are already filled in.", f(F, 25), GRAY)
# tabs
tabs = ["cURL", "Node", "Python"]
tabw = 260
tab0 = LX1 - 34 - tabw
rr([tab0, c3y + 40, LX1 - 34, c3y + 84], 10, fill=SUB, outline=BORDER, width=2)
seg = tabw / 3
for i, t in enumerate(tabs):
    cx = tab0 + seg * i + seg / 2
    if i == 0:
        rr([tab0 + 4, c3y + 44, tab0 + seg - 2, c3y + 80], 8, fill=(46, 42, 38))
    text((cx, c3y + 62), t, f(FB if i == 0 else F, 24), WHITE if i == 0 else DIM, anchor="mm")
# code block
code_y = c3y + 130
code_bottom = code_y + 210
rr([LX0 + 34, code_y, LX1 - 34, code_bottom], 14, fill=(8, 8, 9), outline=BORDER, width=2)
text((LX0 + 60, code_y + 22), "REQUEST", f(FB, 22), DIM)
text((LX1 - 60, code_y + 22), "Copy", f(F, 22), GRAY, anchor="ra")
d.line([LX0 + 34, code_y + 64, LX1 - 34, code_y + 64], fill=BORDER, width=2)
code = ['curl https://api.condueet.com/v1/accounts/acc_test_xxxx \\',
        '  -H "Authorization: Bearer sk_test_9f21c40a7715" \\',
        '  -H "Content-Type: application/json"']
cyy = code_y + 86
for ln in code:
    text((LX0 + 60, cyy), ln, f(FM, 25), MONO)
    cyy += 40
# run request (disabled) + helper — below the code block
run_y = code_bottom + 20
rr([LX0 + 34, run_y, LX0 + 230, run_y + 52], 11, fill=(30, 28, 26), outline=BORDER, width=2)
d.polygon([(LX0 + 66, run_y + 16), (LX0 + 66, run_y + 36), (LX0 + 84, run_y + 26)], fill=DIM)
text((LX0 + 98, run_y + 26), "Run request", f(FB, 24), DIM, anchor="lm")
text((LX0 + 258, run_y + 26), "Link a test customer first — the request needs an account id.",
     f(F, 23), DIM, anchor="lm")

# ===== Right card 1: WHAT THIS COSTS =====
rc1 = [RX0, CY, RX1, CY + 396]
rr(rc1, 20, fill=CARD, outline=BORDER, width=2)
text((RX0 + 34, CY + 30), "WHAT THIS COSTS", f(FB, 24), WHITE)
rows = [("Account balance", "₦45 / call", WHITE),
        ("Statement", "₦45 / call", WHITE),
        ("Identity", "₦90 / call", WHITE),
        ("This sandbox call", "₦0", GREEN)]
ry = CY + 82
for lab, val, col in rows:
    tc = GREEN if col is GREEN else GRAY
    text((RX0 + 34, ry), lab, f(F, 25), tc)
    text((RX1 - 34, ry), val, f(FB, 25), col, anchor="ra")
    ry += 46
foot = ["Sandbox calls are free and unmetered.",
        "Live calls draw from your wallet as they",
        "succeed — failed calls are never charged."]
fy = ry + 14
for ln in foot:
    text((RX0 + 34, fy), ln, f(F, 22), DIM)
    fy += 32

# ===== Right card 2: THEN WHAT =====
rc2y = CY + 422
rc2 = [RX0, rc2y, RX1, rc2y + 420]
rr(rc2, 20, fill=CARD, outline=BORDER, width=2)
text((RX0 + 34, rc2y + 30), "THEN WHAT", f(FB, 24), WHITE)

def icon_warn(cx, cy):
    d.polygon([(cx, cy - 15), (cx - 16, cy + 13), (cx + 16, cy + 13)], outline=PINK, width=3)
    d.line([cx, cy - 4, cx, cy + 5], fill=PINK, width=3)
    d.ellipse([cx - 2, cy + 8, cx + 2, cy + 12], fill=PINK)

def icon_hooks(cx, cy):
    d.line([cx - 15, cy - 6, cx + 15, cy - 6], fill=PINK, width=3)
    d.polygon([(cx + 15, cy - 12), (cx + 15, cy), (cx + 22, cy - 6)], fill=PINK)
    d.line([cx - 15, cy + 8, cx + 15, cy + 8], fill=PINK, width=3)
    d.polygon([(cx - 15, cy + 2), (cx - 15, cy + 14), (cx - 22, cy + 8)], fill=PINK)

def icon_live(cx, cy):
    d.polygon([(cx, cy - 16), (cx + 15, cy), (cx, cy + 16), (cx - 15, cy)], outline=PINK, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=PINK)

icons = [icon_warn, icon_hooks, icon_live]
items = [("Handle a failed pull", ["Bank timeouts, expired consent and", "how retries work."]),
         ("Receive webhooks", ["Get told when data lands instead of", "polling."]),
         ("Go live", ["Activation takes a few hours for", "developers."])]
iy = rc2y + 92
for drawicon, (title, desc) in zip(icons, items):
    drawicon(RX0 + 52, iy + 14)
    text((RX0 + 86, iy), title, f(FB, 27), WHITE)
    dyy = iy + 42
    for ln in desc:
        text((RX0 + 86, dyy), ln, f(F, 23), GRAY)
        dyy += 32
    iy += 118

img.save("/Users/macbookpro/Desktop/Portfolio-2026/assets/condueet-v2-shell.png")
print("saved", img.size)
