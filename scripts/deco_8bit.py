#!/usr/bin/env python3
"""Grain 8 bits et formes de décor pixel pour le site SYNEO.

Usage : python3 scripts/deco_8bit.py → assets/img/deco/
  grain-clair.png / grain-sombre.png : textures de petits carrés (à répéter)
  engrenage, tuyau, etincelle, anneau, zigzag, croix : décors pixel en contour (SVG)
"""
import math
import pathlib
import random

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "deco"


def grain(name, color, n=170, size=96, cell=3, alphas=(14, 22, 34)):
    rnd = random.Random(name)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for _ in range(n):
        x, y = rnd.randrange(0, size, cell), rnd.randrange(0, size, cell)
        a = rnd.choice(alphas)
        for dx in range(cell):
            for dy in range(cell):
                im.putpixel((x + dx, y + dy), color + (a,))
    im.save(OUT / f"{name}.png", optimize=True)


def svg_from(cells, w, h, color, title):
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for x, y in sorted(cells))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" '
            f'aria-hidden="true"><title>{title}</title><g fill="{color}">{rects}</g></svg>\n')


def ring_cells(cx, cy, r1, r2, w, h):
    return {(x, y) for y in range(h) for x in range(w)
            if r1 <= math.hypot(x + .5 - cx, y + .5 - cy) <= r2}


def engrenage():
    w = h = 24
    c = ring_cells(12, 12, 6.2, 8, w, h) | ring_cells(12, 12, 2, 3.2, w, h)
    for k in range(8):                                       # dents
        a = k * math.pi / 4
        for r in (8.5, 9.5, 10.5):
            for s in (-1, 0, 1):
                x = 12 + math.cos(a) * r - math.sin(a) * s
                y = 12 + math.sin(a) * r + math.cos(a) * s
                c.add((int(x), int(y)))
    return c, w, h


def tuyau():
    w, h = 40, 22
    c = set()
    for x in range(0, 26):                                   # tuyau horizontal
        c |= {(x, 4), (x, 9)}
    for y in range(4, 22):                                   # coude qui descend
        c |= {(26 + (1 if y > 6 else 0), y)} if y < 6 else {(27, y), (32, y)} if y > 9 else set()
    for x in range(26, 33):
        c.add((x, 4 if x < 30 else 4))
    c |= {(28, 5), (29, 6), (30, 7), (31, 8), (32, 9), (26, 9), (27, 10)}
    for x in range(25, 35):                                  # bride
        c |= {(x, 18), (x, 19)}
    for y in range(1, 13):                                   # bride verticale
        c |= {(14, y), (15, y)} if y in (1, 2, 11, 12) else set()
    for x in range(12, 18):
        c |= {(x, 1), (x, 12)}
    for y in range(1, 13):
        c |= {(12, y), (17, y)}
    return c, w, h


def etincelle():
    w = h = 13
    c = {(6, y) for y in range(13)} | {(x, 6) for x in range(13)}
    c |= {(5, 5), (7, 5), (5, 7), (7, 7)}
    c -= {(6, 6)}
    return c, w, h


def anneau():
    return ring_cells(10, 10, 7, 9.2, 20, 20), 20, 20


def zigzag():
    w, h = 36, 10
    c = set()
    x, y, d = 0, 7, -1
    while x < w:
        for _ in range(3):
            c |= {(x, y), (x, y + 1)}
            x += 1
            y += d
        d = -d
    return c, w, h


def croix():
    w = h = 9
    c = {(x, x) for x in range(9)} | {(8 - x, x) for x in range(9)}
    c |= {(x + 1, x) for x in range(8)} | {(7 - x, x) for x in range(8)}
    return c, w, h


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    grain("grain-clair", (11, 26, 58))                       # sur fonds clairs : carrés nuit
    grain("grain-sombre", (251, 248, 243), alphas=(10, 16, 26))   # sur fonds sombres : carrés crème
    for name, fn in (("engrenage", engrenage), ("tuyau", tuyau), ("etincelle", etincelle),
                     ("anneau", anneau), ("zigzag", zigzag), ("croix", croix)):
        cells, w, h = fn()
        for tone, col in (("", "#0B1A3A"), ("-clair", "#FBF8F3"), ("-or", "#FF8A3D"), ("-orange", "#FC4C02")):
            (OUT / f"{name}{tone}.svg").write_text(svg_from(cells, w, h, col, name), encoding="utf-8")
    print("✓ assets/img/deco/")


if __name__ == "__main__":
    main()
