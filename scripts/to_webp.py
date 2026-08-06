#!/usr/bin/env python3
"""Convert all PNG/JPG images in assets/ to WebP. Originals are kept as fallback."""
import os
from PIL import Image

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
QUALITY = 82  # visually lossless for UI screenshots, big size win

before = after = 0
converted = 0
for name in sorted(os.listdir(ASSETS)):
    ext = name.lower().rsplit(".", 1)[-1]
    if ext not in ("png", "jpg", "jpeg"):
        continue
    src = os.path.join(ASSETS, name)
    dst = os.path.join(ASSETS, name.rsplit(".", 1)[0] + ".webp")
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        continue  # already converted
    im = Image.open(src)
    # Preserve alpha where present; WebP supports it.
    save_kwargs = {"quality": QUALITY, "method": 4}
    im.save(dst, "WEBP", **save_kwargs)
    b, a = os.path.getsize(src), os.path.getsize(dst)
    before += b
    after += a
    converted += 1
    print(f"{name:48s} {b//1024:5d}KB -> {a//1024:5d}KB")

print(f"\n{converted} images: {before//1024//1024:.0f}MB -> {after//1024//1024:.0f}MB "
      f"({100*(before-after)//before}% smaller)")
