#!/usr/bin/env python3
"""Illustration pixel art animée pour le haut de l'accueil (composition « bloc sombre + ruban en S »).

Couches (160×150 px, agrandies ×4 sans flou) :
  hp-fond.png      : grand cercle, étoiles, ruban doré (partie arrière)
  hp-groupe.png    : planche de 4 images des 4 personnages du logo (respiration + salut)
  hp-avant.png     : courbe du logo + ruban doré (partie avant)

Usage : python3 scripts/hero_pixel.py
"""
import math
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "hero-pixel"
W, H, S = 160, 150, 4


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


INK = hx("#0B1A3A")
GOLD, GOLD_L, GOLD_D = hx("#F2B233"), hx("#FFD66E"), hx("#C98E1B")
PEOPLE = [  # (principal, ombre, reflet), du petit bleu au grand orange, comme le logo
    (hx("#0B4DB3"), hx("#083A8A"), hx("#3C7BDB")),
    (hx("#1C5CC8"), hx("#12459C"), hx("#5590E6")),
    (hx("#FC6A1A"), hx("#C9500C"), hx("#FF9A5C")),
    (hx("#FC4C02"), hx("#B73800"), hx("#FF7A3D")),
]
WHITE = hx("#FBF8F3")


class Layer:
    def __init__(self):
        self.px = {}

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[(int(x), int(y))] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.put(x, y, c)

    def disc(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r:
                    self.put(x, y, c)

    def outline(self, keep=()):
        add = [(x + dx, y + dy) for (x, y) in list(self.px) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if (x + dx, y + dy) not in self.px]
        for p in add:
            self.px[p] = INK

    def image(self):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            if 0 <= x < W and 0 <= y < H:
                im.putpixel((x, y), c)
        return im


def bez(p0, p1, p2, p3, n=400):
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        yield (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])


def ribbon(layer, curves, w=4.6):
    """Ruban épais : bord sombre, cœur doré, reflet clair d'un côté."""
    pts = [p for cv in curves for p in bez(*cv)]
    for x, y in pts:
        layer.disc(x, y, w, GOLD)
    for i, (x, y) in enumerate(pts[:-1]):
        nx, ny = pts[i + 1][0] - x, pts[i + 1][1] - y
        L = math.hypot(nx, ny) or 1
        px, py = -ny / L, nx / L
        layer.put(round(x + px * (w - 1.6)), round(y + py * (w - 1.6)), GOLD_L)
        layer.put(round(x - px * (w - 1.2)), round(y - py * (w - 1.2)), GOLD_D)


def logo_curve(x):
    """Courbe du logo qui porte le groupe (quadratique)."""
    x0, cx, x1 = 10, 72, 150
    y0, cy, y1 = 126, 150, 108
    a, b, c = x0 - 2 * cx + x1, 2 * (cx - x0), x0 - x
    t = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    return (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1


def curve_color(x):
    t = (x - 10) / 140
    stops = [(0, (11, 77, 179)), (.5, (90, 79, 168)), (1, (252, 76, 2))]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            k = (t - a) / (b - a)
            return tuple(round(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)) + (255,)
    return stops[-1][1] + (255,)


# ---------------------------------------------------------------------------
def fond():
    L = Layer()
    for y in range(H):                                    # grand cercle tramé sur le bord
        for x in range(W):
            d = math.hypot(x + .5 - 84, y + .5 - 76)
            if d < 66 or (d < 69 and (x + y) % 2 == 0):
                L.put(x, y, hx("#14305F"))
    for x, y in ((14, 22), (122, 8), (150, 52), (6, 86), (148, 96), (34, 140)):
        L.put(x, y, WHITE)
    # partie arrière du S
    rib = Layer()
    ribbon(rib, [((134, 14), (110, -4), (66, 4), (70, 32)), ((70, 32), (73, 56), (122, 54), (124, 80))])
    rib.outline()
    L.px.update(rib.px)
    return L


def avant():
    L = Layer()
    for x in range(10, 151):                              # courbe du logo, épaisse de 7 px
        y = logo_curve(x)
        for dy in range(-3, 4):
            L.put(x, round(y + dy), curve_color(x))
        L.put(x, round(y - 3), tuple(min(255, v + 40) for v in curve_color(x)[:3]) + (255,))
    rib = Layer()                                         # le S repasse devant, sur le côté
    ribbon(rib, [((124, 80), (152, 86), (152, 122), (128, 132)), ((128, 132), (112, 138), (98, 136), (92, 148))])
    L.px.update(rib.px)
    L.outline()
    return L


def personne(L, cx, feet, h, pal, bob, arm):
    """Personnage façon logo : tête ronde, buste arrondi, jambes ; ombre à droite, reflet à gauche."""
    col, dark, light = pal
    feet -= bob
    r = max(3, round(h * .12))
    hy = feet - h + r
    tw = max(6, round(h * .32))
    tt, tb = hy + r + 1, feet - round(h * .42)
    lw = max(2, round(h * .11))
    x0 = cx - tw // 2
    # jambes (pieds posés : seul le buste bouge)
    for lx, c in ((cx - lw - 1 + 0, col), (cx + 1, dark)):
        L.rect(lx, tb, lx + lw - 1, feet + bob, c)
    # buste
    for y in range(tt, tb + 1):
        inset = 1 if y in (tt, tb) else 0
        for x in range(x0 + inset, x0 + tw - inset):
            c = col
            if x >= x0 + tw - 2 - inset:
                c = dark
            elif x == x0 + 1 + inset and y < tb - 2:
                c = light
            L.put(x, y, c)
    # tête
    L.disc(cx + .5, hy, r, col)
    for y in range(int(hy - r), int(hy + r) + 1):
        for x in range(cx + 1, cx + r + 1):
            if (x + .5 - cx - .5) ** 2 + (y + .5 - hy) ** 2 <= r * r and x >= cx + r - 1:
                L.put(x, y, dark)
    L.put(cx - r // 2, hy - r // 2, light)
    L.put(cx - r // 2 + 1, hy - r // 2, light)
    # bras levé du plus petit (salut) : deux positions
    if arm is not None:
        sx, sy = x0 - 1, tt + 1
        pts = [(sx, sy), (sx - 2, sy - 2), (sx - 3, sy - 4), (sx - 3 - arm, sy - 6), (sx - 3 - arm, sy - 7)]
        for x, y in pts:
            L.rect(x, y, x + 1, y + 1, col)
    return (x0 - 1, tt + 2), (x0 + tw, tt + 2)


def groupe(frame):
    L = Layer()
    xs, hs = [24, 49, 76, 104], [30, 39, 48, 57]
    shoulders = []
    for i, (x, h) in enumerate(zip(xs, hs)):
        bob = 1 if (frame + i) % 2 else 0                  # respiration en décalé
        arm = (frame % 2) * 2 if i == 0 else None          # le petit agite la main
        feet = round(logo_curve(x)) - 4
        shoulders.append(personne(L, x, feet, h, PEOPLE[i], bob, arm))
    # mains jointes entre voisins
    for i in range(3):
        (ax, ay), (bx, by) = shoulders[i][1], shoulders[i + 1][0]
        mx, my = (ax + bx) // 2, max(ay, by) + 9
        for t in range(0, 11):
            k = t / 10
            L.rect(round(ax + (mx - ax) * k), round(ay + (my - ay) * k), round(ax + (mx - ax) * k) + 1, round(ay + (my - ay) * k) + 1, PEOPLE[i][0])
            L.rect(round(bx + (mx - bx) * k), round(by + (my - by) * k), round(bx + (mx - bx) * k) + 1, round(by + (my - by) * k) + 1, PEOPLE[i + 1][0])
        L.disc(mx + .5, my + .5, 1.8, PEOPLE[i + 1][0])
    # bras extérieur du grand
    ox, oy = shoulders[3][1]
    for k in range(9):
        L.rect(ox + (1 if k > 3 else 0), oy + k * 2, ox + 1 + (1 if k > 3 else 0), oy + k * 2 + 1, PEOPLE[3][0])
    L.outline()
    return L.image()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    big = lambda im: im.resize((W * S, H * S), Image.NEAREST)
    big(fond().image()).save(OUT / "hp-fond.png", optimize=True)
    big(avant().image()).save(OUT / "hp-avant.png", optimize=True)
    sheet = Image.new("RGBA", (W * S * 4, H * S), (0, 0, 0, 0))
    for f in range(4):
        sheet.paste(big(groupe(f)), (f * W * S, 0))
    sheet.save(OUT / "hp-groupe.png", optimize=True)
    print("✓ assets/img/hero-pixel/ : hp-fond, hp-groupe (4 images), hp-avant")


if __name__ == "__main__":
    main()
