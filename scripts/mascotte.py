#!/usr/bin/env python3
"""Génère les mascottes pixel art SYNEO (Syn & Néo) en SVG.

Usage : python3 scripts/mascotte.py   → écrit assets/img/mascotte/*.svg

Les personnages sont dessinés sur une petite grille, puis un contour
foncé est ajouté automatiquement autour de chaque forme (style 8-bit).
"""
import html
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img" / "mascotte"

INK = "#0B1A3A"     # contour
WHITE = "#FFFFFF"
GOLD, GOLD_L, GOLD_D = "#F2B233", "#FFD66E", "#B97F0E"
GREY, GREY_L = "#8C98B3", "#C9D1E2"

# Palettes tirées du logo SYNEO
SYN = dict(main="#02449B", light="#2E6FD3", dark="#012F6D", acc="#FC5A0A", acc_l="#FF8A3D")
NEO = dict(main="#FC4C02", light="#FF8A3D", dark="#C13A00", acc="#02449B", acc_l="#2E6FD3")


class Sprite:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = {}          # (x, y) -> couleur
        self.solid = set()    # pixels qui reçoivent un contour
        self.edge = set()     # pixels du contour

    def put(self, x, y, c, solid=True):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[(x, y)] = c
            if solid:
                self.solid.add((x, y))

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def limb(self, pts, c):
        for x, y in pts:
            self.rect(x, y, x + 1, y + 1, c)

    def disc(self, cx, cy, r, c):
        for y in range(self.h):
            for x in range(self.w):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r:
                    self.put(x, y, c)

    def outline(self):
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.px:
                    continue
                if any((x + dx, y + dy) in self.solid for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for p in add:
            self.px[p] = INK
        self.edge = set(add)

    def shade(self, pal):
        """Reflet à gauche, ombre à droite sur la couleur principale."""
        upd = {}
        for (x, y), c in self.px.items():
            if c != pal["main"]:
                continue
            out = lambda q: q not in self.px or q in self.edge
            if out((x - 1, y)) or out((x, y - 1)) and out((x - 1, y - 1)):
                upd[(x, y)] = pal["light"]
            elif out((x + 1, y)):
                upd[(x, y)] = pal["dark"]
        self.px.update(upd)

    def svg(self, title):
        rects = "".join(
            f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{c}"/>'
            for (x, y), c in sorted(self.px.items(), key=lambda i: (i[0][1], i[0][0]))
        )
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'shape-rendering="crispEdges" role="img" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title>{rects}</svg>\n')


def body(s, pal, ox=0, oy=0, tall=False, look=1, arms="down"):
    """Personnage de base : tête ronde, écharpe-courbe du logo, corps, jambes."""
    m = pal["main"]
    s.disc(ox + 12, oy + 7, 4.9, m)                       # tête
    by1 = oy + (21 if tall else 19)
    s.rect(ox + 9, oy + 13, ox + 14, by1, m)              # corps
    s.rect(ox + 9, by1 + 1, ox + 10, by1 + 3, m)          # jambe gauche
    s.rect(ox + 13, by1 + 1, ox + 14, by1 + 3, m)         # jambe droite
    # écharpe : la courbe du logo, qui flotte sur le côté
    s.rect(ox + 8, oy + 12, ox + 15, oy + 12, pal["acc"])
    s.rect(ox + 9, oy + 13, ox + 14, oy + 13, pal["acc_l"])
    for x, y in ((16, 12), (17, 13), (17, 14)):
        s.put(ox + x, oy + y, pal["acc"])
    # bras (2 pixels d'épaisseur)
    L = lambda pts: s.limb([(ox + x, oy + y) for x, y in pts], m)
    if arms in ("down", "right_up", "right_hold", "mic", "right_down"):
        L([(7, 14), (7, 16), (7, 17)])                        # bras gauche le long du corps
    if arms in ("down", "left_up"):
        L([(15, 14), (15, 16), (15, 17)])                     # bras droit le long du corps
    if arms == "right_up":                                    # salut de la main
        L([(15, 14), (16, 12), (17, 10), (18, 8)])
    if arms == "right_hold":                                  # bras plié vers l'avant
        L([(15, 14), (16, 15), (17, 15), (18, 14), (19, 13)])
    if arms == "mic":                                         # main près de la bouche
        L([(15, 14), (16, 12), (17, 10)])
    if arms == "left_up":
        L([(7, 14), (6, 12), (5, 10), (4, 8)])

def eyes(s, ox=0, oy=0, look=1):
    for ex in (9, 13):
        s.rect(ox + ex, oy + 6, ox + ex + 1, oy + 7, WHITE)
        px = ox + ex + (1 if look > 0 else 0)
        s.put(px, oy + 6, INK)
        s.put(px, oy + 7, INK)


def finish(s, pals, extra=None):
    s.outline()
    for p in pals:
        s.shade(p)
    if extra:
        extra(s)
    return s


# ----------------------------------------------------------------------------
# Poses
# ----------------------------------------------------------------------------
def pose_salut(pal, name):
    s = Sprite(24, 26)
    body(s, pal, arms="right_up")
    eyes(s, look=1)
    return finish(s, [pal]), f"{name} qui salue"


def pose_micro(pal, name):
    s = Sprite(26, 26)
    body(s, pal, arms="mic")
    eyes(s, look=1)
    s.rect(18, 7, 20, 9, GREY)       # tête du micro
    s.put(18, 7, GREY_L)
    s.put(19, 10, INK)               # manche
    return finish(s, [pal]), f"{name} au micro (conférences)"


def pose_idee(pal, name):
    s = Sprite(24, 30)
    body(s, pal, oy=5, arms="down")
    eyes(s, oy=5, look=-1)
    s.disc(12, 3.2, 2.6, GOLD)       # ampoule au-dessus de la tête
    s.put(11, 2, GOLD_L)
    s.rect(11, 6, 13, 6, GREY)
    def rays(sp):
        for x, y in ((7, 1), (17, 1), (6, 4), (18, 4)):
            sp.px[(x, y)] = GOLD
    return finish(s, [pal], rays), f"{name} a une idée (vulgarisation)"


def pose_prisme(pal, name):
    s = Sprite(32, 26)
    body(s, pal, arms="right_hold")
    eyes(s, look=1)
    # prisme doré tenu dans la main
    for row in range(5):
        s.rect(20 - row, 10 + row, 20 + row, 10 + row, GOLD)
    s.put(20, 10, GOLD_L); s.put(19, 11, GOLD_L)
    s.rect(17, 14, 23, 14, GOLD_D)
    def beams(sp):   # rayons bleu / orange qui sortent du prisme
        for i in range(6):
            sp.px[(25 + i, 11 + i // 2)] = SYN["main"]
            sp.px[(25 + i, 13 + i // 2)] = NEO["main"]
    return finish(s, [pal], beams), f"{name} et le prisme (PRISME)"


def pose_escalier(pal, name):
    s = Sprite(32, 34)
    # marches en pixels
    for i, (x0, y) in enumerate(((0, 31), (8, 27), (16, 23), (24, 19))):
        s.rect(x0, y, 31, 33, "#C9D1E2" if i % 2 else "#DCE2EE")
    body(s, pal, ox=8, oy=0, arms="right_up")
    eyes(s, ox=8, oy=0, look=1)
    return finish(s, [pal]), f"{name} monte les marches (entreprendre)"


def pose_laptop(pal, name):
    s = Sprite(26, 26)
    body(s, pal, arms="right_hold")
    eyes(s, look=1)
    s.rect(15, 15, 22, 19, GREY)     # écran
    s.rect(16, 16, 21, 18, "#7CC4FF")
    s.put(17, 17, WHITE); s.put(19, 17, WHITE)
    s.rect(14, 20, 23, 20, INK)      # clavier
    return finish(s, [pal]), f"{name} code (tech & IA)"


def duo_main_dans_la_main():
    """Hommage au logo : Syn (bleu, plus petit) tient la main de Néo (orange, plus grand)."""
    s = Sprite(44, 30)
    body(s, SYN, ox=0, oy=4, arms="right_down")
    eyes(s, ox=0, oy=4, look=1)
    body(s, NEO, ox=16, oy=0, tall=True, arms="left_down")
    eyes(s, ox=16, oy=0, look=-1)
    s.limb([(15, 18), (16, 19), (18, 20)], SYN["main"])          # bras de Syn vers Néo
    s.limb([(23, 14), (22, 16), (21, 18), (20, 20)], NEO["main"])  # bras de Néo vers Syn
    s.limb([(31, 14), (31, 16), (31, 17)], NEO["main"])          # autre bras de Néo
    return finish(s, [SYN, NEO]), "Syn et Néo main dans la main (networking, partenariats)"


def avatar():
    """Avatar carré : tête de Néo pour favicon, profil réseaux sociaux."""
    s = Sprite(16, 16)
    s.disc(8, 8.5, 6.4, NEO["main"])
    for ex in (5, 9):
        s.rect(ex, 6, ex + 1, 8, WHITE)
        s.put(ex + 1, 7, INK); s.put(ex + 1, 8, INK)
    s.rect(3, 14, 12, 14, SYN["main"])     # bout d'écharpe bleue
    return finish(s, [NEO, SYN]), "Avatar SYNEO"


def confettis():
    s = Sprite(40, 14)
    pts = [(1, 2, SYN["main"]), (6, 8, NEO["main"]), (11, 3, GOLD), (15, 10, SYN["light"]),
           (20, 1, NEO["light"]), (24, 7, SYN["main"]), (29, 11, GOLD), (33, 4, NEO["main"]), (37, 9, SYN["light"])]
    for x, y, c in pts:
        s.put(x, y, c, solid=False); s.put(x + 1, y, c, solid=False)
        s.put(x, y + 1, c, solid=False); s.put(x + 1, y + 1, c, solid=False)
    return s, "Confettis pixel"


def bouton():
    """Fond de bouton aux bords en escalier (texte ajouté en HTML par-dessus)."""
    s = Sprite(40, 10)
    for y in range(10):
        inset = (2, 1, 0, 0, 0, 0, 0, 0, 1, 2)[y]
        s.rect(inset, y, 39 - inset, y, NEO["main"])
    s.solid.clear()
    return s, "Bouton pixel"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = {
        "avatar": avatar(),
        "syn-salut": pose_salut(SYN, "Syn"),
        "neo-salut": pose_salut(NEO, "Néo"),
        "neo-micro": pose_micro(NEO, "Néo"),
        "syn-idee": pose_idee(SYN, "Syn"),
        "neo-prisme": pose_prisme(NEO, "Néo"),
        "syn-escalier": pose_escalier(SYN, "Syn"),
        "syn-laptop": pose_laptop(SYN, "Syn"),
        "duo-main-dans-la-main": duo_main_dans_la_main(),
        "confettis": confettis(),
        "bouton": bouton(),
    }
    for name, (sprite, title) in jobs.items():
        (OUT / f"{name}.svg").write_text(sprite.svg(title), encoding="utf-8")
        print(f"✓ {name}.svg  ({sprite.w}×{sprite.h})")


if __name__ == "__main__":
    main()
