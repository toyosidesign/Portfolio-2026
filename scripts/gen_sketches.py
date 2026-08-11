#!/usr/bin/env python3
"""Aria autonomy - low-fidelity mobile sketches (onboarding, Today, create task).
Hand-drawn pencil-on-paper look to match the portfolio's sketch aesthetic."""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(7)
W, H = 2400, 1600
PAPER   = (244, 237, 222)
PENCIL  = (60, 57, 50)
PENCIL2 = (122, 116, 102)
PEN     = (192, 70, 106)
SCREEN  = (250, 247, 240)

HAND = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
def f(s): return ImageFont.truetype(HAND, s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# faint paper speckle
for _ in range(1400):
    x, y = random.randint(0, W), random.randint(0, H)
    g = random.randint(0, 18)
    d.point((x, y), fill=(PAPER[0]-g, PAPER[1]-g, PAPER[2]-g))

def jit(a=2.0):
    return random.uniform(-a, a)

def sline(p1, p2, color=PENCIL, w=4, passes=2, seg=14):
    """hand-drawn line: a few offset passes broken into jittered segments."""
    for _ in range(passes):
        ox, oy = jit(1.6), jit(1.6)
        x1, y1 = p1[0]+ox, p1[1]+oy
        x2, y2 = p2[0]+ox, p2[1]+oy
        n = max(2, int(((x2-x1)**2+(y2-y1)**2)**0.5/seg))
        pts = []
        for k in range(n+1):
            t = k/n
            pts.append((x1+(x2-x1)*t+jit(1.4), y1+(y2-y1)*t+jit(1.4)))
        d.line(pts, fill=color, width=w, joint="curve")

def srect(box, r=26, color=PENCIL, w=4, passes=2):
    for _ in range(passes):
        ox, oy = jit(1.4), jit(1.4)
        d.rounded_rectangle([box[0]+ox, box[1]+oy, box[2]+ox, box[3]+oy],
                            radius=r, outline=color, width=w)

def scrib(x, y, w, color=PENCIL2, weight=5):
    """a wavy line standing in for a line of text."""
    pts = []
    n = max(3, int(w/22))
    for k in range(n+1):
        pts.append((x+(w)*k/n, y+jit(2.2)))
    d.line(pts, fill=color, width=weight, joint="curve")

def scrib_block(x, y, w, lines, lh=26, color=PENCIL2, weight=4, shrink_last=True):
    for i in range(lines):
        ww = w if not (shrink_last and i == lines-1) else int(w*0.6)
        scrib(x, y+i*lh, ww, color=color, weight=weight)

def htext(xy, s, size, color=PENCIL, anchor="la"):
    d.text(xy, s, font=f(size), fill=color, anchor=anchor)

def check(cx, cy, s=14, color=PEN, w=6):
    sline((cx-s, cy), (cx-s*0.2, cy+s), color, w, passes=1)
    sline((cx-s*0.2, cy+s), (cx+s*1.2, cy-s*1.1), color, w, passes=1)

def arrow(p1, p2, color=PEN, w=4):
    sline(p1, p2, color, w, passes=1)
    import math
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    for a in (ang+2.5, ang-2.5):
        d.line([p2, (p2[0]-18*math.cos(a), p2[1]-18*math.sin(a))], fill=color, width=w)

def cat_icon(kind, ox, oy, s=32, col=PENCIL):
    if kind == "event":
        d.rounded_rectangle([ox, oy+8, ox+s, oy+s], radius=6, outline=col, width=3)
        d.line([ox, oy+18, ox+s, oy+18], fill=col, width=3)
        d.line([ox+9, oy+2, ox+9, oy+12], fill=col, width=3)
        d.line([ox+s-9, oy+2, ox+s-9, oy+12], fill=col, width=3)
    elif kind == "bell":
        d.arc([ox+3, oy+2, ox+s-3, oy+s], start=180, end=360, fill=col, width=3)
        d.line([ox+3, oy+s//2, ox+3, oy+s-6], fill=col, width=3)
        d.line([ox+s-3, oy+s//2, ox+s-3, oy+s-6], fill=col, width=3)
        d.line([ox-2, oy+s-6, ox+s+2, oy+s-6], fill=col, width=3)
        d.ellipse([ox+s//2-3, oy+s-5, ox+s//2+3, oy+s+2], outline=col, width=2)
    elif kind == "book":
        d.line([ox+s//2, oy+5, ox+s//2, oy+s], fill=col, width=3)
        for sx in (ox+2, ox+s-2):
            d.line([ox+s//2, oy+5, sx, oy+9], fill=col, width=3)
            d.line([sx, oy+9, sx, oy+s-2], fill=col, width=3)
            d.line([sx, oy+s-2, ox+s//2, oy+s], fill=col, width=3)
    elif kind == "chart":
        base = oy+s
        d.line([ox, base, ox+s, base], fill=col, width=3)
        for bi, hh in enumerate((s*0.4, s*0.72, s*0.55)):
            bx = ox+3+bi*((s-6)/3)
            d.rectangle([bx, base-hh, bx+(s-6)/3-6, base], outline=col, width=3)

# ---------- phone frames ----------
MX, GAP = 70, 150
PW = 650
PH = int(PW*19.5/9)
TOP = 150
titles = ["1  ·  Onboarding", "2  ·  Home  (Today)", "3  ·  Create task"]
xs = [MX + i*(PW+GAP) for i in range(3)]

# header handwriting (top-left of the page)
htext((MX, 60), "Aria  ~  early sketches", 40, PENCIL)
sline((MX, 108), (MX+430, 108), PEN, 3, passes=1)

for i, x0 in enumerate(xs):
    x1 = x0+PW
    y0, y1 = TOP, TOP+PH
    htext((x0+8, y0-52), titles[i], 34, PENCIL)
    srect([x0, y0, x1, y1], r=48, color=PENCIL, w=5, passes=2)
    # screen
    sx0, sy0, sx1, sy1 = x0+20, y0+22, x1-20, y1-22
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=34, fill=SCREEN)
    srect([sx0, sy0, sx1, sy1], r=34, color=PENCIL2, w=2, passes=1)
    # notch
    d.rounded_rectangle([(x0+x1)/2-55, y0+30, (x0+x1)/2+55, y0+50], radius=10, fill=PENCIL)
    cpad = 34
    cx0, cx1 = sx0+cpad, sx1-cpad
    cw = cx1-cx0

    # ===== SCREEN 1 : ONBOARDING =====
    if i == 0:
        ty = sy0+90
        htext((cx0, ty), "How much of it", 40, PENCIL)
        htext((cx0, ty+46), "should I do?", 40, PENCIL)
        scrib(cx0, ty+108, cw*0.8, weight=4)
        # FREE card
        fy0 = ty+150
        srect([cx0, fy0, cx1, fy0+180], r=22, color=PENCIL, w=3)
        htext((cx0+24, fy0+22), "FREE", 34, PENCIL)
        htext((cx0+24, fy0+66), "I plan, you do", 26, PENCIL2)
        scrib_block(cx0+24, fy0+112, cw-70, 2, lh=26)
        # PRO card (selected)
        py0 = fy0+205
        srect([cx0, py0, cx1, py0+180], r=22, color=PEN, w=4)
        htext((cx0+24, py0+22), "PRO", 34, PENCIL)
        htext((cx0+24, py0+66), "I do, you check", 26, PENCIL2)
        scrib_block(cx0+24, py0+112, cw-70, 2, lh=26)
        # selected tick top-right
        d.ellipse([cx1-58, py0+20, cx1-20, py0+58], outline=PEN, width=4)
        check((cx1-39), py0+34, s=12)
        # continue button
        by0 = py0+215
        srect([cx0, by0, cx1, by0+78], r=22, color=PENCIL, w=4)
        htext(((cx0+cx1)/2, by0+39), "Continue", 32, PENCIL, anchor="mm")
        # pen annotation
        htext((cx0+6, by0+96), "tier sets how far Aria goes", 26, PEN)
        arrow((cx1-120, py0+120), (cx1-40, py0+90))

    # ===== SCREEN 2 : HOME (TODAY) =====
    elif i == 1:
        htext((cx0, sy0+72), "Today", 44, PENCIL)
        htext((cx1, sy0+84), "Fri 12", 26, PENCIL2, anchor="ra")
        scrib(cx0, sy0+128, cw, weight=3)
        ry = sy0+160
        offers = [True, True, False]
        for r_i in range(3):
            rh = 150
            srect([cx0, ry, cx1, ry+rh], r=20, color=PENCIL, w=3)
            # checkbox
            d.ellipse([cx0+22, ry+30, cx0+58, ry+66], outline=PENCIL2, width=4)
            scrib(cx0+80, ry+34, cw*0.5, color=PENCIL, weight=5)
            scrib_block(cx0+80, ry+72, cw*0.62, 2, lh=24)
            if offers[r_i]:
                # offer pill
                srect([cx1-190, ry+30, cx1-24, ry+74], r=22, color=PEN, w=3)
                htext((cx1-107, ry+52), "Aria offer", 22, PEN, anchor="mm")
            ry += rh+22
        htext((cx0, ry+2), "Coming up", 30, PENCIL)
        ry += 46
        for _ in range(2):
            srect([cx0, ry, cx1, ry+92], r=18, color=PENCIL2, w=2)
            scrib(cx0+24, ry+34, cw*0.55, weight=4)
            scrib(cx0+24, ry+62, cw*0.4, weight=3)
            ry += 108
        # tab bar
        tb = sy1-96
        sline((sx0+16, tb), (sx1-16, tb), PENCIL2, 2, passes=1)
        icons = 5
        for t in range(icons):
            tx = sx0 + (sx1-sx0)*(t+0.5)/icons
            if t == 2:
                d.ellipse([tx-30, tb+18, tx+30, tb+78], outline=PEN, width=4)
                htext((tx, tb+48), "+", 40, PEN, anchor="mm")
            else:
                srect([tx-20, tb+26, tx+20, tb+66], r=8, color=PENCIL2, w=3, passes=1)
        # annotation (kept clear of the cards)
        htext((cx0, sy1-152), "the offer  =  what Aria can take off you", 24, PEN)

    # ===== SCREEN 3 : CREATE TASK =====
    else:
        cxc = (sx0+sx1)/2
        # header: close (x) + centred title
        sline((cx0, sy0+44), (cx0+30, sy0+74), PENCIL, 4, passes=1)
        sline((cx0+30, sy0+44), (cx0, sy0+74), PENCIL, 4, passes=1)
        htext((cxc, sy0+58), "New task", 40, PENCIL, anchor="mm")
        # CATEGORY : 2x2 cards with icon + title + description
        htext((cx0, sy0+108), "category", 24, PENCIL2)
        cats = [("Event", "event"), ("Reminder", "bell"),
                ("Assignment", "book"), ("Project", "chart")]
        cardw = (cw-20)/2
        cardh = 150
        cgy = sy0+148
        for idx, (name, icon) in enumerate(cats):
            col, row = idx % 2, idx // 2
            cardx = cx0 + col*(cardw+20)
            cardy = cgy + row*(cardh+20)
            sel = (name == "Reminder")
            srect([cardx, cardy, cardx+cardw, cardy+cardh], r=18,
                  color=PEN if sel else PENCIL, w=4 if sel else 3)
            cat_icon(icon, cardx+22, cardy+20, s=30)
            htext((cardx+64, cardy+22), name, 26, PENCIL)
            scrib_block(cardx+24, cardy+80, cardw-48, 2, lh=24)
        bottom_cards = cgy + 2*cardh + 20
        htext((cx0, bottom_cards+12), "category shapes the fields below", 20, PEN)
        # prompt + input
        py = bottom_cards + 58
        htext((cx0, py), "what should I remind you about?", 22, PENCIL2)
        srect([cx0, py+34, cx1, py+104], r=16, color=PENCIL, w=3)
        htext((cx0+22, py+69), "e.g. take the bins out", 24, PENCIL2, anchor="lm")
        # DATE + month calendar
        dy = py+140
        htext((cx0, dy), "date", 24, PENCIL2)
        caly = dy+34
        calh = (sy1-116) - caly
        srect([cx0, caly, cx1, caly+calh], r=20, color=PENCIL, w=3)
        htext((cx0+24, caly+26), "August 2026", 32, PENCIL)
        sline((cx1-100, caly+30), (cx1-116, caly+46), PENCIL, 3, passes=1)
        sline((cx1-116, caly+46), (cx1-100, caly+62), PENCIL, 3, passes=1)
        sline((cx1-42, caly+30), (cx1-26, caly+46), PENCIL, 3, passes=1)
        sline((cx1-26, caly+46), (cx1-42, caly+62), PENCIL, 3, passes=1)
        colw = cw/7
        wy = caly+98
        for c, wl in enumerate(["S", "M", "T", "W", "T", "F", "S"]):
            htext((cx0+colw*(c+0.5), wy), wl, 22, PENCIL2, anchor="mm")
        weeks = [
            [(26, 1), (27, 1), (28, 1), (29, 1), (30, 1), (31, 1), (1, 0)],
            [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)],
            [(9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0)],
            [(16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0)],
            [(23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0)],
            [(30, 0), (31, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)],
        ]
        gy0 = caly+142
        rowh = ((caly+calh-22) - gy0)/6
        for r_i, week in enumerate(weeks):
            for c_i, (num, muted) in enumerate(week):
                ccx = cx0+colw*(c_i+0.5)
                ccy = gy0 + rowh*(r_i+0.5)
                if num == 11 and r_i == 2:
                    d.ellipse([ccx-24, ccy-24, ccx+24, ccy+24], fill=PEN)
                    htext((ccx, ccy), "11", 24, SCREEN, anchor="mm")
                else:
                    htext((ccx, ccy), str(num), 24,
                          PENCIL2 if muted else PENCIL, anchor="mm")
        # save button
        by = sy1-96
        srect([cx0, by, cx1, by+74], r=20, color=PEN, w=4)
        htext(((cx0+cx1)/2, by+37), "Save task", 30, PEN, anchor="mm")

img.save("/Users/macbookpro/Desktop/Portfolio-2026/assets/aria2-sketches.png")
print("saved", img.size)
