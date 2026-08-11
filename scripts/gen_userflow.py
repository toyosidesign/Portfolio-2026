#!/usr/bin/env python3
"""Aria autonomy - Assignment task user-flow diagram (flowchart style)."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1340
BG = (12, 11, 11)
STEP = ((24, 31, 42), (74, 100, 132), (214, 226, 240))
ACT  = ((20, 40, 38), (70, 130, 116), (200, 235, 224))
ENTRY= ((34, 24, 28), (255, 216, 228), (255, 216, 228))
RES  = ((255, 216, 228), (255, 216, 228), (28, 16, 21))
DIA  = ((255, 216, 228), (255, 216, 228), (28, 16, 21))
GRPB = (120, 114, 102)
GRPT = (150, 144, 132)
CHG  = ((20, 40, 28), (40, 120, 74), (150, 220, 170))
CHA  = ((44, 34, 16), (150, 110, 40), (230, 190, 120))
CHR  = ((44, 20, 22), (150, 60, 60), (235, 150, 150))
OPT  = ((22, 26, 32), (86, 90, 98), (205, 209, 215))
LMAIN= (120, 190, 150)
LALT = (120, 124, 130)

FR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def f(p, s): return ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
nodes = {}

def node(name, cx, cy, w, h, text, pal, r=14, bw=2, size=27):
    box = [cx-w/2, cy-h/2, cx+w/2, cy+h/2]
    d.rounded_rectangle(box, radius=r, fill=pal[0], outline=pal[1], width=bw)
    d.text((cx, cy), text, font=f(FB, size), fill=pal[2], anchor="mm")
    nodes[name] = box
    return box

def chip(name, cx, cy, text, pal, dot=None, h=52, size=23):
    w = d.textlength(text, font=f(FB, size)) + (74 if dot else 46)
    box = [cx-w/2, cy-h/2, cx+w/2, cy+h/2]
    d.rounded_rectangle(box, radius=12, fill=pal[0], outline=pal[1], width=2)
    d.text((cx + (12 if dot else 0), cy), text, font=f(FB, size), fill=pal[2], anchor="mm")
    if dot:
        d.ellipse([box[0]+16, cy-7, box[0]+30, cy+7], fill=dot)
    nodes[name] = box
    return box

def diamond(name, cx, cy, w, h, text, size=24):
    d.polygon([(cx, cy-h/2), (cx+w/2, cy), (cx, cy+h/2), (cx-w/2, cy)], fill=DIA[0], outline=DIA[1])
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        d.text((cx, cy-11+i*24 if len(lines) > 1 else cy), ln, font=f(FB, size), fill=DIA[2], anchor="mm")
    nodes[name] = [cx-w/2, cy-h/2, cx+w/2, cy+h/2]

def dashed_group(box, title, title_dx=22, dash=16, gap=12, color=GRPB):
    x0, y0, x1, y1 = box
    def dline(a, b):
        L = math.hypot(b[0]-a[0], b[1]-a[1]); n = int(L/(dash+gap))
        for k in range(n+1):
            t0 = (dash+gap)*k/L; t1 = min(t0+dash/L, 1.0)
            d.line([(a[0]+(b[0]-a[0])*t0, a[1]+(b[1]-a[1])*t0),
                    (a[0]+(b[0]-a[0])*t1, a[1]+(b[1]-a[1])*t1)], fill=color, width=2)
    dline((x0, y0), (x1, y0)); dline((x1, y0), (x1, y1))
    dline((x1, y1), (x0, y1)); dline((x0, y1), (x0, y0))
    d.text((x0+title_dx, y0+16), title, font=f(FB, 22), fill=GRPT, anchor="lm")

def top(n): b=nodes[n]; return ((b[0]+b[2])/2, b[1])
def bot(n): b=nodes[n]; return ((b[0]+b[2])/2, b[3])
def rgt(n): b=nodes[n]; return (b[2], (b[1]+b[3])/2)

def arrowhead(p_from, p_to, color, s=15):
    ang = math.atan2(p_to[1]-p_from[1], p_to[0]-p_from[0])
    for a in (ang+2.6, ang-2.6):
        d.line([p_to, (p_to[0]-s*math.cos(a), p_to[1]-s*math.sin(a))], fill=color, width=3)

def conn(points, color=LMAIN, label=None, lw=3):
    d.line(points, fill=color, width=lw, joint="curve")
    arrowhead(points[-2], points[-1], color)
    if label:
        d.text((points[0][0]+14, points[0][1]-18), label, font=f(FB, 22), fill=(214, 214, 214), anchor="lm")

# ================= LAYOUT =================
SX = 300
NW, NH = 220, 62

node("assignment", SX, 78, NW, NH, "Assignment", ENTRY)
node("upload", SX, 188, NW, NH, "Upload the brief", ACT)
node("reads", SX, 298, NW, NH, "Aria reads it", ACT)

gA = [150, 372, 2250, 500]
dashed_group(gA, "EXTRACTION CARD  ·  confidence per field", title_dx=210)
fields = [("f_del", "Deliverable", CHG, (60, 200, 120)),
          ("f_dea", "Deadline", CHG, (60, 200, 120)),
          ("f_wei", "Weighting", CHA, (220, 160, 70)),
          ("f_cri", "Criteria", CHA, (220, 160, 70)),
          ("f_for", "Format rules", CHR, (220, 90, 90))]
for (nm, tx, pal, dot), cxp in zip(fields, [470, 810, 1140, 1450, 1780]):
    chip(nm, cxp, 456, tx, pal, dot=dot)

diamond("confident", SX, 640, 210, 150, "All fields\nconfident?")

gB = [700, 566, 2250, 714]
dashed_group(gB, "RESOLVE GAPS")
chip("g_tutor", 1010, 650, "Ask tutor", OPT)
chip("g_hand", 1420, 650, "Upload handbook", OPT)
chip("g_know", 1850, 650, "I know this", OPT)

node("commit", SX, 820, NW, NH, "Commitments", STEP)
node("plan", SX, 930, NW, NH, "Plan preview", STEP)
diamond("accept", SX, 1078, 210, 148, "Accept?")

node("guide", 700, 930, 180, 58, "Guide", ACT, size=25)
gC = [900, 862, 2250, 998]
dashed_group(gC, "3-4 DIRECTIONS  ·  needs · cost · criterion")
chip("d_a", 1170, 946, "Direction A", OPT)
chip("d_b", 1560, 946, "Direction B", OPT)
chip("d_c", 1950, 946, "Direction C", OPT)

node("result", 620, 1232, 900, 74,
     "Task created  ·  dated steps  ·  step one pinned  ·  buffer reserved", RES, size=24)

# ================= CONNECTORS =================
conn([bot("assignment"), top("upload")])
conn([bot("upload"), top("reads")])
conn([bot("reads"), (SX, 372)])
conn([(SX, 500), top("confident")])
# No -> resolve gaps
conn([rgt("confident"), (gB[0], 640)], color=LALT, label="No")
# resolved -> back up into extraction card
conn([(1950, gB[1]), (1950, 502)], color=LALT)
d.text((1966, 540), "resolved", font=f(FB, 20), fill=GRPT, anchor="lm")
# Yes -> commitments
conn([bot("confident"), top("commit")])
d.text((322, 702), "Yes", font=f(FB, 22), fill=(214, 214, 214), anchor="lm")
conn([bot("commit"), top("plan")])
conn([bot("plan"), top("accept")])
# stuck -> guide -> directions
conn([rgt("plan"), (nodes["guide"][0], 930)], color=LALT, label="Stuck")
conn([rgt("guide"), (gC[0], 930)], color=LALT)
# directions -> back to plan preview (routed above guide, no crossings)
conn([(gC[0], 892), (360, 892), (SX, top("plan")[1])], color=LALT)
# accept Yes -> result
conn([bot("accept"), (SX, 1180), (620, 1180), top("result")])
d.text((322, 1142), "Yes", font=f(FB, 22), fill=(214, 214, 214), anchor="lm")

img.save("/Users/macbookpro/Desktop/Portfolio-2026/assets/aria2-userflow.png")
print("saved", img.size)
