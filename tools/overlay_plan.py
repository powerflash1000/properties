#!/usr/bin/env python3
"""Overlay a model's walls/openings on the original plan photo to check registration.
usage: python3 tools/overlay_plan.py PHOTO MODEL.json OUT.png [px0 pz0 scale]
Default mapping (apt1): px = 100 + 61*x, py = 35 + 61*z (photo pixels, EXIF-corrected).
Red = walls, green = doors, blue = windows/balcony doors, orange = arches."""
import json, sys
from PIL import Image, ImageOps, ImageDraw
photo, model, out = sys.argv[1:4]
px0, pz0, sc = (float(v) for v in sys.argv[4:7]) if len(sys.argv) >= 7 else (100, 35, 61)
im = ImageOps.exif_transpose(Image.open(photo)).convert('RGBA')
m = json.load(open(model, encoding='utf-8'))
ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
X = lambda x: px0 + sc * x; Z = lambda z: pz0 + sc * z
for w in m['walls']:
    t = max(2, int(w['t'] * sc))
    seg = [(X(w['p']), Z(w['a'])), (X(w['p']), Z(w['b']))] if w['ax'] == 'v' else [(X(w['a']), Z(w['p'])), (X(w['b']), Z(w['p']))]
    d.line(seg, fill=(255, 0, 0, 140), width=t)
    for o in w.get('op', []):
        ow = {'door': 1.0, 'front': 1.0, 'slide': 1.5}.get(o['ty'], o.get('w', 1.0))
        if o['ty'] == 'door' and o.get('w'): ow = o['w']
        a, b = o['c'] - ow / 2, o['c'] + ow / 2
        col = {'win': (0, 120, 255, 230), 'door': (0, 200, 0, 230), 'front': (0, 200, 0, 230), 'slide': (0, 160, 255, 230), 'arch': (255, 160, 0, 230)}[o['ty']]
        s2 = [(X(w['p']), Z(a)), (X(w['p']), Z(b))] if w['ax'] == 'v' else [(X(a), Z(w['p'])), (X(b), Z(w['p']))]
        d.line(s2, fill=col, width=t + 6)
Image.alpha_composite(im, ov).convert('RGB').save(out)
print('wrote', out)
