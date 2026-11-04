#!/usr/bin/env python3
"""Illustration pixel art animée du haut de l'accueil SYNEO.

Scène : la nuit sur Yaoundé, les 4 personnages du logo (du petit bleu au grand orange)
se tiennent la main sur la courbe du logo ; un grand ruban doré en S s'enroule autour d'eux.

Couches (212×200 px, agrandies ×3 sans flou) :
  hp-fond.png   ciel tramé, lune, étoiles, Yaoundé, partie arrière du ruban
  hp-groupe.png planche de 4 images : respiration, salut, clignement, écharpes au vent
  hp-avant.png  courbe du logo et partie avant du ruban

Usage : python3 scripts/hero_pixel.py
"""
import math
import pathlib
import random

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "hero-pixel"
W, H, S = 212, 200, 3
CX, CY, CR = 112, 101, 90           # grand cercle


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


INK = hx("#0A1633")
SKY = [hx(c) for c in ("#0F2250", "#14295C", "#1A3268", "#213C75", "#2A4783")]
CITY, CITY_L, HILL = hx("#0F2049"), hx("#16295A"), hx("#122650")
WIN, WIN2, RED = hx("#FFD66E"), hx("#FFB35C"), hx("#FC4C02")
MOON, MOON_D = hx("#FFF1C9"), hx("#E8D19A")
STAR = hx("#FBF8F3")
G = dict(d=hx("#A8700F"), b=hx("#E9A42A"), l=hx("#FFCC55"), s=hx("#FFF0B8"))   # ruban doré
SHOE, SHOE_L = hx("#1B1F2E"), hx("#3A4258")
EYE = hx("#FBF8F3")

# du petit bleu au grand orange (comme le logo) : vêtement, ombre, reflet, pantalon, écharpe
PEOPLE = [
    dict(c=hx("#1559C9"), d=hx("#0D3E92"), l=hx("#4C8BEA"), p=hx("#0B2F6E"), sc=hx("#FC6A1A"), scd=hx("#C9500C")),
    dict(c=hx("#2368D6"), d=hx("#164CA3"), l=hx("#5E9AF0"), p=hx("#123A80"), sc=hx("#FF8A3D"), scd=hx("#D2611E")),
    dict(c=hx("#FF7424"), d=hx("#CC5410"), l=hx("#FFA265"), p=hx("#9A3A08"), sc=hx("#2E6FD3"), scd=hx("#1B4FA6")),
    dict(c=hx("#FC4C02"), d=hx("#BE3900"), l=hx("#FF7D44"), p=hx("#7E2700"), sc=hx("#0B4DB3"), scd=hx("#083A8A")),
]


class Layer:
    def __init__(self):
        self.px = {}

    def put(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < W and 0 <= y < H:
            self.px[(x, y)] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.put(x, y, c)

    def disc(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r:
                    self.put(x, y, c)

    def outline(self, color=INK):
        add = {(x + dx, y + dy) for (x, y) in self.px for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if (x + dx, y + dy) not in self.px}
        for p in add:
            self.put(*p, color)
        return self

    def onto(self, other):
        other.px.update(self.px)
        return other

    def image(self):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            im.putpixel((x, y), c)
        return im


def in_circle(x, y, pad=0):
    return (x + .5 - CX) ** 2 + (y + .5 - CY) ** 2 <= (CR - pad) ** 2


def bayer(x, y):
    m = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
    return (m[y % 4][x % 4] + .5) / 16


# ---------------------------------------------------------------------------
# Courbes
def bez(p0, p1, p2, p3, n=500):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def ribbon(curves, w=6.2):
    """Ruban en relief, lumière venant d'en haut à gauche : 4 nuances + éclats."""
    L = Layer()
    pts = [p for cv in curves for p in bez(*cv)]
    for x, y in pts:
        L.disc(x, y, w, G["b"])
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        tx, ty = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n, tx / n
        if nx * -1 + ny * -1 < 0:                       # normale orientée vers la lumière (haut-gauche)
            nx, ny = -nx, -ny
        for k in (w - 1.2, w - .4):
            L.put(x - nx * k, y - ny * k, G["d"])
        L.put(x - nx * (w - 2.2), y - ny * (w - 2.2), G["d"] if i % 3 else G["b"])
        L.put(x + nx * (w - 1.6), y + ny * (w - 1.6), G["l"])
        L.put(x + nx * (w - 2.6), y + ny * (w - 2.6), G["l"])
        if (i // 14) % 4 == 0:                          # éclats brillants, en tirets
            L.put(x + nx * (w - 2.1), y + ny * (w - 2.1), G["s"])
    return L


def logo_curve(x):
    x0, cx, x1 = 14, 96, 200
    y0, cy, y1 = 168, 198, 144
    a, b, c = x0 - 2 * cx + x1, 2 * (cx - x0), x0 - x
    t = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    return (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1


def grad(x):
    t = max(0, min(1, (x - 14) / 186))
    stops = [(0, (13, 79, 190)), (.45, (84, 84, 178)), (.7, (196, 82, 98)), (1, (252, 76, 2))]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            k = (t - a) / (b - a)
            return tuple(round(ca[i] + (cb[i] - ca[i]) * k) for i in range(3))
    return stops[-1][1]


def shade(c, k):
    return tuple(max(0, min(255, round(v * k))) for v in c[:3]) + (255,)


# ---------------------------------------------------------------------------
def fond():
    L = Layer()
    rnd = random.Random(11)
    # ciel en bandes tramées (Bayer), plus clair vers l'horizon
    for y in range(H):
        for x in range(W):
            if not in_circle(x, y):
                continue
            t = (y - (CY - CR)) / (2 * CR) * (len(SKY) - 1)
            i = min(len(SKY) - 2, int(t))
            L.put(x, y, SKY[i + 1] if (t - i) > bayer(x, y) else SKY[i])
    # bord du cercle tramé
    for y in range(H):
        for x in range(W):
            d = math.hypot(x + .5 - CX, y + .5 - CY)
            if CR < d < CR + 3 and bayer(x, y) < (CR + 3 - d) / 3 * .6:
                L.put(x, y, SKY[0])
    # lune en croissant, avec halo tramé
    mx, my = 52, 46
    for y in range(my - 22, my + 23):
        for x in range(mx - 22, mx + 23):
            d = math.hypot(x + .5 - mx, y + .5 - my)
            if 12 < d < 20 and bayer(x, y) < (20 - d) / 8 * .35 and in_circle(x, y):
                L.put(x, y, SKY[3])
    L.disc(mx, my, 11, MOON)
    L.disc(mx + 5, my - 4, 10, SKY[1])
    for (x, y) in ((mx - 6, my + 2), (mx - 4, my + 6), (mx - 8, my - 2)):
        L.put(x, y, MOON_D)
    # étoiles : points et petites croix
    for _ in range(46):
        x, y = rnd.randint(CX - CR + 6, CX + CR - 6), rnd.randint(CY - CR + 6, CY + 30)
        if in_circle(x, y, 4) and math.hypot(x - mx, y - my) > 16:
            L.put(x, y, STAR if rnd.random() < .6 else SKY[4])
    for x, y in ((150, 30), (84, 22), (176, 70), (30, 92)):
        if in_circle(x, y, 4):
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                L.put(x + dx, y + dy, STAR)
    # Yaoundé : collines lointaines, antenne du mont Fébé, immeubles éclairés
    for x in range(W):
        h = 0
        for c, hh, r in ((40, 22, 34), (88, 30, 30), (140, 18, 36), (190, 24, 30)):
            h = max(h, hh * max(0, 1 - ((x - c) / r) ** 2))
        top = int(170 - 12 - h + 1.5 * math.sin(x * .4))
        for y in range(top, H):
            if in_circle(x, y):
                L.put(x, y, HILL if y > top else CITY_L)
    ax, base = 88, 170 - 12 - 30
    for y in range(base - 20, base + 1):
        L.put(ax, y, CITY_L)
        if y > base - 8:
            L.put(ax - 1, y, CITY_L); L.put(ax + 1, y, CITY_L)
    L.put(ax, base - 21, RED)
    x = 104
    while x < 168:
        bw, bh = rnd.randint(4, 8), rnd.randint(8, 22)
        b = 170 - 4
        for yy in range(b - bh, b + 1):
            for xx in range(x, x + bw):
                if in_circle(xx, yy):
                    L.put(xx, yy, CITY)
        for yy in range(b - bh + 2, b - 1, 3):
            for xx in range(x + 1, x + bw - 1, 2):
                if rnd.random() < .45 and in_circle(xx, yy):
                    L.put(xx, yy, WIN if rnd.random() < .7 else WIN2)
        x += bw + rnd.randint(0, 2)
    # sol devant la ville
    for y in range(166, H):
        for x in range(W):
            if in_circle(x, y):
                L.put(x, y, CITY if bayer(x, y) < (y - 166) / 22 else HILL)
    # partie arrière du ruban
    ribbon([((178, 19), (146, -5), (87, 5), (93, 43)), ((93, 43), (97, 75), (162, 72), (164, 107))]).outline().onto(L)
    return L


def avant():
    L = Layer()
    for x in range(14, 201):                              # courbe du logo : 9 px, reflet en haut, ombre en bas
        y = logo_curve(x)
        c = grad(x)
        for dy in range(-4, 5):
            k = 1.28 if dy == -4 else 1.14 if dy == -3 else .72 if dy >= 3 else 1
            L.put(x, y + dy, shade(c + (255,), k))
        if x % 9 < 3:
            L.put(x, y - 3, shade(c + (255,), 1.45))
    L.outline()
    ribbon([((164, 107), (201, 115), (201, 163), (170, 176)), ((170, 176), (148, 184), (130, 181), (122, 199))]).outline().onto(L)
    return L


# ---------------------------------------------------------------------------
def personnage(cx, feet, h, P, f, idx):
    """Un personnage du logo en pixel art. f = image 0..3."""
    L = Layer()
    bob = 1 if (f + idx) % 2 else 0
    r = max(4, round(h * .13))
    top = feet - h + bob
    hy = top + r
    tw = max(9, round(h * .36)) | 1
    neck = hy + r
    hip = feet - round(h * .40)
    lw = max(3, round(h * .12))
    x0 = cx - tw // 2
    # jambes (pantalon) + chaussures, toujours posées
    for lx, c in ((cx - lw, P["p"]), (cx + 1, shade(P["p"], .8))):
        L.rect(lx, hip, lx + lw - 1, feet - 2, c)
        L.rect(lx, feet - 1, lx + lw, feet, SHOE)
        L.put(lx, feet - 1, SHOE_L)
    # buste arrondi
    for y in range(neck + 1, hip + 1):
        k = y - (neck + 1)
        ins = 2 if k == 0 else 1 if k == 1 or y == hip else 0                 # épaules arrondies
        if hip - y in (3, 4, 5):
            ins = max(ins, 1)                                                     # taille légèrement affinée
        for x in range(x0 + ins, x0 + tw - ins):
            c = P["c"]
            if x >= x0 + tw - 3:
                c = P["d"]
            elif x <= x0 + 1 and y < hip - 2:
                c = P["l"]
            L.put(x, y, c)
    L.rect(x0 + 1, hip - 1, x0 + tw - 2, hip - 1, P["d"])           # ceinture
    # tête
    L.disc(cx + .5, hy + .5, r, P["c"])
    for y in range(hy - r, hy + r + 1):
        for x in range(cx, cx + r + 2):
            if (x + .5 - cx - .5) ** 2 + (y + .5 - hy - .5) ** 2 <= r * r and (x - cx) > r * .45:
                L.put(x, y, P["d"])
    L.put(cx - r + 2, hy - r + 2, P["l"]); L.put(cx - r + 3, hy - r + 2, P["l"]); L.put(cx - r + 2, hy - r + 3, P["l"])
    # yeux (regardent vers la droite, clignement sur l'image 3)
    ey = hy - 1
    for ex in (cx - 2, cx + 2):
        if f == 3 and idx in (1, 3):
            L.rect(ex, ey + 1, ex + 1, ey + 1, INK)
        else:
            L.rect(ex, ey, ex + 1, ey + 1, EYE)
            L.put(ex + 1, ey, INK); L.put(ex + 1, ey + 1, INK)
    # écharpe aux couleurs de l'autre, pan qui flotte
    L.rect(x0 + 1, neck, x0 + tw - 2, neck + 1, P["sc"])
    L.rect(x0 + 1, neck + 1, x0 + tw - 2, neck + 1, P["scd"])
    flap = [(x0 + 1, neck + 2), (x0, neck + 3), (x0 - 1, neck + 3 + (f % 2))]
    for x, y in flap:
        L.put(x, y, P["sc"])
    # épaules (pour les bras)
    return L, (x0 - 1, neck + 3), (x0 + tw, neck + 3), lw


def bras(L, p, q, c, t=2):
    (x0, y0), (x1, y1) = p, q
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        k = i / n
        L.rect(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, x0 + (x1 - x0) * k + t - 1, y0 + (y1 - y0) * k + t - 1, c)


def groupe(f):
    xs, hs = [30, 64, 102, 142], [46, 60, 74, 90]
    out = Layer()
    bodies, sh = [], []
    for i, (x, h) in enumerate(zip(xs, hs)):
        feet = round(logo_curve(x)) - 5
        L, ls, rs, lw = personnage(x, feet, h, PEOPLE[i], f, i)
        bodies.append(L); sh.append((ls, rs))
    # bras : mains jointes entre voisins (dessinées dans le calque du personnage le plus grand)
    for i in range(3):
        a, b = sh[i][1], sh[i + 1][0]
        mx, my = (a[0] + b[0]) // 2, max(a[1], b[1]) + 12
        bras(bodies[i], a, (mx, my), PEOPLE[i]["c"], 3)
        bras(bodies[i + 1], b, (mx + 1, my), PEOPLE[i + 1]["c"], 3)
        bodies[i + 1].disc(mx + 1.5, my + 1.5, 2.2, PEOPLE[i + 1]["l"])
    # le plus petit salue (3 positions)
    sx, sy = sh[0][0]
    hand = [(sx - 6, sy - 9), (sx - 8, sy - 7), (sx - 5, sy - 11), (sx - 8, sy - 7)][f]
    bras(bodies[0], (sx, sy), (sx - 3, sy - 4), PEOPLE[0]["c"], 3)
    bras(bodies[0], (sx - 3, sy - 4), hand, PEOPLE[0]["c"], 3)
    bodies[0].disc(hand[0] + 1, hand[1], 2, PEOPLE[0]["l"])
    # bras extérieur du plus grand, main sur la hanche
    ox, oy = sh[3][1]
    bras(bodies[3], (ox, oy), (ox + 4, oy + 9), PEOPLE[3]["c"], 3)
    bras(bodies[3], (ox + 4, oy + 9), (ox + 1, oy + 16), PEOPLE[3]["d"], 3)
    # ombres portées tramées sur la courbe
    for x, h in zip(xs, hs):
        y = round(logo_curve(x)) - 4
        for dx in range(-h // 5, h // 5 + 1):
            if (dx + y) % 2 == 0:
                out.put(x + dx, y, shade(grad(x + dx) + (255,), .6))
    for L in bodies:                                       # du plus petit au plus grand, contour pour chacun
        L.outline().onto(out)
    return out.image()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    big = lambda im: im.resize((W * S, H * S), Image.NEAREST)
    big(fond().image()).save(OUT / "hp-fond.png", optimize=True)
    big(avant().image()).save(OUT / "hp-avant.png", optimize=True)
    sheet = Image.new("RGBA", (W * S * 4, H * S), (0, 0, 0, 0))
    for f in range(4):
        sheet.paste(big(groupe(f)), (f * W * S, 0))
    sheet.save(OUT / "hp-groupe.png", optimize=True)
    print(f"✓ assets/img/hero-pixel/ ({W}×{H} px, ×{S})")


if __name__ == "__main__":
    main()
