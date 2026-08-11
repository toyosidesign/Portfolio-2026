#!/usr/bin/env python3
"""Aria autonomy - six illustrated storyboard panels (hand-drawn, paper)."""
import math, random
from PIL import Image, ImageDraw, ImageFont

random.seed(11)
PW, PH = 1000, 680
PAPER   = (244, 237, 222)
PENCIL  = (60, 57, 50)
PENCIL2 = (122, 116, 102)
PEN     = (192, 70, 106)
SCREEN  = (250, 247, 240)
GREEN   = (22, 163, 74)
AMBER   = (217, 119, 6)
RED     = (220, 38, 38)

HAND = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
def f(s): return ImageFont.truetype(HAND, s)

def jit(a=2.0): return random.uniform(-a, a)

def sline(d, p1, p2, color=PENCIL, w=5, passes=2, seg=16):
    for _ in range(passes):
        ox, oy = jit(1.4), jit(1.4)
        x1, y1 = p1[0]+ox, p1[1]+oy
        x2, y2 = p2[0]+ox, p2[1]+oy
        n = max(2, int(((x2-x1)**2+(y2-y1)**2)**0.5/seg))
        pts = [(x1+(x2-x1)*k/n+jit(1.3), y1+(y2-y1)*k/n+jit(1.3)) for k in range(n+1)]
        d.line(pts, fill=color, width=w, joint="curve")

def srect(d, box, r=20, color=PENCIL, w=5, passes=2):
    for _ in range(passes):
        ox, oy = jit(1.3), jit(1.3)
        d.rounded_rectangle([box[0]+ox, box[1]+oy, box[2]+ox, box[3]+oy],
                            radius=r, outline=color, width=w)

def scrib(d, x, y, w, color=PENCIL2, weight=5):
    n = max(3, int(w/22))
    pts = [(x+w*k/n, y+jit(2.0)) for k in range(n+1)]
    d.line(pts, fill=color, width=weight, joint="curve")

def htext(d, xy, s, size, color=PENCIL, anchor="la"):
    d.text(xy, s, font=f(size), fill=color, anchor=anchor)

def check(d, cx, cy, s=15, color=PEN, w=7):
    sline(d, (cx-s, cy), (cx-s*0.2, cy+s), color, w, passes=1)
    sline(d, (cx-s*0.2, cy+s), (cx+s*1.2, cy-s*1.1), color, w, passes=1)

def arrow(d, p1, p2, color=PEN, w=5):
    sline(d, p1, p2, color, w, passes=1)
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    for a in (ang+2.6, ang-2.6):
        d.line([p2, (p2[0]-22*math.cos(a), p2[1]-22*math.sin(a))], fill=color, width=w)

def phone(d, cx, cyt, w, h):
    """draw a phone; return inner screen rect."""
    x0, y0 = cx-w/2, cyt
    srect(d, [x0, y0, x0+w, y0+h], r=30, color=PENCIL, w=5)
    sx0, sy0, sx1, sy1 = x0+14, y0+16, x0+w-14, y0+h-16
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=20, fill=SCREEN)
    d.rounded_rectangle([cx-32, y0+22, cx+32, y0+34], radius=6, fill=PENCIL)
    return sx0, sy0, sx1, sy1

def doc(d, x0, y0, w, h, label="PDF"):
    fold = 46
    pts = [(x0, y0), (x0+w-fold, y0), (x0+w, y0+fold), (x0+w, y0+h), (x0, y0+h)]
    for _ in range(2):
        o = (jit(1.2), jit(1.2))
        d.line([(p[0]+o[0], p[1]+o[1]) for p in pts]+[(pts[0][0]+o[0], pts[0][1]+o[1])],
               fill=PENCIL, width=5, joint="curve")
    d.line([(x0+w-fold, y0), (x0+w-fold, y0+fold), (x0+w, y0+fold)], fill=PENCIL2, width=4)
    for k in range(4):
        scrib(d, x0+22, y0+70+k*34, w-52, weight=4)
    htext(d, (x0+22, y0+h-46), label, 26, PEN)

# ---- speech bubble ----
def bubble(d, x0, y0, w, h, tail_x):
    srect(d, [x0, y0, x0+w, y0+h], r=18, color=PENCIL, w=4)
    d.polygon([(tail_x, y0+h-2), (tail_x+26, y0+h-2), (tail_x+6, y0+h+26)], fill=SCREEN)
    sline(d, (tail_x, y0+h), (tail_x+6, y0+h+26), PENCIL, 4, passes=1)
    sline(d, (tail_x+26, y0+h), (tail_x+6, y0+h+26), PENCIL, 4, passes=1)

def scene(i, d):
    M = 70
    x0, y0, x1, y1 = M, M, PW-M, PH-M
    cx = (x0+x1)/2

    if i == 1:  # the brief lands
        doc(d, x0, y0+40, 300, 380, "brief.pdf")
        sr = phone(d, x1-150, y0+30, 300, 420)
        htext(d, (sr[0]+30, sr[1]+30), "Aria", 34, PENCIL)
        scrib(d, sr[0]+30, sr[1]+90, 180, weight=4)
        srect(d, [sr[0]+28, sr[3]-90, sr[2]-28, sr[3]-30], r=16, color=PEN, w=4)
        htext(d, ((sr[0]+sr[2])/2, sr[3]-60), "Upload brief", 24, PEN, anchor="mm")
        arrow(d, (x0+330, y0+220), (x1-300, y0+230))

    elif i == 2:  # aria reads it back
        sr = phone(d, cx-140, y0+10, 320, 460)
        htext(d, (sr[0]+28, sr[1]+28), "What I found", 30, PENCIL)
        rows = [("Deliverable", GREEN), ("Deadline", GREEN), ("Weighting", AMBER), ("Format", RED)]
        for k, (lab, col) in enumerate(rows):
            ry = sr[1]+80+k*74
            srect(d, [sr[0]+24, ry, sr[2]-24, ry+58], r=12, color=PENCIL2, w=3, passes=1)
            htext(d, (sr[0]+42, ry+14), lab, 24, PENCIL)
            d.ellipse([sr[2]-58, ry+16, sr[2]-30, ry+44], fill=col)
        bubble(d, x1-260, y0+20, 250, 96, x1-180)
        htext(d, (x1-236, y0+42), "reads it", 28, PENCIL)
        htext(d, (x1-236, y0+74), "back to you", 28, PENCIL)

    elif i == 3:  # a plan with runway
        base = y0+230
        sline(d, (x0+20, base), (x1-20, base), PENCIL, 5)
        n = 5
        for k in range(n):
            px = x0+40 + (x1-x0-120)*k/(n-1)
            d.ellipse([px-14, base-14, px+14, base+14], outline=PENCIL, width=5)
            if k == 0:
                d.ellipse([px-14, base-14, px+14, base+14], fill=PEN)
                sline(d, (px, base-14), (px, base-70), PEN, 4, passes=1)
                d.polygon([(px, base-70), (px+46, base-58), (px, base-46)], fill=PEN)
                htext(d, (px-6, base+26), "pinned", 22, PEN)
        # buffer block near deadline
        bx = x1-150
        srect(d, [bx, base-40, x1-20, base+40], r=12, color=PEN, w=4)
        htext(d, ((bx+x1-20)/2, base), "buffer", 22, PEN, anchor="mm")
        htext(d, (x0+20, y0+60), "dated steps, with runway", 30, PENCIL)
        htext(d, (x1-40, base+70), "deadline", 22, PENCIL2, anchor="ra")

    elif i == 4:  # a bad week hits
        # rain cloud
        ccx, ccy = x0+180, y0+120
        for dx in (-70, -20, 40, 90):
            d.ellipse([ccx+dx-55, ccy-40, ccx+dx+55, ccy+40], outline=PENCIL, width=5)
        for rx in range(-60, 110, 34):
            sline(d, (ccx+rx, ccy+50), (ccx+rx-16, ccy+110), PENCIL2, 4, passes=1)
        # overdue blocks (left) moving right
        by = y1-150
        for k in range(3):
            srect(d, [x0+20+k*70, by, x0+70+k*70, by+50], r=10, color=PENCIL2, w=4, passes=1)
        for k in range(3):
            tx = cx+40+k*80
            srect(d, [tx, by, tx+50, by+50], r=10, color=PENCIL, w=4)
        arrow(d, (x0+250, by+25), (cx+30, by+25))
        htext(d, (cx-30, by-70), "spread across days left", 26, PEN)
        htext(d, (x1-40, by+90), "moved 3", 26, PEN, anchor="ra")

    elif i == 5:  # approve the day
        sr = phone(d, cx, y0+10, 340, 470)
        htext(d, (sr[0]+28, sr[1]+26), "Morning review", 28, PENCIL)
        groups = ["I'll send", "For your tap", "Yours today"]
        gy = sr[1]+78
        for g in groups:
            htext(d, (sr[0]+30, gy), g, 22, PEN)
            for r_i in range(2):
                yy = gy+30+r_i*30
                d.ellipse([sr[0]+34, yy, sr[0]+56, yy+22], outline=PENCIL2, width=3)
                scrib(d, sr[0]+70, yy+4, 150, weight=4)
            gy += 108
        srect(d, [sr[0]+28, sr[3]-70, sr[2]-28, sr[3]-24], r=16, color=PEN, w=5)
        htext(d, ((sr[0]+sr[2])/2-16, sr[3]-47), "Approve", 26, PEN, anchor="mm")
        check(d, (sr[2]-70), sr[3]-47, s=11)

    else:  # it reports back
        sr = phone(d, cx, y0+10, 340, 470)
        # clock (ten-min hold)
        clx, cly = sr[2]-56, sr[1]+56
        d.ellipse([clx-30, cly-30, clx+30, cly+30], outline=PENCIL, width=5)
        sline(d, (clx, cly), (clx, cly-18), PENCIL, 4, passes=1)
        sline(d, (clx, cly), (clx+14, cly+6), PENCIL, 4, passes=1)
        htext(d, (sr[0]+28, sr[1]+30), "Today", 30, PENCIL)
        for k in range(4):
            yy = sr[1]+120+k*74
            srect(d, [sr[0]+24, yy, sr[2]-24, yy+56], r=12, color=PENCIL2, w=3, passes=1)
            scrib(d, sr[0]+82, yy+22, 150, weight=5)
            d.ellipse([sr[0]+40, yy+16, sr[0]+70, yy+46], outline=PEN, width=4)
            check(d, sr[0]+55, yy+24, s=9)
        htext(d, (x0+10, y1-6), "sent  -  checked off", 26, PEN)

# ---- render 6 images + a contact sheet for review ----
paths = []
imgs = []
for i in range(1, 7):
    im = Image.new("RGB", (PW, PH), PAPER)
    d = ImageDraw.Draw(im)
    for _ in range(600):
        x, y = random.randint(0, PW), random.randint(0, PH)
        g = random.randint(0, 16); d.point((x, y), fill=(PAPER[0]-g, PAPER[1]-g, PAPER[2]-g))
    scene(i, d)
    p = f"/Users/macbookpro/Desktop/Portfolio-2026/assets/aria2-story-{i}.webp"
    im.save(p, "WEBP", quality=90, method=6)
    paths.append(p); imgs.append(im)

# contact sheet
cs = Image.new("RGB", (PW*3+40, PH*2+30), (20, 18, 16))
for idx, im in enumerate(imgs):
    r, c = divmod(idx, 3)
    cs.paste(im, (10+c*(PW+10), 10+r*(PH+10)))
cs.save("/private/tmp/claude-501/-Users-macbookpro-Desktop-Portfolio-2026/3537d3c5-007c-4e6a-a44b-8eff968a8867/scratchpad/story_contact.png")
print("saved 6 panels")
