#!/usr/bin/env python3
"""PAX variants of the cockpit art: paint out the BRK FAN label and pb (A330F only; the pax A330 has no
brake fans). Each row of the box is filled with the median panel grey of that row, so the panel's
vertical gradient carries through and the white divider lines either side stay. Box is in 4800 px
(a330_cockpit_hi.jpg) coordinates and scales to any width of the same layout.
  assets/a330_cockpit_hi.jpg -> assets/a330_cockpit_hi_pax.jpg
  assets/a330_cockpit.jpg    -> assets/a330_cockpit_pax.jpg"""
import os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BOX = (2916, 3493, 3009, 3612)   # x0, y0, x1, y1 at 4800 px wide: label + pb, inside the white lines
for src, dst, q in [('a330_cockpit_hi.jpg', 'a330_cockpit_hi_pax.jpg', 85), ('a330_cockpit.jpg', 'a330_cockpit_pax.jpg', 72)]:
    im = Image.open(os.path.join(ROOT, 'assets', src)).convert('RGB'); a = np.asarray(im).copy()
    k = im.width / 4800; x0, y0, x1, y1 = [round(v * k) for v in BOX]
    for y in range(y0, y1):
        ref = np.concatenate([a[y, x0 - max(1, round(3 * k)):x0], a[y, x1:x1 + max(1, round(3 * k))]])  # panel just inside the lines
        a[y, x0:x1] = np.median(ref, axis=0).astype(np.uint8)
    Image.fromarray(a).save(os.path.join(ROOT, 'assets', dst), quality=q, optimize=True, progressive=True)
    print(dst, (x0, y0, x1, y1))
