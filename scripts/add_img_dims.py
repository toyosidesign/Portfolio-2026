#!/usr/bin/env python3
"""Add intrinsic width/height attributes to <img> tags that reference an
existing assets/*.webp, so browsers reserve aspect-ratio space and avoid CLS.
Skips tags that already have a width= attribute. Only touches single-line img tags."""
import os, re, glob
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG_TAG = re.compile(r'<img\b[^>]*?>', re.IGNORECASE)
SRC = re.compile(r'src="(assets/[^"]+\.webp)"')
HAS_WH = re.compile(r'\bwidth=')

dims_cache = {}
def dims(path):
    if path not in dims_cache:
        with Image.open(os.path.join(ROOT, path)) as im:
            dims_cache[path] = im.size
    return dims_cache[path]

total = 0
for html in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    with open(html, encoding="utf-8") as f:
        text = f.read()
    edits = [0]

    def repl(m):
        tag = m.group(0)
        if HAS_WH.search(tag):
            return tag
        s = SRC.search(tag)
        if not s:
            return tag
        p = s.group(1)
        if not os.path.exists(os.path.join(ROOT, p)):
            return tag
        w, h = dims(p)
        edits[0] += 1
        # insert width/height right after "<img"
        return tag.replace("<img", f'<img width="{w}" height="{h}"', 1)

    new = IMG_TAG.sub(repl, text)
    if edits[0]:
        with open(html, "w", encoding="utf-8") as f:
            f.write(new)
        total += edits[0]
        print(f"{os.path.basename(html):20s} +{edits[0]} imgs")

print(f"\nAdded width/height to {total} images")
