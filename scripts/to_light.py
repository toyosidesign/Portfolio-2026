"""Convert a dark-theme case-study page to the light theme (Grey + Royal palettes).

Usage: python3 scripts/to_light.py Page.html [...]
Rewrites Tailwind colour classes inside class="..." attributes and JS template
strings, plus the shared header/footer inline styles. Page-specific <style>
blocks and inline style="" colours still need a manual pass afterwards.
"""
import re, sys

# Solid backgrounds that are dark/coloured: white text on these must stay white.
DARK_BG = re.compile(r'(?<![\w:-])(bg-(accent|royal-[6-9]|royal-10|grey-[5-9]|grey-10|black(/[6-9]\d)?|black/\[0\.[6-9]\d*\]|\[#(0|1|2|3)[0-9a-fA-F]{5}\]|\[#[0-9a-fA-F]{6}\]|(blue|green|red|emerald|indigo|violet|sky|cyan|amber|orange|rose|slate)-[5-9]00|gradient-to-[a-z]+)|from-ink)(?![\w/-])')

WHITE_ALPHA = {  # bg-white/x on dark  ->  bg-black/y on light
    '5': '[0.03]', '10': '[0.05]', '15': '[0.06]', '20': '[0.08]', '25': '[0.10]', '30': '[0.12]',
    '[0.02]': '[0.02]', '[0.03]': '[0.025]', '[0.04]': '[0.03]', '[0.05]': '[0.03]', '[0.06]': '[0.04]',
    '[0.08]': '[0.05]', '[0.09]': '[0.05]', '[0.18]': '[0.08]',
}
TEXT = {
    'text-[#c7c7cc]': 'text-grey-5', 'text-[#a1a1aa]': 'text-[#555555]', 'text-[#8a8a8a]': 'text-grey-4',
    'text-[#c0c0c0]': 'text-grey-4', 'text-[#6b6b6b]': 'text-grey-4', 'text-[#5a5a5a]': 'text-grey-4',
    'text-[#e6e6e6]': 'text-grey-6', 'text-[#f2f2f7]': 'text-grey-5',
    'text-white/70': 'text-grey-5', 'text-white/60': 'text-grey-4',
}
SIMPLE = {
    'bg-base': 'bg-white', 'bg-card': 'bg-[#f7f7fa]', 'bg-panel': 'bg-royal-1',
    'bg-header/90': 'bg-white/85', 'border-[#3d3e3f]': 'border-grey-1',
}

def conv_token(tok, dark_ctx):
    pre, _, core = tok.rpartition(':')
    pre = pre + ':' if pre else ''
    if core in SIMPLE: return pre + SIMPLE[core]
    if core.startswith('bg-card/'): return pre + 'bg-[#f7f7fa]/' + core.split('/', 1)[1]
    if core in TEXT and not dark_ctx: return pre + TEXT[core]
    if core == 'text-white' and not dark_ctx: return pre + 'text-grey-8'
    m = re.fullmatch(r'(border|divide|ring)-white/(\S+)', core)
    if m: return f'{pre}{m.group(1)}-black/{m.group(2)}'
    m = re.fullmatch(r'bg-white/(\S+)', core)
    if m and m.group(1) in WHITE_ALPHA and not dark_ctx: return f'{pre}bg-black/{WHITE_ALPHA[m.group(1)]}'
    m = re.fullmatch(r'(text|bg|border|from|to|via|ring|fill|stroke|decoration|outline)-accent(/\S+)?', core)
    if m: return f'{pre}{m.group(1)}-royal-7{m.group(2) or ""}'
    m = re.fullmatch(r'shadow-\[(.*)\]', core)
    if m and 'rgba(0,0,0,' in m.group(1):
        val = re.sub(r'rgba\(0,0,0,(0?\.\d+)\)', lambda a: f'rgba(16,16,16,{min(0.14, round(float(a.group(1)) * 0.25, 3))})', m.group(1))
        return f'{pre}shadow-[{val}]'
    return tok

DARK_PANELS = {'bg-[#0e0c0a]', 'bg-[#0a0a0a]', 'bg-black'}
TINT_TEXT = {'text-amber': 'text-amber-700', 'text-leader': 'text-amber-700', 'text-company': 'text-emerald-700',
             'text-cyan': 'text-cyan-700', 'text-primary/70': 'text-primary', 'text-amber/90': 'text-amber-700'}

def conv_tint(tok):
    pre, _, core = tok.rpartition(':'); pre = pre + ':' if pre else ''
    if core in TINT_TEXT: return pre + TINT_TEXT[core]
    m = re.fullmatch(r'text-(red|amber|emerald|green|sky|blue|cyan|violet|rose|orange|yellow|indigo|purple|pink|teal|lime)-(100|200|300|400)(/\S+)?', core)
    if m: return f'{pre}text-{m.group(1)}-700{m.group(3) or ""}'
    m = re.fullmatch(r'text-\[(#[0-9a-fA-F]{6})\]', core)
    if m:
        new = map_color(_hex(m.group(1)), 'text')
        if new.lower() != m.group(1).lower(): return f'{pre}text-[{new}]'
    return tok

def conv_classes(cls):
    cls = ' '.join('bg-[#f7f7fa]' if t in DARK_PANELS else t for t in cls.split())
    toks = cls.split()
    dark = bool(DARK_BG.search(cls))
    out = [conv_token(t, dark) for t in toks]
    if not dark: out = [conv_tint(t) for t in out]
    # buttons that were pink-with-black-text become royal-with-white-text
    if re.search(r'(?<![\w:/-])bg-(accent|royal-7)(?![\w/-])', cls):
        out = ['text-white' if t in ('text-black', 'text-panel', 'text-base', 'text-grey-8') else
               'hover:bg-royal-8' if t in ('hover:bg-white', 'hover:brightness-95', 'hover:brightness-110') else t for t in out]
    return ' '.join(out)

def convert(s):
    s = re.sub(r'class="([^"]*)"', lambda m: 'class="' + conv_classes(m.group(1)) + '"', s)
    s = re.sub(r"class='([^']*)'", lambda m: "class='" + conv_classes(m.group(1)) + "'", s)
    s = s.replace('::selection { background: #ffd8e4; color: #000; }', '::selection { background: #dedefd; color: #101010; }')
    # shared footer
    s = s.replace('background: radial-gradient(120% 100% at 50% -10%, #1b1618 0%, #130f0e 42%, #0b0a0a 100%);',
                  'background: radial-gradient(120% 100% at 50% -10%, #dedefd 0%, #f1f1fe 42%, #ffffff 100%);')
    s = s.replace('rounded-full bg-white text-black px-5 py-3 text-sm font-semibold hover:bg-white/90 transition',
                  'rounded-full bg-grey-8 text-white px-5 py-3 text-sm font-semibold hover:bg-grey-5 transition')
    s = s.replace('rounded-full bg-black/[0.05] text-grey-5 hover:bg-black/[0.08] hover:text-grey-8 transition-colors',
                  'rounded-full bg-royal-1 text-royal-8 hover:bg-royal-7 hover:text-white transition-colors')
    s = s.replace('<div class="border-t border-black/10">\n      <div class="max-w-[1520px] mx-auto px-6 py-5',
                  '<div class="border-t border-black/10 bg-white">\n      <div class="max-w-[1520px] mx-auto px-6 py-5')
    return s

# ---------------------------------------------------------------------------
# Pass 2: colours inside <style> blocks and style="" attributes.
import colorsys

def _hex(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _out(rgb): return '#%02x%02x%02x' % tuple(max(0, min(255, round(c))) for c in rgb)

def _hls(rgb): return colorsys.rgb_to_hls(*(c / 255 for c in rgb))

def _grey(l): v = l * 255; return _out((v, v, v))

PINK = {(255, 216, 228), (255, 200, 216)}

def map_color(rgb, kind, alpha=None):
    """kind: 'text' | 'bg' | 'border' | 'shadow'"""
    if rgb in PINK: rgb2 = (100, 101, 210)
    else:
        h, l, s = _hls(rgb)
        neutral = s < 0.2 or max(rgb) - min(rgb) < 28
        rgb2 = rgb
        if alpha is not None:
            if rgb == (255, 255, 255): rgb2 = (16, 16, 16)
            elif max(rgb) < 40 and kind == 'shadow':
                return f'rgba(16,16,16,{min(0.14, round(alpha * 0.3, 3))})'
            elif max(rgb) < 40 and kind == 'bg' and alpha < 0.6: rgb2 = (16, 16, 16); alpha = round(alpha * 0.1, 3)
        elif kind == 'text' and not neutral and l > 0.62:
            r, g, b = colorsys.hls_to_rgb(h, 0.36, min(s, 0.75)); rgb2 = (r * 255, g * 255, b * 255)
        elif neutral:
            if kind == 'text':
                if l > 0.6: rgb2 = _hex(_grey(max(0.06, 1.04 - l)))
                elif l >= 0.35: rgb2 = _hex(_grey(0.97 - l))
            elif kind in ('bg', 'border'):
                if l < 0.12: rgb2 = (247, 247, 250)
                elif l < 0.2: rgb2 = (238, 238, 243)
                elif l < 0.35: rgb2 = (225, 225, 232)
    if alpha is not None:
        return f'rgba({rgb2[0]},{rgb2[1]},{rgb2[2]},{alpha})'
    return _out(rgb2)

COLOR_RE = re.compile(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+\s*)?\)')

def _conv_value(prop, val):
    p = prop.strip().lower()
    if p == 'color' or p in ('fill', 'caret-color', '-webkit-text-fill-color'): kind = 'text'
    elif 'shadow' in p: kind = 'shadow'
    elif p.startswith('border') or p.startswith('outline'): kind = 'border'
    elif p.startswith('background') or p == 'stroke': kind = 'bg'
    else: return val
    def rep(m):
        t = m.group(0)
        if t.startswith('#'): return map_color(_hex(t), kind)
        nums = [float(x) for x in re.findall(r'[\d.]+', t)]
        rgb = tuple(int(x) for x in nums[:3]); a = nums[3] if len(nums) > 3 else None
        return map_color(rgb, kind, a)
    return COLOR_RE.sub(rep, val)

def _block_bg(css):
    """Background colour a declaration block keeps after conversion (or None)."""
    m = re.search(r'background(?:-color)?\s*:\s*([^;]+)', css)
    if not m: return None, False
    c = COLOR_RE.search(m.group(1))
    if not c or c.group(0).startswith('rgba'): return None, False
    rgb = _hex(c.group(0)) if c.group(0).startswith('#') else tuple(int(x) for x in re.findall(r'\d+', c.group(0))[:3])
    return _hex(map_color(rgb, 'bg')), rgb in PINK

def conv_decls(css):
    bg, was_pink = _block_bg(css)
    keep_text = bg is not None and _hls(bg)[1] < 0.6   # text sits on a dark/saturated fill
    def one(m):
        prop, sep, val = m.group(1), m.group(2), m.group(3)
        if prop.strip().lower() == 'color':
            if was_pink: return prop + sep + '#ffffff'
            if keep_text: return m.group(0)
        return prop + sep + _conv_value(prop, val)
    return re.sub(r'([a-zA-Z-]+)(\s*:\s*)([^;{}"]+)', one, css)

def _fix_inline_fills(s):
    def tag(m):
        t = m.group(0)
        bg = re.search(r'style="[^"]*background(?:-color)?:\s*(#[0-9a-fA-F]{6})', t)
        if bg and 'text-grey-8' in t and _hls(_hex(bg.group(1)))[1] < 0.5:
            t = t.replace('text-grey-8', 'text-white')
        return t
    return re.sub(r'<[a-z]+\b[^>]*>', tag, s)

def convert_css(s):
    s = _fix_inline_fills(s)
    s = re.sub(r'(<style>)(.*?)(</style>)', lambda m: m.group(1) + re.sub(r'\{([^{}]*)\}', lambda b: '{' + conv_decls(b.group(1)) + '}', m.group(2), flags=re.S) + m.group(3), s, flags=re.S)
    s = re.sub(r'style="([^"]*)"', lambda m: 'style="' + conv_decls(m.group(1)) + '"', s)
    return s

if __name__ == '__main__':
    for p in sys.argv[1:]:
        src = open(p).read(); out = convert_css(convert(src))
        open(p, 'w').write(out); print(p, 'changed' if out != src else 'unchanged')

