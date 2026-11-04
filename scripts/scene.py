#!/usr/bin/env python3
"""Scène pixel art SYNEO : le lac municipal de Yaoundé au coucher du soleil.

Usage : python3 scripts/scene.py
→ assets/img/scenes/lac-yaounde.png (320×180) et lac-yaounde@4x.png (1280×720)

Tout est dessiné par code : ciel, nuages, collines, ville, arbres, eau,
reflets, ponton. Syn et Néo viennent de scripts/mascotte.py.
"""
import math
import pathlib
import random
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import mascotte  # noqa: E402

OUT = ROOT / "assets" / "img" / "scenes"
W, H = 360, 210
HORIZON = 182          # niveau de l'eau
rnd = random.Random(7)


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# Palette douce, accordée au bleu et à l'orange de SYNEO
P = {k: hx(v) for k, v in dict(
    sky_top="#BFD6F2", sky_mid="#DCE8F6", sky_low="#FBE6D4",
    sun="#FFD3A8", sun_l="#FFE8D2",
    cloud="#FCFAF6", cloud_s="#E6E9F2", cloud_ss="#D3DAE8",
    hill_far="#A9BCD9", hill_far_l="#BACBE3",
    hill_mid="#86A3A6", hill_mid_l="#9DB7B4", hill_mid_d="#6F8F95",
    city="#ECE6DC", city_s="#D3D6E0", window="#9FAFC8",
    antenna="#5D6B86", red="#FC4C02",
    ink="#2E2A3D",
    leaf_d="#3F6B4E", leaf="#5C8C5E", leaf_l="#86B07A", leaf_ll="#A9C98F",
    trunk="#7B5A43", trunk_d="#5A3F30",
    earth="#B5654A", earth_d="#8E4A38", grass="#6F9A5C", grass_l="#93B978",
    water="#8FB4CB", water_d="#739CB6", water_l="#BBD4E3", water_ll="#DCEAF2",
    wood="#A7764F", wood_d="#7A5238",
    flower="#FC6A1A", flower2="#F2B233",
).items()}


class Canvas:
    def __init__(self):
        self.px = [[(0, 0, 0)] * W for _ in range(H)]

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[y][x] = c

    def get(self, x, y):
        return self.px[y][x]

    def blit(self, layer, outline=True):
        if outline:
            layer.outline()
        for (x, y), c in layer.px.items():
            self.put(x, y, c)

    def image(self):
        im = Image.new("RGB", (W, H))
        im.putdata([c for row in self.px for c in row])
        return im


class Layer:
    """Un objet dessiné à part, puis cerné d'un contour foncé."""
    def __init__(self):
        self.px = {}

    def put(self, x, y, c):
        self.px[(int(x), int(y))] = c

    def disc(self, cx, cy, r, color_fn):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r:
                    self.put(x, y, color_fn(x, y))

    def outline(self, color=None):
        color = color or P["ink"]
        add = [(x + dx, y + dy) for (x, y) in self.px for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if (x + dx, y + dy) not in self.px]
        for p in add:
            self.px[p] = color


def dither(x, y, a, b, t):
    """Mélange en damier : t=0 → a, t=1 → b."""
    m = ((x + y) % 2) * 0.5 + ((x // 2 + y // 2) % 2) * 0.25
    return b if t > m + 0.125 else a


# ---------------------------------------------------------------------------
def sky(cv):
    bands = 9
    stops = [P["sky_top"], P["sky_mid"], P["sky_low"]]
    def grad(t):
        return mix(stops[0], stops[1], t / .6) if t < .6 else mix(stops[1], stops[2], (t - .6) / .4)
    for y in range(HORIZON):
        t = y / HORIZON
        b = int(t * bands)
        c = grad((b + .5) / bands)
        y_in = y - int(b * HORIZON / bands)
        for x in range(W):
            if y_in == 0 and b > 0 and (x + y) % 2 == 0:
                cv.put(x, y, grad((b - .5) / bands))
            else:
                cv.put(x, y, c)


def sun(cv, cx=244, cy=118):
    for y in range(cy - 26, cy + 26):
        for x in range(cx - 26, cx + 26):
            d = math.hypot(x + .5 - cx, y + .5 - cy)
            if d < 11:
                cv.put(x, y, P["sun"])
            elif d < 18 and (x + y) % 2 == 0:
                cv.put(x, y, P["sun_l"])
            elif d < 24 and (x % 2 == 0 and y % 2 == 0):
                cv.put(x, y, P["sun_l"])


def cloud(cv, cx, cy, s=1.0):
    blobs = [(-30, 6, 10), (-18, -2, 14), (-2, -10, 18), (16, -4, 15), (30, 2, 12), (42, 7, 8), (-40, 10, 6)]
    pts = set()
    flat = cy + 12 * s
    for dx, dy, r in blobs:
        r *= s
        X, Y = cx + dx * s, cy + dy * s
        for y in range(int(Y - r), int(Y + r) + 1):
            for x in range(int(X - r), int(X + r) + 1):
                if (x + .5 - X) ** 2 + (y + .5 - Y) ** 2 <= r * r and y <= flat:
                    pts.add((x, y))
    for (x, y) in pts:
        up = sum((x, y - k) in pts for k in range(1, 4))
        right = (x + 1, y) in pts and (x + 2, y) in pts
        if y > flat - 3 * s:
            c = P["cloud_ss"] if y > flat - 1.5 * s else P["cloud_s"]
        elif up < 2 and right:
            c = P["cloud"]
        elif not right:
            c = P["cloud_s"]
        else:
            c = P["cloud"]
        cv.put(x, y, c)


def hills(cv):
    # collines lointaines (les sept collines de Yaoundé)
    far = [(20, 22, 40), (90, 24, 34), (168, 36, 40), (250, 22, 40), (330, 20, 44)]
    for x in range(W):
        h = max((hh * max(0, 1 - ((x - c) / r) ** 2) for c, hh, r in far), default=0)
        h += 2 * math.sin(x * .3) + rnd.random()
        top = int(HORIZON - 12 - h)
        for y in range(top, HORIZON):
            cv.put(x, y, P["hill_far_l"] if y == top else P["hill_far"])
    # antenne du mont Fébé, sur la plus haute colline
    ax, base = 168, HORIZON - 12 - 36
    for i, y in enumerate(range(base - 16, base + 1)):
        w = 0 if i < 6 else 1
        for x in range(ax - w, ax + w + 1):
            cv.put(x, y, P["antenna"])
    cv.put(ax, base - 17, P["red"])
    # collines intermédiaires, plus vertes
    mid = [(0, 14, 56), (80, 10, 44), (196, 15, 52), (300, 13, 56)]
    tops = {}
    for x in range(W):
        h = max((hh * max(0, 1 - ((x - c) / r) ** 2) for c, hh, r in mid), default=0)
        h += 1.5 * math.sin(x * .21 + 1)
        top = int(HORIZON - 4 - h)
        tops[x] = top
        for y in range(top, HORIZON):
            c = P["hill_mid"]
            if y == top:
                c = P["hill_mid_l"]
            elif rnd.random() < .05 or (y - top < 3 and rnd.random() < .25):
                c = P["hill_mid_d"]          # petits arbres au loin
            cv.put(x, y, c)
    # ville sur la colline du centre
    x = 190
    while x < 232:
        bw, bh = rnd.randint(4, 7), rnd.randint(6, 15)
        base = tops[x + bw // 2] + 3
        for yy in range(base - bh, base):
            for xx in range(x, x + bw):
                c = P["city"] if xx < x + bw - 1 else P["city_s"]
                if (yy - (base - bh)) % 3 == 1 and (xx - x) % 2 == 1 and xx < x + bw - 1:
                    c = P["window"]
                cv.put(xx, yy, c)
        x += bw + rnd.randint(0, 2)


def ground(cv):
    """Deux berges de terre rouge couvertes d'herbe, de part et d'autre du lac."""
    banks = [(0, 150, HORIZON - 8), (232, W, HORIZON - 10)]
    for x0, x1, top in banks:
        L = Layer()
        for x in range(x0, x1):
            t = top + (1 if (x // 9) % 3 == 0 else 0)
            for y in range(t, HORIZON + 2):
                c = P["earth"] if y > t + 2 else P["grass"]
                if y == t:
                    c = P["grass_l"]
                if y > t + 2 and rnd.random() < .12:
                    c = P["earth_d"]
                L.put(x, y, c)
        cv.blit(L)
        # touffes d'herbe et fleurs
        for _ in range((x1 - x0) // 4):
            gx = rnd.randint(x0 + 1, x1 - 2)
            for k in range(rnd.randint(2, 4)):
                cv.put(gx + rnd.choice((-1, 0, 1)), top - 1 - k, P["grass"] if k else P["grass_l"])
        for _ in range((x1 - x0) // 14):
            fx = rnd.randint(x0 + 2, x1 - 3)
            cv.put(fx, top - 3, rnd.choice((P["flower"], P["flower2"])))
            cv.put(fx, top - 2, P["leaf"]); cv.put(fx, top - 1, P["leaf"])


def palm(cv, x, base, h, lean=1):
    L = Layer()
    pts = []
    for i in range(h):
        px_ = x + lean * int(9 * (i / h) ** 2)
        pts.append((px_, base - i))
        ring = i % 4 == 0
        L.put(px_, base - i, P["trunk_d"] if ring else P["trunk"])
        L.put(px_ + 1, base - i, P["trunk_d"])
        if i < 3:
            L.put(px_ - 1, base - i, P["trunk_d"])
    tx, ty = pts[-1]
    for ang in (-175, -150, -125, -100, -80, -55, -30, -5, 20, 160):
        a = math.radians(ang + rnd.uniform(-6, 6))
        ln = rnd.randint(16, 23)
        for i in range(ln):
            t = i / ln
            fx = tx + math.cos(a) * i
            fy = ty + math.sin(a) * i * (1 - t * .3) + 11 * t * t
            L.put(fx, fy, P["leaf_l"] if t < .5 else P["leaf"])
            if t < .8:
                L.put(fx, fy + 1, P["leaf"] if t < .5 else P["leaf_d"])
            if t > .15 and i % 2 == 0:
                side = 1 if math.cos(a) >= 0 else -1
                L.put(fx, fy + 2, P["leaf_d"])
                L.put(fx + side, fy + 3, P["leaf_d"])
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 1), (2, 1)):
        L.put(tx + dx, ty + dy, P["trunk_d"])
    cv.blit(L)


def round_tree(cv, x, base, r, trunk_h=10):
    """Manguier : couronne en grappes de feuillage, chaque grappe éclairée en haut à droite."""
    L = Layer()
    for y in range(base - trunk_h - 6, base + 1):
        L.put(x, y, P["trunk"]); L.put(x + 1, y, P["trunk_d"])
        if y > base - 3:
            L.put(x - 1, y, P["trunk_d"]); L.put(x + 2, y, P["trunk_d"])
    for i in range(4):                                   # deux branches
        L.put(x - 1 - i, base - trunk_h - 2 - i, P["trunk"])
        L.put(x + 2 + i, base - trunk_h - 3 - i, P["trunk"])
    cy = base - trunk_h - r + 3
    # grappes : d'abord le cœur, puis la périphérie, du bas vers le haut
    blobs = [(0, r * .15, r * .78)]
    n = 14
    for k in range(n):
        a = 2 * math.pi * k / n + rnd.uniform(-.2, .2)
        d = r * rnd.uniform(.62, .82)
        blobs.append((math.cos(a) * d, math.sin(a) * d * .82, r * rnd.uniform(.3, .42)))
    for _ in range(6):
        a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0, .5) * r
        blobs.append((math.cos(a) * d, math.sin(a) * d * .8, r * rnd.uniform(.28, .38)))
    blobs.sort(key=lambda b: (b[1], -b[0]), reverse=True)  # bas-gauche d'abord, haut-droite au-dessus
    tones = [P["leaf_d"], P["leaf"], P["leaf_l"], P["leaf_ll"]]
    for dx, dy, rr in blobs:
        bx, by = x + dx, cy + dy
        glob = (dx / r) * .35 - (dy / r) * .55          # position dans la couronne
        for yy in range(int(by - rr), int(by + rr) + 1):
            for xx in range(int(bx - rr), int(bx + rr) + 1):
                ux, uy = (xx + .5 - bx) / rr, (yy + .5 - by) / rr
                if ux * ux + uy * uy > 1:
                    continue
                loc = ux * .5 - uy * .7                  # relief de la grappe
                v = 1.3 + glob * 1.6 + loc * .9
                i = max(0, min(3, int(v)))
                if ux * ux + uy * uy > .72 and uy > .2:  # ombre portée sous chaque grappe
                    i = max(0, i - 1)
                L.put(xx, yy, tones[i])
    for _ in range(6):
        mx, my = x + rnd.randint(-r + 4, r - 4), cy + rnd.randint(0, r - 4)
        if (mx, my) in L.px and L.px[(mx, my)] in (P["leaf"], P["leaf_d"]):
            L.put(mx, my, P["flower2"])
    cv.blit(L)


def bush(cv, x, base, r):
    L = Layer()
    L.disc(x, base - r + 1, r, lambda px, py: dither(px, py, P["leaf"], P["leaf_d"], (py - (base - 2 * r)) / (2 * r)))
    for _ in range(2):
        L.put(x + rnd.randint(-r + 1, r - 1), base - r - rnd.randint(0, r - 1), P["flower"])
    cv.blit(L)


def water(cv):
    snap = [row[:] for row in cv.px]
    for y in range(HORIZON, H):
        depth = y - HORIZON
        for x in range(W):
            base = mix(P["water"], P["water_d"], min(1, depth / 34))
            src_y = HORIZON - 1 - depth
            k = .42 - depth * .012
            if src_y >= 0 and k > 0:
                c = mix(base, snap[src_y][x], k)
            else:
                c = base
            cv.put(x, y, c)
    # vaguelettes rares, horizontales
    for _ in range(70):
        x, y = rnd.randint(0, W - 8), rnd.randint(HORIZON + 2, H - 1)
        ln = rnd.randint(2, 6)
        c = P["water_l"] if rnd.random() < .75 else P["water_ll"]
        for i in range(ln):
            cv.put(x + i, y, c)
    for x in range(W):
        cv.put(x, HORIZON, P["water_ll"] if x % 5 else P["water_l"])
    # reflet du soleil, en tirets
    for y in range(HORIZON + 2, H, 2):
        w = max(1, 9 - (y - HORIZON) // 4)
        for x in range(214 - w, 214 + w):
            if (x // 2 + y) % 3:
                cv.put(x, y, P["sun_l"])


def dock(cv, x0=112, x1=176, y=146):
    L = Layer()
    for x in range(x0, x1):
        L.put(x, y, P["wood"]); L.put(x, y + 1, P["wood_d"] if x % 6 == 0 else P["wood"])
    for px_ in range(x0 + 4, x1, 14):                       # pilotis
        for yy in range(y + 2, y + 9):
            L.put(px_, yy, P["wood_d"]); L.put(px_ + 1, yy, P["wood"])
    cv.blit(L)


def birds(cv):
    for bx, by in ((28, 66), (36, 62), (44, 69), (322, 74)):
        for dx, dy in ((-2, -1), (-1, 0), (0, 1), (1, 0), (2, -1)):
            cv.put(bx + dx, by + dy, P["ink"])


def mascots(cv, x, feet_y):
    sprite, _ = mascotte.duo_main_dans_la_main()
    oy = feet_y - sprite.h
    for (sx, sy), c in sprite.px.items():
        cv.put(x + sx, oy + sy, hx(c))


def fern(cv, x, base):
    """Petite plante au premier plan."""
    for k, (dx, h) in enumerate(((-3, 4), (-1, 7), (1, 8), (3, 5), (5, 3))):
        for i in range(h):
            cv.put(x + dx + (i // 3) * (1 if dx > 0 else -1), base - i, P["leaf"] if i < h - 2 else P["leaf_l"])


def flower(cv, x, base, h=7, c=None):
    c = c or P["flower"]
    for i in range(h):
        cv.put(x, base - i, P["leaf_d"])
    cv.put(x + 1, base - 3, P["leaf"]); cv.put(x - 1, base - 4, P["leaf"])
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1), (0, 0)):
        cv.put(x + dx, base - h + dy, c if (dx, dy) != (0, 0) else P["flower2"])


def main():
    cv = Canvas()
    sky(cv)
    sun(cv, 214, 154)
    cloud(cv, 74, 112, 1.25)      # gros cumulus qui montent derrière les arbres
    cloud(cv, 292, 104, 1.1)
    cloud(cv, 186, 136, .7)
    cloud(cv, 40, 40, .55)
    cloud(cv, 250, 30, .45)
    hills(cv)
    birds(cv)
    lb, rb = HORIZON - 8, HORIZON - 10
    # massif gauche (arrière-plan puis premier plan)
    bush(cv, 112, lb, 6)
    palm(cv, 96, lb, 52, lean=1)
    round_tree(cv, 30, lb, 24, 16)
    palm(cv, 66, lb, 62, lean=-1)
    round_tree(cv, 128, lb, 13, 9)
    # massif droit
    palm(cv, 246, rb, 50, lean=-1)
    round_tree(cv, 292, rb, 22, 15)
    palm(cv, 338, rb, 66, lean=-1)
    round_tree(cv, 262, rb, 12, 8)
    ground(cv)
    for fx in (12, 48, 86, 140):
        fern(cv, fx, lb)
    for fx in (240, 280, 320, 352):
        fern(cv, fx, rb)
    flower(cv, 104, lb, 8); flower(cv, 22, lb, 6, P["flower2"]); flower(cv, 306, rb, 9)
    water(cv)
    dock(cv, 140, 206, HORIZON - 4)
    mascots(cv, 156, HORIZON - 4)
    OUT.mkdir(parents=True, exist_ok=True)
    im = cv.image()
    im.save(OUT / "lac-yaounde.png")
    im.resize((W * 4, H * 4), Image.NEAREST).save(OUT / "lac-yaounde@4x.png")
    print("✓ assets/img/scenes/lac-yaounde.png", im.size)


if __name__ == "__main__":
    main()
