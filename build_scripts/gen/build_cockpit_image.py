#!/usr/bin/env python3
"""Build WORK/assets/a330_cockpit.jpg from src/'A330 All Panels FULL SIZE.pdf' (Airbus A330 light test
poster, one page). pdftoppm at 120 dpi, crop the overhead, main panel + glareshield and pedestal
(dropping the ILS/VOR display insets and the engine-variant insets), stack them on a 1200x1748 white
canvas (300:437, the flows_quiz map viewBox), JPEG quality 72. Writes img/layout.json with the
placement of each crop; gen_flows_trainer.py maps panel coordinates through it."""
import subprocess, json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, 'img'), exist_ok=True)
subprocess.run(['pdftoppm', '-r', '120', '-png', os.path.join(HERE, 'src', 'A330 All Panels FULL SIZE.pdf'), os.path.join(HERE, 'img', 'hi')], check=True)
im = Image.open(os.path.join(HERE, 'img', 'hi-1.png')).convert('RGB')
s = im.size[0] / 796   # crop boxes were read on a 796 px wide (40 dpi) preview
def crop(x0, y0, x1, y1): return im.crop((int(x0*s), int(y0*s), int(x1*s), int(y1*s)))
oh = crop(276, 6, 524, 480); mp = crop(20, 484, 778, 730); pd = crop(288, 732, 510, 1100)
for n, c in [('oh', oh), ('mp', mp), ('pd', pd)]: c.save(os.path.join(HERE, 'img', f'{n}.png'))
W = 1200; H = round(W * 437 / 300); gap = 12
fit_h = lambda im, h: im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
fit_w = lambda im, w: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
oh2 = fit_h(oh, 720); mp2 = fit_w(mp, W); pd2 = fit_h(pd, H - 720 - mp2.height - 3 * gap)
canvas = Image.new('RGB', (W, H), (255, 255, 255))
y = gap; canvas.paste(oh2, ((W - oh2.width) // 2, y)); y += oh2.height + gap
canvas.paste(mp2, (0, y)); y += mp2.height + gap
canvas.paste(pd2, ((W - pd2.width) // 2, y))
out = os.path.join(HERE, 'work', 'assets', 'a330_cockpit.jpg')
canvas.save(out, quality=72, optimize=True, progressive=True)
json.dump({'W': W, 'H': H, 'oh': [(W - oh2.width) // 2, gap, oh2.width, oh2.height], 'mp': [0, gap + oh2.height + gap, mp2.width, mp2.height],
           'pd': [(W - pd2.width) // 2, gap * 3 + oh2.height + mp2.height, pd2.width, pd2.height]}, open(os.path.join(HERE, 'img', 'layout.json'), 'w'))
print(out, os.path.getsize(out), 'bytes')
