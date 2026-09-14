import json, base64, math, random

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def b64_file(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

def load_name_paths(path='assets/name_paths.json'):
    with open(path) as f:
        return json.load(f)

def typing_clip_rect(clip_id, x, y, full_w, height, dur, begin, fill='freeze', repeatCount='1'):
    """A clipPath containing a rect whose width animates 0 -> full_w (typewriter reveal).
    Height is padded generously so no font ever clips vertically."""
    return f'''<clipPath id="{clip_id}" clipPathUnits="userSpaceOnUse">
<rect x="{x}" y="{y}" width="0" height="{height}">
<animate attributeName="width" from="0" to="{full_w}" dur="{dur}" begin="{begin}" fill="{fill}" repeatCount="{repeatCount}" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
</rect>
</clipPath>'''

def cycling_clip_rect(clip_id, x, y, full_w, height, cycle_dur, slot_start, slot_dur, type_frac=0.14, hold_frac=0.72):
    """Repeats forever: width 0 -> full over type_frac*slot, holds, then back to 0 over remaining, silent elsewhere."""
    t0 = slot_start
    t_type_end = slot_start + slot_dur * type_frac
    t_hold_end = slot_start + slot_dur * (type_frac + hold_frac)
    t_del_end = slot_start + slot_dur
    def frac(t): return round(t / cycle_dur, 5)
    keyTimes = [0, frac(t0), frac(t_type_end), frac(t_hold_end), frac(t_del_end), 1]
    values = [0, 0, full_w, full_w, 0, 0]
    # de-dup / ensure monotonic increasing keyTimes
    kt, vv = [], []
    last = -1
    for k, v in zip(keyTimes, values):
        k = max(k, last + 0.00001) if kt else k
        kt.append(round(k, 5)); vv.append(v); last = kt[-1]
    kt_s = ';'.join(str(k) for k in kt)
    vv_s = ';'.join(str(v) for v in vv)
    return f'''<clipPath id="{clip_id}" clipPathUnits="userSpaceOnUse">
<rect x="{x}" y="{y}" width="0" height="{height}">
<animate attributeName="width" values="{vv_s}" keyTimes="{kt_s}" dur="{cycle_dur}s" begin="0s" repeatCount="indefinite" calcMode="linear"/>
</rect>
</clipPath>'''

def name_letters_svg(name_paths, x0, baseline_y, px_size, gradient_id, start_delay=0.15, step=0.11, dur=0.55):
    upm = name_paths['upm']
    scale = px_size / upm
    letters = name_paths['letters']
    out = [f'<g transform="translate({x0},{baseline_y}) scale({scale},{-scale})">']
    for i, l in enumerate(letters):
        begin = start_delay + i * step
        out.append(
            f'<g transform="translate({l["x"]},0)" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="{dur}s" begin="{begin}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'from="0 -160" to="0 0" dur="{dur}s" begin="{begin}s" fill="freeze" calcMode="spline" keySplines="0.2 0.6 0.25 1"/>'
            f'<path d="{l["d"]}" fill="url(#{gradient_id})"/>'
            f'</g>'
        )
    out.append('</g>')
    return ''.join(out)

def heart_path(cx, cy, s):
    # simple heart centered at cx,cy with rough size s
    return (f"M{cx} {cy+s*0.3} "
            f"C{cx-s} {cy-s*0.5} {cx-s*0.5} {cy-s*1.3} {cx} {cy-s*0.55} "
            f"C{cx+s*0.5} {cy-s*1.3} {cx+s} {cy-s*0.5} {cx} {cy+s*0.3} Z")

def gen_hearts(n, w, h, color, seed=1):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(0.05*w, 0.95*w)
        y0 = rnd.uniform(0.55*h, 1.05*h)
        size = rnd.uniform(5, 11)
        dur = rnd.uniform(7, 13)
        delay = rnd.uniform(0, 10)
        drift = rnd.uniform(-30, 30)
        opac = rnd.uniform(0.35, 0.75)
        out.append(
            f'<path d="{heart_path(0,0,size)}" fill="{color}" opacity="0" transform="translate({x},{y0})">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'from="0 0" to="{drift} {-h*0.85}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{opac};{opac};0" keyTimes="0;0.15;0.7;1" '
            f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</path>'
        )
    return ''.join(out)

def gen_sparkles(n, w, h, color, seed=2):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(0.02*w, 0.98*w)
        y = rnd.uniform(0.02*h, 0.98*h)
        size = rnd.uniform(2, 4.2)
        dur = rnd.uniform(1.6, 3.4)
        delay = rnd.uniform(0, 4)
        out.append(
            f'<g transform="translate({x},{y})">'
            f'<path d="M0,-{size*3} L{size*0.7},-{size*0.7} L{size*3},0 L{size*0.7},{size*0.7} '
            f'L0,{size*3} L-{size*0.7},{size*0.7} L-{size*3},0 L-{size*0.7},-{size*0.7} Z" '
            f'fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="scale" additive="sum" '
            f'values="0.3;1.15;0.3" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</path></g>'
        )
    return ''.join(out)

def gen_rising_particles(n, w, h, color, seed=3):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(0.03*w, 0.97*w)
        r = rnd.uniform(1.2, 2.6)
        dur = rnd.uniform(6, 12)
        delay = rnd.uniform(0, 10)
        drift = rnd.uniform(-18, 18)
        out.append(
            f'<circle cx="{x}" cy="{h+10}" r="{r}" fill="{color}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0 0" to="{drift} {-(h+40)}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.1;0.8;1" '
            f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return ''.join(out)

def gen_orbs(n, w, h, colors, seed=4):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(0.1*w, 0.9*w)
        y = rnd.uniform(0.1*h, 0.9*h)
        r = rnd.uniform(60, 140)
        c = colors[i % len(colors)]
        dur = rnd.uniform(5, 9)
        delay = rnd.uniform(0, 4)
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.10" filter="url(#orbBlur)">'
            f'<animate attributeName="opacity" values="0.06;0.18;0.06" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="r" values="{r};{r*1.15};{r}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return ''.join(out)
