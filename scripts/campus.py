#!/usr/bin/env python3
"""Façades de campus en pixel art pour la carte « La route PRISME ».

Usage : python3 scripts/campus.py → assets/img/campus/*.png (96×64, agrandies ×4)
Les bâtiments sont des évocations stylisées, pas des reproductions fidèles.
"""
import pathlib
import random

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "campus"
W, H, GROUND = 96, 64, 52


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


C = {k: hx(v) for k, v in dict(
    ink="#0B1A3A", sky1="#BFD6F2", sky2="#DCE8F6", sky3="#FBE6D4", dusk1="#2B3F7A", dusk2="#6B5C8E", dusk3="#F2A36B",
    grass="#6F9A5C", grass_l="#93B978", road="#B9AFA3", road_l="#D6CDC1", earth="#B5654A",
    white="#F4F1EA", white_d="#D8D2C6", cream="#EADBC0", cream_d="#CDB892", grey="#A9B2C4", grey_d="#7D879C",
    glass="#7FA6D6", glass_l="#B7D0EE", glass_n="#FFD66E",
    blue="#02449B", blue_l="#2E6FD3", orange="#FC4C02", orange_l="#FF8A3D", gold="#F2B233", red="#C4583A",
    leaf="#4F8A5B", leaf_l="#7DB36F", leaf_d="#356146", trunk="#7B5A43",
).items()}


class Pic:
    def __init__(self, night=False):
        self.night = night
        self.px = [[(0, 0, 0)] * W for _ in range(H)]
        s1, s2, s3 = (C["dusk1"], C["dusk2"], C["dusk3"]) if night else (C["sky1"], C["sky2"], C["sky3"])
        for y in range(H):
            for x in range(W):
                t = y / GROUND
                c = s1 if t < .4 else s2 if t < .75 else s3
                if t >= 1:
                    c = C["grass"] if y < GROUND + 3 else C["road"]
                    if y == GROUND:
                        c = C["grass_l"]
                    if y >= GROUND + 3 and (x // 6 + y) % 7 == 0:
                        c = C["road_l"]
                self.px[y][x] = c
        rnd = random.Random(1)
        if night:
            for _ in range(12):
                self.put(rnd.randint(0, W - 1), rnd.randint(0, 18), C["white"])

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def box(self, x0, y0, x1, y1, fill, shade=None):
        self.rect(x0, y0, x1, y1, C["ink"])
        self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)
        if shade:
            self.rect(x1 - 2, y0 + 1, x1 - 1, y1 - 1, shade)

    def windows(self, x0, y0, x1, y1, w=3, h=3, gx=2, gy=3):
        y = y0
        while y + h <= y1:
            x = x0
            while x + w <= x1:
                lit = self.night and (x * 7 + y * 3) % 5 < 3
                self.rect(x, y, x + w - 1, y + h - 1, C["glass_n"] if lit else C["glass"])
                if not self.night:
                    self.put(x, y, C["glass_l"])
                x += w + gx
            y += h + gy

    def palm(self, x, h=16):
        for i in range(h):
            self.put(x + (i * i) // 90, GROUND - i, C["trunk"])
        tx, ty = x + (h * h) // 90, GROUND - h
        for dx, dy in ((-6, 2), (-5, 1), (-4, 0), (-3, -1), (-2, -1), (-1, -1), (0, -2), (1, -1), (2, -1), (3, -1), (4, 0), (5, 1), (6, 2),
                       (-6, 3), (6, 3), (-3, 0), (3, 0), (-1, 0), (1, 0), (0, -1), (-4, 1), (4, 1)):
            self.put(tx + dx, ty + dy, C["leaf_l"] if dy < 0 else C["leaf"])

    def tree(self, x, r=6):
        self.rect(x, GROUND - 5, x + 1, GROUND, C["trunk"])
        for y in range(-r, r + 1):
            for xx in range(-r, r + 1):
                if xx * xx + y * y <= r * r:
                    c = C["leaf_l"] if y < -r / 3 and xx > -r / 3 else C["leaf"] if y < r / 3 else C["leaf_d"]
                    self.put(x + xx, GROUND - 5 - r + y, c)

    def flag(self, x, y, color):
        self.rect(x, y, x, y + 10, C["ink"])
        self.rect(x + 1, y, x + 6, y + 3, color)

    def banner(self, x0, y, x1):
        """Banderole PRISME : bleu, orange, or."""
        self.rect(x0, y, x1, y + 2, C["blue"])
        third = (x1 - x0) // 3
        self.rect(x0 + third, y, x0 + 2 * third, y + 2, C["orange"])
        self.rect(x0 + 2 * third, y, x1, y + 2, C["gold"])

    def save(self, name):
        im = Image.new("RGB", (W, H))
        im.putdata([c for row in self.px for c in row])
        OUT.mkdir(parents=True, exist_ok=True)
        im.resize((W * 4, H * 4), Image.NEAREST).save(OUT / f"{name}.png", optimize=True)
        print("✓", f"assets/img/campus/{name}.png")


def portique(p, x0, x1, top, base_color, shade):
    """Façade à colonnes (grande école)."""
    p.box(x0, top + 6, x1, GROUND, base_color, shade)
    for x in range(x0 + 1, x1 + 1):                                  # fronton triangulaire
        h = 6 - abs(x - (x0 + x1) // 2) * 6 // ((x1 - x0) // 2)
        p.rect(x, top + 6 - h, x, top + 6, base_color)
        p.put(x, top + 6 - h - 1, C["ink"])
    for cx in range(x0 + 4, x1 - 2, 6):                              # colonnes
        p.rect(cx, top + 10, cx + 1, GROUND - 1, C["white"])
        p.rect(cx + 2, top + 10, cx + 2, GROUND - 1, C["white_d"])
    p.rect(x0 + 1, top + 8, x1 - 1, top + 9, C["white_d"])
    p.rect((x0 + x1) // 2 - 3, GROUND - 8, (x0 + x1) // 2 + 3, GROUND - 1, C["ink"])


def enspy(night=False, name="enspy"):
    p = Pic(night)
    p.box(10, 20, 86, GROUND, C["cream"], C["cream_d"])
    p.windows(13, 23, 32, GROUND - 3); p.windows(64, 23, 84, GROUND - 3)
    portique(p, 34, 62, 14, C["white"], C["white_d"])
    p.banner(36, 22, 60)
    p.flag(46, 3, C["red"])
    p.palm(4, 18); p.palm(90, 15)
    if name == "inaugurale":
        rnd = random.Random(5)
        for _ in range(26):
            p.put(rnd.randint(4, 92), rnd.randint(2, 30), (C["orange"], C["gold"], C["blue_l"], C["white"])[rnd.randint(0, 3)])
    p.save(name)


def uy1():
    p = Pic()
    p.box(6, 24, 52, GROUND, C["white"], C["white_d"])
    p.windows(9, 27, 50, GROUND - 3, 4, 3, 2, 3)
    p.box(50, 14, 76, GROUND, C["cream"], C["cream_d"])
    p.windows(53, 17, 73, GROUND - 3, 3, 4, 2, 3)
    p.box(74, 28, 92, GROUND, C["white"], C["white_d"]); p.windows(77, 31, 90, GROUND - 3)
    p.banner(52, 20, 74)
    p.tree(16, 6); p.tree(40, 5); p.palm(86, 14)
    p.save("uy1")


def supptic():
    p = Pic()
    p.box(14, 26, 82, GROUND, C["white"], C["white_d"])
    p.windows(17, 29, 80, GROUND - 3, 5, 3, 2, 3)
    p.box(56, 8, 68, 27, C["grey"], C["grey_d"])                       # tour télécom
    p.rect(61, 1, 62, 8, C["ink"])
    for y in (3, 6):
        p.rect(58, y, 65, y, C["ink"])
    p.put(61, 0, C["orange"])
    p.rect(30, 22, 52, 25, C["blue"]); p.rect(32, 23, 50, 23, C["white"])
    p.tree(8, 6); p.palm(88, 16)
    p.save("supptic")


def iai():
    p = Pic()
    p.box(8, 22, 88, GROUND, C["cream"], C["cream_d"])
    for x in range(9, 88):                                             # coupole centrale
        d = abs(x - 48)
        if d <= 12:
            h = int((144 - d * d) ** .5)
            p.rect(x, 22 - h, x, 22, C["blue_l"] if x < 46 else C["blue"])
            p.put(x, 21 - h, C["ink"])
    p.windows(12, 26, 40, GROUND - 3); p.windows(56, 26, 86, GROUND - 3)
    p.rect(42, 30, 54, GROUND - 1, C["glass"]); p.rect(42, 30, 54, 30, C["ink"])
    p.banner(14, 24, 36)
    p.palm(3, 17); p.tree(92, 5)
    p.save("iai")


def esstic():
    p = Pic()
    p.box(10, 18, 50, GROUND, C["white"], C["white_d"])
    p.windows(13, 21, 48, GROUND - 3, 3, 3, 2, 3)
    p.box(48, 28, 88, GROUND, C["cream"], C["cream_d"])
    p.rect(52, 32, 84, 44, C["ink"]); p.rect(53, 33, 83, 43, C["glass"])   # écran géant (communication)
    for x, h in ((56, 4), (60, 7), (64, 5), (68, 9), (72, 6)):
        p.rect(x, 43 - h, x + 2, 42, C["orange"] if x == 68 else C["white"])
    p.rect(26, 10, 27, 18, C["ink"]); p.rect(22, 9, 31, 10, C["ink"])        # antenne
    p.tree(6, 5); p.palm(91, 14)
    p.save("esstic")


def numiatech():
    p = Pic(night=True)
    p.box(20, 12, 46, GROUND, C["glass"], C["blue"])
    p.windows(23, 15, 44, GROUND - 3, 3, 2, 2, 2)
    p.box(44, 24, 80, GROUND, C["white"], C["white_d"])
    p.windows(47, 27, 78, GROUND - 3, 4, 3, 2, 3)
    p.banner(46, 30, 78)
    p.rect(52, GROUND - 7, 58, GROUND - 1, C["glass_n"])
    p.palm(10, 17); p.palm(88, 15)
    p.save("numiatech")


if __name__ == "__main__":
    enspy(name="inaugurale")
    enspy()
    uy1()
    supptic()
    iai()
    esstic()
    numiatech()
