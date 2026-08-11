#!/usr/bin/env python3
"""Aria autonomy - mid-fidelity greyscale wireframes
(onboarding, Today, create task) matching the sketch screens."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1600
BGC   = (233, 235, 238)     # canvas
BODY  = (34, 36, 40)        # phone frame
SCRN  = (255, 255, 255)
LINE  = (150, 155, 162)     # element outline
FILL0 = (238, 240, 243)     # light fill
FILL1 = (223, 226, 231)     # mid fill
BAR   = (205, 209, 215)     # text placeholder
BARD  = (176, 181, 189)     # darker bar
DARK  = (62, 66, 72)        # primary fill / strong text
INK   = (70, 74, 80)        # labels
MUTE  = (140, 146, 154)

FR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def f(p, s): return ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), BGC)
d = ImageDraw.Draw(img)

def rr(box, r, fill=None, outline=None, w=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w)

def bar(x, y, w, h=15, color=BAR):
    d.rounded_rectangle([x, y, x+w, y+h], radius=h/2, fill=color)

def bars(x, y, w, n, lh=28, last=0.6, color=BAR):
    for i in range(n):
        bar(x, y+i*lh, int(w*(last if i == n-1 else 1)), color=color)

def txt(xy, s, size, color=INK, anchor="la", bold=True):
    d.text(xy, s, font=f(FB if bold else FR, size), fill=color, anchor=anchor)

def checkbox(cx, cy, s=15, checked=False):
    rr([cx-s, cy-s, cx+s, cy+s], 6, outline=LINE, w=3)
    if checked:
        d.line([(cx-s+5, cy), (cx-3, cy+s-5)], fill=DARK, width=5)
        d.line([(cx-3, cy+s-5), (cx+s-3, cy-s+4)], fill=DARK, width=5)

def radio(cx, cy, s=17, on=False):
    d.ellipse([cx-s, cy-s, cx+s, cy+s], outline=LINE, width=3)
    if on:
        d.ellipse([cx-s+6, cy-s+6, cx+s-6, cy+s-6], fill=DARK)

# ---------- phones ----------
MX, GAP, PW = 70, 150, 650
PH = int(PW*19.5/9)
TOP = 150
titles = ["1  ·  Onboarding", "2  ·  Home  (Today)", "3  ·  Create task"]
xs = [MX + i*(PW+GAP) for i in range(3)]

txt((MX, 34), "Aria  —  wireframes", 38, INK)
d.line([(MX, 80), (MX+400, 80)], fill=MUTE, width=3)

for i, x0 in enumerate(xs):
    x1 = x0+PW
    y0, y1 = TOP, TOP+PH
    txt((x0+8, y0-52), titles[i], 33, INK)
    rr([x0, y0, x1, y1], 48, fill=SCRN, outline=BODY, w=5)
    sx0, sy0, sx1, sy1 = x0+18, y0+18, x1-18, y1-18
    rr([sx0, sy0, sx1, sy1], 34, fill=SCRN, outline=(210, 213, 218), w=2)
    # status bar
    txt((sx0+26, sy0+22), "9:41", 22, INK)
    for k in range(3):
        bar(sx1-90+k*26, sy0+30, 18, 10, color=BARD)
    d.rounded_rectangle([(x0+x1)/2-52, y0+30, (x0+x1)/2+52, y0+48], radius=9, fill=BODY)
    cpad = 34
    cx0, cx1 = sx0+cpad, sx1-cpad
    cw = cx1-cx0

    # ===== 1 · ONBOARDING =====
    if i == 0:
        ty = sy0+96
        txt((cx0, ty), "How much of it", 38, INK)
        txt((cx0, ty+46), "should I do?", 38, INK)
        bar(cx0, ty+108, int(cw*0.82))
        # Free card
        fy = ty+150
        rr([cx0, fy, cx1, fy+180], 20, fill=FILL0, outline=LINE, w=2)
        txt((cx0+26, fy+24), "Free", 34, INK)
        radio(cx1-40, fy+42, on=False)
        txt((cx0+26, fy+72), "I plan, you do", 24, MUTE)
        bars(cx0+26, fy+118, cw-80, 2, lh=26)
        # Pro card (selected)
        py = fy+205
        rr([cx0, py, cx1, py+180], 20, fill=SCRN, outline=DARK, w=4)
        txt((cx0+26, py+24), "Pro", 34, INK)
        radio(cx1-40, py+42, on=True)
        txt((cx0+26, py+72), "I do, you check", 24, MUTE)
        bars(cx0+26, py+118, cw-80, 2, lh=26)
        # Continue
        by = py+215
        rr([cx0, by, cx1, by+80], 18, fill=DARK)
        txt(((cx0+cx1)/2, by+40), "Continue", 30, SCRN, anchor="mm")
        bar(cx0+60, by+120, cw-120, 12, color=FILL1)

    # ===== 2 · TODAY =====
    elif i == 1:
        txt((cx0, sy0+80), "Today", 44, INK)
        txt((cx1, sy0+92), "Fri 12", 26, MUTE, anchor="ra")
        d.line([(cx0, sy0+150), (cx1, sy0+150)], fill=(224, 227, 231), width=3)
        ry = sy0+172
        for r_i in range(3):
            rh = 150
            rr([cx0, ry, cx1, ry+rh], 18, fill=SCRN, outline=LINE, w=2)
            checkbox(cx0+42, ry+50, 16)
            bar(cx0+80, ry+34, int(cw*0.46), 17)
            bars(cx0+80, ry+72, int(cw*0.6), 2, lh=24)
            if r_i < 2:
                rr([cx1-186, ry+30, cx1-24, ry+74], 22, fill=FILL1, outline=LINE, w=2)
                txt((cx1-105, ry+52), "Aria offer", 22, INK, anchor="mm")
            ry += rh+22
        txt((cx0, ry+4), "Coming up", 28, INK)
        ry += 48
        for _ in range(2):
            rr([cx0, ry, cx1, ry+92], 16, fill=FILL0, outline=(214, 217, 222), w=2)
            bar(cx0+24, ry+32, int(cw*0.5), 15)
            bar(cx0+24, ry+60, int(cw*0.34), 13)
            ry += 108
        # tab bar
        tb = sy1-100
        d.line([(sx0+16, tb), (sx1-16, tb)], fill=(224, 227, 231), width=3)
        for t in range(5):
            tx = sx0 + (sx1-sx0)*(t+0.5)/5
            if t == 2:
                d.ellipse([tx-30, tb+16, tx+30, tb+76], fill=DARK)
                txt((tx, tb+46), "+", 40, SCRN, anchor="mm")
            else:
                rr([tx-20, tb+26, tx+20, tb+66], 8, outline=MUTE, w=3)

    # ===== 3 · CREATE TASK =====
    else:
        txt((cx0, sy0+80), "New task", 42, INK)
        d.line([(cx0, sy0+140), (cx1, sy0+140)], fill=(224, 227, 231), width=3)
        txt((cx0, sy0+164), "Category", 24, MUTE)
        tiles = ["Bday", "Assign", "Project", "Note"]
        n = 4; gapt = 16
        tw = (cw-(n-1)*gapt)/n
        for t in range(n):
            txx = cx0+t*(tw+gapt)
            sel = (t == 1)
            rr([txx, sy0+200, txx+tw, sy0+200+tw], 16,
               fill=SCRN if not sel else FILL1, outline=DARK if sel else LINE, w=4 if sel else 2)
            txt((txx+tw/2, sy0+200+tw+22), tiles[t], 20, MUTE, anchor="mm")
        fy = sy0+200+tw+70
        def field(label, y, x0f, x1f):
            txt((x0f, y), label, 24, MUTE)
            rr([x0f, y+30, x1f, y+92], 12, fill=FILL0, outline=LINE, w=2)
            bar(x0f+18, y+54, int((x1f-x0f)*0.5), 14, color=BARD)
            return y+118
        fy = field("Title", fy, cx0, cx1)
        txt((cx0, fy), "Date / time", 24, MUTE)
        rr([cx0, fy+30, cx0+cw/2-10, fy+92], 12, fill=FILL0, outline=LINE, w=2)
        bar(cx0+18, fy+54, int((cw/2-10)*0.5), 14, color=BARD)
        rr([cx0+cw/2+10, fy+30, cx1, fy+92], 12, fill=FILL0, outline=LINE, w=2)
        bar(cx0+cw/2+28, fy+54, int((cw/2-10)*0.4), 14, color=BARD)
        fy += 118
        txt((cx0, fy), "How Aria handles it", 24, MUTE)
        chy = fy+34; chx = cx0
        for c in ["Text", "Email", "Call", "Card"]:
            wch = d.textlength(c, font=f(FB, 22))+44
            if chx+wch > cx1:
                chx = cx0; chy += 58
            rr([chx, chy, chx+wch, chy+46], 22, fill=SCRN, outline=LINE, w=2)
            txt((chx+wch/2, chy+23), c, 22, INK, anchor="mm")
            chx += wch+16
        by = sy1-108
        rr([cx0, by, cx1, by+78], 18, fill=DARK)
        txt(((cx0+cx1)/2, by+39), "Save", 30, SCRN, anchor="mm")

img.save("/Users/macbookpro/Desktop/Portfolio-2026/assets/aria2-wireframes.png")
print("saved", img.size)
