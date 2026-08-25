#!/usr/bin/env python3
"""Generate SVG markup (reusing the page's .flowsvg CSS classes) for the
Dossier IA tree and the full buyer / seller task-flow charts with every branch."""
import html

def esc(s): return html.escape(s, quote=True)

def wrap(text, maxc):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur)+len(w)+1 <= maxc: cur = (cur+" "+w).strip()
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

MARK = ('<marker id="{i}" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">'
        '<path class="amk{g}" d="M0 0 L6 3 L0 6 Z"/></marker>')

def box(x, y, w, h, title, desc="", cls="box", tw=None):
    tw = tw or int(w/6.4)
    cx = x + w/2
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>']
    if desc:
        dl = wrap(desc, tw)
        ty = y + 20
        out.append(f'<text class="t" x="{cx}" y="{ty}" text-anchor="middle" dominant-baseline="central">{esc(title)}</text>')
        for i, ln in enumerate(dl):
            out.append(f'<text class="t2" x="{cx}" y="{ty+18+i*13}" text-anchor="middle" dominant-baseline="central">{esc(ln)}</text>')
    else:
        out.append(f'<text class="t" x="{cx}" y="{y+h/2}" text-anchor="middle" dominant-baseline="central">{esc(title)}</text>')
    return "".join(out)

def dia(cx, cy, hw, hh, l1, l2, gold=False):
    g = " g" if gold else ""
    pts = f'{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}'
    return (f'<polygon class="dia{" gate" if gold else ""}" points="{pts}"/>'
            f'<text class="t{g}" x="{cx}" y="{cy-7}" text-anchor="middle" dominant-baseline="central">{esc(l1)}</text>'
            f'<text class="t{g}" x="{cx}" y="{cy+9}" text-anchor="middle" dominant-baseline="central">{esc(l2)}</text>')

def path(d, cls="con", mk="m"):
    return f'<path class="{cls}" d="{d}" marker-end="url(#{mk})"/>'

def lbl(x, y, s, anchor="middle"):
    return f'<text class="yn" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>'

# =====================================================================
# BUYER task flow, full, with every branch as a node
# =====================================================================
def buyer():
    W, H = 1860, 340
    e = [f'<svg class="flowsvg" style="min-width:{W}px" viewBox="0 0 {W} {H}" role="img" aria-label="Buyer task flow chart with every branch">',
         f'<defs>{MARK.format(i="m",g="")}{MARK.format(i="mg",g=" g")}</defs>']
    sy = 70
    bw, bh, gap = 190, 72, 24
    x = 16
    C = {}  # centers/edges by id
    spine = [
        ("find","box start","Find a lot","Catalogue, filtered by category and seller record"),
        ("read","box","Read the dossier","Six plates, sealed before the lot went live"),
        ("offer","box","Make an offer","Price, and how long it stands: 24h, 3 or 7 days"),
        ("hold","box","Card hold placed","A hold, never a charge. It makes the offer credible"),
        ("D_ans","dia","Seller","answers?"),
        ("fund","box","Fund escrow","24 hours to transfer. Card settles under $5,000"),
        ("watch","box","Watch the checkpoint","Money held, piece already in vault custody"),
        ("D_pre","dia gate","Pre-release","check?"),
        ("ship","box term","Shipped to you","Money releases to the seller the same moment"),
    ]
    for el in spine:
        if el[1].startswith("dia"):
            hw, hh = 66, 46
            cx = x + hw
            gold = "gate" in el[1]
            e.append(dia(cx, sy, hw, hh, el[2], el[3], gold))
            C[el[0]] = dict(l=cx-hw, r=cx+hw, cx=cx, b=sy+hh, t=sy-hh)
            x = cx + hw + gap
        else:
            e.append(box(x, sy-bh/2, bw, bh, el[2], el[3], el[1]))
            C[el[0]] = dict(l=x, r=x+bw, cx=x+bw/2, b=sy+bh/2, t=sy-bh/2)
            x += bw + gap
    # spine connectors
    order = [s[0] for s in spine]
    for a, b in zip(order, order[1:]):
        gold = (a == "D_pre")
        e.append(path(f'M{C[a]["r"]} {sy} H{C[b]["l"]}', "con g" if gold else "con", "mg" if gold else "m"))
    e.append(lbl(C["D_ans"]["r"]+16, sy-9, "YES"))
    e.append(lbl(C["D_pre"]["r"]+16, sy-9, "PASS"))
    # branch: seller answers -> 4 endings (bus below)
    ends = [
        ("Countered","48 hours to answer. The hold carries over. Accept, counter back, or walk"),
        ("Declined","Nothing charged, hold released the same day"),
        ("Expired","Unanswered past the window you set. It lapses on its own"),
        ("Lapsed, unfunded","Accepted, but the money did not arrive inside 24 hours"),
    ]
    ew, eh, egap = 200, 86, 18
    ey = 200
    total = len(ends)*ew + (len(ends)-1)*egap
    ex0 = C["D_ans"]["cx"] - total/2
    if ex0 < 16: ex0 = 16
    busy = 165
    e.append(f'<path class="con" d="M{C["D_ans"]["cx"]} {C["D_ans"]["b"]} V{busy}"/>')
    e.append(lbl(C["D_ans"]["cx"]+8, C["D_ans"]["b"]+18, "OTHER", "start"))
    # horizontal bus
    centers = [ex0 + i*(ew+egap) + ew/2 for i in range(len(ends))]
    e.append(f'<path class="con" d="M{centers[0]} {busy} H{centers[-1]}"/>')
    for cx, (t, d) in zip(centers, ends):
        e.append(f'<path class="con" d="M{cx} {busy} V{ey}" marker-end="url(#m)"/>')
        e.append(box(cx-ew/2, ey, ew, eh, t, d, "box dash", tw=30))
    e.append(lbl(ex0-4, busy-8, "offer ends → My deals", "start"))
    # branch: pre-release fail -> refunded
    ry = 200
    e.append(f'<path class="con" d="M{C["D_pre"]["cx"]} {C["D_pre"]["b"]} V{ry}" marker-end="url(#m)"/>')
    e.append(lbl(C["D_pre"]["cx"]+8, C["D_pre"]["b"]+18, "FAIL", "start"))
    e.append(box(C["D_pre"]["cx"]-ew/2, ry, ew, eh, "Refunded in full", "Refund starts itself. Seller carries the return", "box dash", tw=30))
    e.append("</svg>")
    return "\n".join(e)

# =====================================================================
# SELLER task flow, full, with every branch as a node
# =====================================================================
def seller():
    W, H = 2020, 340
    e = [f'<svg class="flowsvg" style="min-width:{W}px" viewBox="0 0 {W} {H}" role="img" aria-label="Seller task flow chart with every branch">',
         f'<defs>{MARK.format(i="m",g="")}{MARK.format(i="mg",g=" g")}</defs>']
    sy = 70
    bw, bh, gap = 190, 72, 24
    x = 16
    C = {}
    spine = [
        ("open","box gate","Open a seller account","Individual: ID, 3 live lots. Trade: registration, no limit"),
        ("desc","box","Describe the piece","Model, year, papers, asking price, condition as you see it"),
        ("intake","box","Ship once, to intake","Book a slot. The piece enters vault custody and stays"),
        ("D_read","dia gate","The","reading?"),
        ("pub","box","Dossier published","All six plates, including the ones that count against it"),
        ("D_offer","dia","Offer","arrives?"),
        ("bfund","box","Buyer funds escrow","24 hours. You ship nothing, it is already here"),
        ("D_pre","dia gate","Pre-release","check?"),
        ("rel","box term","Released to you","Sale price less 8% commission and the $150 reading"),
        ("rec","box dash","Record updated","214 sales, 0 disputes, 1 unwind, 2 failed readings"),
    ]
    for el in spine:
        if el[1].startswith("dia"):
            hw, hh = 66, 46
            cx = x + hw
            e.append(dia(cx, sy, hw, hh, el[2], el[3], "gate" in el[1]))
            C[el[0]] = dict(l=cx-hw, r=cx+hw, cx=cx, b=sy+hh, t=sy-hh)
            x = cx + hw + gap
        else:
            e.append(box(x, sy-bh/2, bw, bh, el[2], el[3], el[1]))
            C[el[0]] = dict(l=x, r=x+bw, cx=x+bw/2, b=sy+bh/2, t=sy-bh/2)
            x += bw + gap
    order = [s[0] for s in spine]
    for a, b in zip(order, order[1:]):
        gold = a in ("D_pre",)
        e.append(path(f'M{C[a]["r"]} {sy} H{C[b]["l"]}', "con g" if gold else "con", "mg" if gold else "m"))
    e.append(lbl(C["D_read"]["r"]+16, sy-9, "PASS"))
    e.append(lbl(C["D_offer"]["r"]+16, sy-9, "ACCEPT"))
    e.append(lbl(C["D_pre"]["r"]+16, sy-9, "PASS"))
    ew, eh = 200, 86
    ey, busy = 200, 165
    def drop(cx, t, d, label):
        e.append(f'<path class="con" d="M{cx} {C["_b"]} V{ey}" marker-end="url(#m)"/>')
    # reading -> failed at intake
    e.append(f'<path class="con" d="M{C["D_read"]["cx"]} {C["D_read"]["b"]} V{ey}" marker-end="url(#m)"/>')
    e.append(lbl(C["D_read"]["cx"]+8, C["D_read"]["b"]+18, "FAIL", "start"))
    e.append(box(C["D_read"]["cx"]-ew/2, ey, ew, eh, "Failed at intake", "Never lists. Returned at your cost, published to your record anyway", "box dash", tw=30))
    # offer -> countered/declined + expired/unfunded (two)
    o_ends = [("Countered or declined","The lot stays live and keeps taking offers"),
              ("Expired or unfunded","Nothing owed either way. The lot returns to live")]
    oc = C["D_offer"]["cx"]
    ocenters = [oc-(ew/2+9), oc+(ew/2+9)]
    e.append(f'<path class="con" d="M{oc} {C["D_offer"]["b"]} V{busy}"/>')
    e.append(lbl(oc+8, C["D_offer"]["b"]+18, "OTHER", "start"))
    e.append(f'<path class="con" d="M{ocenters[0]} {busy} H{ocenters[1]}"/>')
    for cx,(t,d) in zip(ocenters,o_ends):
        e.append(f'<path class="con" d="M{cx} {busy} V{ey}" marker-end="url(#m)"/>')
        e.append(box(cx-ew/2, ey, ew, eh, t, d, "box dash", tw=30))
    # pre-release -> failed pre-release
    e.append(f'<path class="con" d="M{C["D_pre"]["cx"]} {C["D_pre"]["b"]} V{ey}" marker-end="url(#m)"/>')
    e.append(lbl(C["D_pre"]["cx"]+8, C["D_pre"]["b"]+18, "FAIL", "start"))
    e.append(box(C["D_pre"]["cx"]-ew/2, ey, ew, eh, "Failed pre-release", "Buyer refunded in full, piece returns to you, outcome recorded", "box dash", tw=30))
    e.append("</svg>")
    return "\n".join(e)

# =====================================================================
# IA tree, connected org-chart across 3 access zones
# =====================================================================
def ia():
    W = 2060
    e = [f'<svg class="flowsvg" style="min-width:{W}px" viewBox="0 0 {W} 980" role="img" aria-label="Information architecture tree: 27 screens across 3 access zones">',
         f'<defs>{MARK.format(i="m",g="")}{MARK.format(i="mg",g=" g")}</defs>']
    zones = [
        ("Zone 1 · Public","No account", "box start", [
            ("Home",""),("Catalogue","Bags · Shoes · Watches"),("The piece","Plates · Condition · Price"),
            ("The dossier","Six plates, sealed"),("Seller record","Sales · Disputes · Failures"),
            ("Help",""),("Contact",""),("Sign in","gate"),("Create account","gate"),
        ]),
        ("Zone 2 · Buyer","Offers, escrow", "box gate", [
            ("Offer flow","Price · Duration · Hold"),("Fund escrow","24h from acceptance"),("Cart",""),
            ("The checkpoint","Money · Item · Pass"),("The reading","Plate by plate"),
            ("My deals","Out · Accepted · Resolved"),("Settings","Cards · City · Storage"),
        ]),
        ("Zone 3 · Seller","Individual or trade", "box gate", [
            ("Inventory & desk","Offers · Vault · Payouts"),("Sell & intake","Describe · Book · Ship"),
            ("Settings","Payout · Tier upgrade"),("Public record","gate-sys"),
        ]),
    ]
    cw, chh, cgap = 168, 60, 14
    py = 60           # parent row y-top
    for zi,(zt, zsub, zcls, kids) in enumerate(zones):
        zy = 60 + zi*310
        # parent node centered over children
        total = len(kids)*cw + (len(kids)-1)*cgap
        x0 = 16
        centers = [x0 + i*(cw+cgap) + cw/2 for i in range(len(kids))]
        pcx = sum(centers)/len(centers)
        e.append(box(pcx-110, zy, 220, 64, zt, zsub, zcls))
        pbot = zy+64
        busy = zy+108
        kidy = zy+140
        # bus
        e.append(f'<path class="con" d="M{pcx} {pbot} V{busy}"/>')
        e.append(f'<path class="con" d="M{centers[0]} {busy} H{centers[-1]}"/>')
        for cx,(t,sub) in zip(centers, kids):
            cls = "box"
            if sub=="gate": cls, sub = "box gate", ""
            elif sub=="gate-sys": cls, sub = "box dash", "System-written"
            e.append(f'<path class="con" d="M{cx} {busy} V{kidy}" marker-end="url(#m)"/>')
            e.append(box(cx-cw/2, kidy, cw, chh, t, sub, cls, tw=24))
    e.append("</svg>")
    return "\n".join(e)

import sys
which = sys.argv[1]
print({"buyer":buyer,"seller":seller,"ia":ia}[which]())
