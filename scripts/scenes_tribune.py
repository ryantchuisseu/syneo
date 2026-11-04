#!/usr/bin/env python3
"""Trois scènes d'intérieur en pixel art pour les cartes de « La tribune ».

  1. parcours  : le bureau de Syn, la nuit, avec vue sur Yaoundé
  2. expertise : Néo présente des graphiques, Syn lève la main
  3. reseau    : Syn et Néo se retrouvent dans un espace de rencontre

Usage : python3 scripts/scenes_tribune.py → assets/img/scenes/tribune-*.png
"""
import pathlib
import random
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import mascotte as M  # noqa: E402

OUT = ROOT / "assets" / "img" / "scenes"
W, H, FLOOR = 120, 80, 56


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


C = {k: hx(v) for k, v in dict(
    ink="#0B1A3A", wall="#1B2F60", wall_l="#22397107", wall2="#1F3567", base="#132650",
    floor="#11234B", floor_l="#172C5B", floor_d="#0C1A3A",
    wood="#B07A4E", wood_l="#CC9566", wood_d="#7E5236",
    grey="#8C98B3", grey_l="#C9D1E2", white="#F4F7FC", screen="#7CC4FF", screen_d="#3E86D6",
    night="#0A1530", sky="#16285A", city="#24407E", star="#F4F7FC", moon="#FFE8B0",
    blue="#02449B", blue_l="#2E6FD3", orange="#FC4C02", orange_l="#FF8A3D",
    gold="#F2B233", gold_l="#FFD66E", ciel="#DCEBFF", peche="#FFD9C4",
    leaf="#4F8A5B", leaf_l="#7DB36F", leaf_d="#356146", pot="#C4583A", pot_d="#8E3D2A",
).items() if len(v) == 7}
C["wall_l"] = hx("#223A71")


class Room:
    def __init__(self, wall=None, floor=None):
        self.px = [[(0, 0, 0)] * W for _ in range(H)]
        wall = wall or C["wall"]
        for y in range(H):
            for x in range(W):
                if y < FLOOR:
                    c = wall if (x // 6) % 2 else C["wall2"]          # papier peint à rayures discrètes
                else:
                    c = C["floor"] if ((y - FLOOR) // 4) % 2 == 0 else C["floor_l"]
                    if (x + (y - FLOOR) // 4 * 9) % 26 == 0:
                        c = C["floor_d"]                               # joints de parquet
                self.px[y][x] = c
        for x in range(W):                                             # plinthe
            self.px[FLOOR - 1][x] = C["base"]
            self.px[FLOOR][x] = C["ink"]

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def box(self, x0, y0, x1, y1, fill, light=None, dark=None):
        """Rectangle cerné d'un contour foncé, reflet en haut, ombre à droite."""
        self.rect(x0, y0, x1, y1, C["ink"])
        self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)
        if light:
            self.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 1, light)
        if dark:
            self.rect(x1 - 1, y0 + 2, x1 - 1, y1 - 1, dark)

    def glow(self, cx, cy, rx, ry, color, k=.35):
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d < 1 and 0 <= x < W and 0 <= y < H:
                    a = k * (1 - d)
                    o = self.px[y][x]
                    self.px[y][x] = tuple(round(o[i] + (color[i] - o[i]) * a) for i in range(3))

    def sprite(self, spr, x, feet_y):
        oy = feet_y - spr.h
        for (sx, sy), c in spr.px.items():
            self.put(x + sx, oy + sy, hx(c))

    def shadow(self, x0, x1, y):
        for x in range(x0, x1 + 1):
            for yy in (y, y + 1):
                o = self.px[yy][x]
                self.px[yy][x] = tuple(round(v * .7) for v in o)

    def save(self, name):
        im = Image.new("RGB", (W, H))
        im.putdata([c for row in self.px for c in row])
        OUT.mkdir(parents=True, exist_ok=True)
        im.resize((W * 4, H * 4), Image.NEAREST).save(OUT / f"tribune-{name}.png", optimize=True)
        print(f"✓ assets/img/scenes/tribune-{name}.png")


# --- Mobilier ----------------------------------------------------------------
def plant(r, x, base, h=14, big=False):
    r.box(x, base - 6, x + 8, base, C["pot"], C["orange_l"], C["pot_d"])
    stems = [(-4, h), (-1, h + 3), (2, h + 1), (5, h - 2), (8, h - 4)] if big else [(0, h - 4), (3, h), (6, h - 3)]
    for dx, hh in stems:
        for i in range(hh - 6):
            xx = x + 4 + int(dx * i / hh)
            r.put(xx, base - 7 - i, C["leaf_d"])
        tx, ty = x + 4 + dx, base - hh - 1
        for lx, ly, c in ((0, 0, C["leaf_l"]), (-1, 1, C["leaf"]), (1, 1, C["leaf"]), (0, 1, C["leaf"]),
                          (-2, 2, C["leaf_d"]), (2, 2, C["leaf_d"]), (0, 2, C["leaf_l"]), (-1, 2, C["leaf"]), (1, 2, C["leaf"])):
            r.put(tx + lx, ty + ly, c)


def window(r, x0, y0, x1, y1, rnd):
    r.box(x0, y0, x1, y1, C["grey_l"])
    r.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, C["night"])
    for y in range(y0 + 2, y1 - 1):                                     # ciel en dégradé
        if y > (y0 + y1) / 2:
            r.rect(x0 + 2, y, x1 - 2, y, C["sky"])
    for _ in range(9):
        r.put(rnd.randint(x0 + 3, x1 - 3), rnd.randint(y0 + 3, (y0 + y1) // 2), C["star"])
    r.rect(x1 - 9, y0 + 4, x1 - 6, y0 + 7, C["moon"]); r.put(x1 - 9, y0 + 4, C["night"])
    # silhouette de Yaoundé : collines, antenne, immeubles éclairés
    for x in range(x0 + 2, x1 - 1):
        h = 3 + int(2 * abs(((x - x0) % 14) - 7) / 7)
        r.rect(x, y1 - 2 - h, x, y1 - 2, C["city"])
    ax = x0 + (x1 - x0) // 3
    r.rect(ax, y1 - 13, ax, y1 - 5, C["city"]); r.put(ax, y1 - 14, C["orange"])
    for bx, bh in ((x0 + 16, 8), (x0 + 19, 11), (x0 + 23, 7)):
        if bx + 2 < x1 - 2:
            r.rect(bx, y1 - 2 - bh, bx + 2, y1 - 2, C["city"])
            r.put(bx + 1, y1 - bh, C["gold_l"])
    r.rect((x0 + x1) // 2, y0 + 1, (x0 + x1) // 2, y1 - 1, C["grey_l"])   # croisillon
    r.rect(x0 + 1, (y0 + y1) // 2, x1 - 1, (y0 + y1) // 2, C["grey_l"])
    r.rect(x0 - 1, y1 + 1, x1 + 1, y1 + 2, C["grey"])                     # rebord


def books(r, x, shelf_y, n, rnd):
    cols = [C["orange"], C["blue_l"], C["gold"], C["ciel"], C["orange_l"], C["white"]]
    for i in range(n):
        h = rnd.randint(5, 8)
        c = cols[i % len(cols)]
        r.rect(x, shelf_y - h, x + 1, shelf_y - 1, c)
        r.put(x, shelf_y - h, C["ink"]); r.put(x + 1, shelf_y - h, C["ink"])
        r.rect(x + 2, shelf_y - h, x + 2, shelf_y - 1, C["ink"])
        x += 3


def string_lights(r, x0, x1, y, sag):
    cols = [C["gold_l"], C["orange_l"], C["ciel"], C["gold_l"], C["orange"]]
    pts = []
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        yy = y + int(sag * 4 * t * (1 - t))
        r.put(x, yy, C["ink"])
        pts.append((x, yy))
    for k, (x, yy) in enumerate(pts[3::8]):
        c = cols[k % len(cols)]
        r.rect(x, yy + 1, x + 1, yy + 2, c)
        r.glow(x + .5, yy + 2, 5, 4, c, .22)


# --- Scènes ------------------------------------------------------------------
def scene_parcours():
    rnd = random.Random(4)
    r = Room()
    window(r, 7, 7, 43, 37, rnd)
    # étagère + livres + petite plante
    r.box(52, 18, 92, 20, C["wood"], C["wood_l"], C["wood_d"])
    books(r, 54, 18, 7, rnd)
    plant(r, 80, 17, 9)
    r.box(60, 28, 70, 38, C["gold"], C["gold_l"])                       # cadre au mur
    r.rect(62, 30, 68, 36, C["blue"]); r.rect(64, 33, 66, 36, C["orange"])
    # tapis
    for x in range(14, 76):
        for y in (70, 71, 72, 73, 74):
            if abs(x - 45) <= 30 - (abs(y - 72) * 3):
                r.put(x, y, C["orange"] if (y % 2) else C["peche"])
    # bureau
    r.box(56, 43, 114, 46, C["wood"], C["wood_l"], C["wood_d"])
    r.box(58, 47, 61, 66, C["wood_d"]); r.box(109, 47, 112, 66, C["wood_d"])
    r.box(92, 47, 108, 56, C["wood"], C["wood_l"], C["wood_d"]); r.rect(99, 51, 101, 51, C["gold"])
    r.shadow(56, 114, 67)
    # ordinateur portable allumé
    r.box(70, 32, 88, 42, C["grey"]); r.rect(72, 34, 86, 40, C["screen"])
    for yy, w in ((35, 10), (37, 7), (39, 12)):
        r.rect(73, yy, 73 + w, yy, C["screen_d"])
    r.rect(68, 42, 90, 43, C["grey_l"])
    r.glow(79, 40, 18, 12, C["screen"], .18)
    # lampe de bureau
    r.box(100, 41, 106, 43, C["ink"])
    r.rect(103, 33, 103, 40, C["ink"]); r.box(98, 29, 108, 34, C["gold"], C["gold_l"])
    r.glow(103, 44, 16, 10, C["gold_l"], .3)
    r.box(92, 38, 96, 43, C["white"]); r.put(97, 40, C["white"])           # tasse
    plant(r, 4, 70, 20, big=True)
    # Syn a une idée, devant son bureau
    spr, _ = M.pose_idee(M.SYN, "Syn"); r.sprite(spr, 30, 74)
    r.save("parcours")


def scene_expertise():
    rnd = random.Random(8)
    r = Room(wall=hx("#1E3466"))
    # écran de présentation avec graphiques
    r.box(28, 6, 100, 42, C["grey"])
    r.rect(30, 8, 98, 40, C["white"])
    for i, (h, c) in enumerate(((10, C["blue_l"]), (16, C["blue"]), (13, C["blue_l"]), (22, C["orange"]), (19, C["blue"]))):
        r.rect(35 + i * 7, 36 - h, 39 + i * 7, 36, c)
    r.rect(33, 37, 70, 37, C["ink"])
    for i in range(14):                                                 # courbe qui monte
        r.put(76 + i * 1, 30 - int((i / 13) ** 1.6 * 16), C["orange"])
        r.put(76 + i * 1, 31 - int((i / 13) ** 1.6 * 16), C["orange"])
    r.rect(76, 33, 94, 33, C["grey"])
    for k, c in enumerate((C["gold"], C["blue_l"], C["orange"])):
        r.rect(78 + k * 6, 11, 81 + k * 6, 13, c)
    r.rect(33, 11, 52, 12, C["ink"]); r.rect(33, 15, 46, 15, C["grey"])
    r.rect(62, 42, 66, 55, C["ink"])                                     # pied de l'écran
    r.glow(64, 26, 46, 26, C["white"], .12)
    # post-it au mur
    for (x, y, c) in ((8, 12, C["gold_l"]), (15, 10, C["orange_l"]), (9, 20, C["ciel"]), (16, 19, C["gold_l"]), (12, 28, C["orange_l"])):
        r.rect(x, y, x + 5, y + 5, c); r.rect(x + 1, y + 2, x + 4, y + 2, C["grey"])
    # tabouret et plante
    r.box(98, 60, 110, 62, C["wood"], C["wood_l"], C["wood_d"]); r.rect(100, 63, 101, 72, C["wood_d"]); r.rect(107, 63, 108, 72, C["wood_d"])
    plant(r, 108, 56, 18, big=True)
    spr, _ = M.pose_micro(M.NEO, "Néo"); r.sprite(spr, 6, 76)
    spr2, _ = M.pose_salut(M.SYN, "Syn"); r.sprite(spr2, 76, 76)
    r.shadow(10, 26, 76); r.shadow(82, 96, 76)
    r.save("expertise")


def scene_reseau():
    rnd = random.Random(12)
    r = Room(wall=hx("#1A2D5C"))
    string_lights(r, 0, W - 1, 4, 7)
    # affiche SYNEO au mur
    r.box(10, 16, 36, 44, C["white"])
    r.rect(12, 18, 34, 30, C["blue"])
    for k, (h, c) in enumerate(((3, C["blue_l"]), (5, C["blue_l"]), (7, C["orange_l"]), (9, C["orange"]))):
        r.rect(15 + k * 5, 28 - h, 18 + k * 5, 28, c)
    r.rect(13, 33, 30, 34, C["blue"]); r.rect(13, 37, 24, 37, C["grey"]); r.rect(13, 40, 27, 40, C["grey"])
    # tableau d'annonces
    r.box(82, 16, 112, 40, C["wood_l"], None, C["wood_d"])
    for (x, y, w, h, c) in ((85, 19, 8, 7, C["white"]), (95, 18, 7, 9, C["gold_l"]), (104, 20, 6, 6, C["ciel"]), (86, 29, 10, 8, C["orange_l"]), (99, 30, 9, 7, C["white"])):
        r.rect(x, y, x + w, y + h, c); r.put(x + w // 2, y, C["orange"])
    # mange-debout avec cafés et téléphone
    r.box(74, 50, 104, 53, C["wood"], C["wood_l"], C["wood_d"])
    r.rect(88, 54, 90, 70, C["wood_d"]); r.box(82, 70, 96, 72, C["wood_d"])
    for mx in (78, 96):
        r.box(mx, 45, mx + 4, 50, C["white"]); r.put(mx + 5, 47, C["white"])
        r.rect(mx + 1, 43, mx + 1, 43, C["grey_l"]); r.rect(mx + 3, 42, mx + 3, 42, C["grey_l"])
    r.box(86, 48, 92, 50, C["ink"]); r.rect(87, 49, 91, 49, C["screen"])
    # Syn et Néo main dans la main, avec une bulle
    spr, _ = M.duo_main_dans_la_main(); r.sprite(spr, 22, 76)
    r.box(50, 30, 66, 40, C["white"])
    r.put(54, 41, C["ink"]); r.put(55, 41, C["white"]); r.put(54, 42, C["ink"])
    for k, c in enumerate((C["blue"], C["orange"], C["gold"])):
        r.rect(53 + k * 4, 34, 54 + k * 4, 35, c)
    plant(r, 108, 72, 16, big=True)
    r.shadow(24, 64, 76)
    r.save("reseau")


if __name__ == "__main__":
    scene_parcours()
    scene_expertise()
    scene_reseau()
