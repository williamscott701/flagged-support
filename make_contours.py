#!/usr/bin/env python3
"""Writes contours.svg, the faint topographic backdrop used by the support pages."""
import numpy as np
import contourpy

W, H, N = 900, 900, 180
rng = np.random.default_rng(23)
y, x = np.mgrid[0:1:complex(0, N), 0:1:complex(0, N)]
z = np.zeros_like(x)
for _ in range(10):
    cx, cy = rng.uniform(-0.1, 1.1, 2)
    r = rng.uniform(0.1, 0.3)
    z += rng.choice([1.0, 1.0, -0.6]) * rng.uniform(0.6, 1.2) * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r))
gen = contourpy.contour_generator(x, y, z)
paths = []
for i, level in enumerate(np.linspace(z.min(), z.max(), 18)[1:-1]):
    width = 1.6 if (i + 1) % 4 == 0 else 0.8
    for seg in gen.lines(level):
        d = "M" + " L".join(f"{px * W:.1f},{py * H:.1f}" for px, py in seg)
        paths.append(f'<path d="{d}" stroke-width="{width}"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<g fill="none" stroke="rgb(150,110,60)" stroke-opacity="0.2" stroke-linecap="round">'
       + "".join(paths) + "</g></svg>")
open("contours.svg", "w").write(svg)
print(len(paths), "paths")
