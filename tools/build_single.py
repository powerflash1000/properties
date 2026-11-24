#!/usr/bin/env python3
"""Build a single self-contained HTML (model inlined) from viewer/index.html + apartments/<id>/model.json.
usage: python3 tools/build_single.py apt1 out.html
Used to publish the viewer as a Claude artifact or to open it from a single file."""
import json, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
apt = sys.argv[1] if len(sys.argv) > 1 else 'apt1'
out = sys.argv[2] if len(sys.argv) > 2 else f'{apt}.html'
model = json.loads((root / 'apartments' / apt / 'model.json').read_text(encoding='utf-8'))
html = (root / 'viewer' / 'index.html').read_text(encoding='utf-8')
marker = "<script>\n'use strict';"
assert marker in html, 'viewer script marker not found'
html = html.replace(marker, '<script>window.MODEL_INLINE=' + json.dumps(model, ensure_ascii=False) + ';</script>\n' + marker, 1)
html = html.replace("get('apt')||'apt1'", "get('apt')||'" + apt + "'")
pathlib.Path(out).write_text(html, encoding='utf-8')
print('wrote', out, len(html))
