#!/usr/bin/env python3
"""Vignettes pixel expressives (personnages en action) pour l'accueil.

Usage : python3 scripts/vignettes.py → assets/img/vignettes/*.png (72×48 px, ×4, fond transparent)

  escalier    Néo, une marche plus haut, tend la main à Syn qui monte (accompagnement)
  randonnee   Syn et Néo, sacs au dos et bâtons, montent vers le drapeau au sommet (le parcours PRISME)
  poignee     Néo serre la main d'un partenaire, Syn tient le dossier (partenariats)
  conference  Néo au pupitre sous le projecteur, le public de dos (conférence inaugurale)
  etudier     Syn révise au bureau, piles de livres, l'idée s'allume (conférences thématiques)
  atelier     Syn code, Néo le guide devant un tableau de post-it et une fusée (formation & incubation)
  tournage    Syn filme Néo qui salue, clap au sol (série Les Bâtisseurs)
  forum       Trois personnages échangent sous une banderole (Forum National)
"""
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import mascotte as M  # noqa: E402

OUT = ROOT / "assets" / "img" / "vignettes"
W, H, SC = 72, 48, 4
SYN, NEO = M.SYN, M.NEO
PART = dict(main="#7FA6D6", light="#AFC6E8", dark="#4F79B8", acc="#FC4C02", acc_l="#FF8A3D")
C = dict(ink="#0B1A3A", ciel="#DCEBFF", ciel2="#AFC6E8", ciel3="#7FA6D6", creme="#FBF8F3", grey="#8C98B3", grey_l="#C9D1E2",
         wood="#B07A4E", wood_l="#CC9566", wood_d="#7E5236", orange="#FC4C02", orange_l="#FF8A3D", peche="#FFC29A",
         blue="#02449B", blue_l="#2E6FD3", screen="#7CC4FF", white="#FFFFFF", leaf="#4F8A5B", leaf_l="#7DB36F")


def line(s, a, b, c, t=2):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        s.rect(x, y, x + t - 1, y + t - 1, c)


def char(s, pal, ox, oy, look=1, arms="none", legs="stand"):
    """Personnage de la famille Syn/Néo, bras et jambes réglables."""
    M.body(s, pal, ox=ox, oy=oy, arms=arms)
    M.eyes(s, ox=ox, oy=oy, look=look)
    if legs == "walk":                                        # une jambe en avant
        for y in range(oy + 20, oy + 23):
            for x in (ox + 13, ox + 14):
                s.px.pop((x, y), None); s.solid.discard((x, y))
        line(s, (ox + 13, oy + 20), (ox + 16, oy + 21), pal["main"])
    if legs == "step":                                        # genou levé (marche d'escalier)
        for y in range(oy + 20, oy + 23):
            for x in (ox + 13, ox + 14):
                s.px.pop((x, y), None); s.solid.discard((x, y))
        s.rect(ox + 13, oy + 19, ox + 16, oy + 20, pal["main"])
        s.rect(ox + 15, oy + 20, ox + 16, oy + 21, pal["main"])
    return (ox + 7, oy + 14), (ox + 15, oy + 14)             # épaules gauche / droite


def done(s, name, pals):
    M.finish(s, pals)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for (x, y), c in s.px.items():
        c = c.lstrip("#")
        im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    OUT.mkdir(parents=True, exist_ok=True)
    im.resize((W * SC, H * SC), Image.NEAREST).save(OUT / f"{name}.png", optimize=True)
    print("✓", name)


# ---------------------------------------------------------------------------
def escalier():
    s = M.Sprite(W, H)
    for i in range(4):                                        # 4 marches qui montent vers la droite
        x0, top = 4 + 16 * i, 44 - 8 * i
        s.rect(x0, top, W - 1, H - 1, C["ciel2"])
        s.rect(x0, top, W - 1, top, C["white"])
        s.rect(x0, top + 1, W - 1, top + 1, C["ciel"])
    line(s, (66, 4), (66, 19), C["ink"], 1)                   # drapeau en haut
    s.rect(67, 4, 71, 7, C["orange"])
    # Syn sur la 1re marche monte (genou levé), Néo sur la 2e lui tend la main
    _, sr = char(s, SYN, 6, 21, look=1, arms="none", legs="step")
    nl, _ = char(s, NEO, 26, 5, look=-1, arms="none")
    line(s, (6 + 7, 21 + 14), (6 + 7, 21 + 18), SYN["main"])  # bras libre de Syn
    line(s, (nl[0] + 8, nl[1]), (nl[0] + 8, nl[1] + 4), NEO["main"])
    line(s, nl, (28, 28), NEO["main"])
    line(s, sr, (27, 29), SYN["main"])
    s.rect(27, 28, 28, 29, NEO["light"])
    done(s, "escalier", [SYN, NEO])


def randonnee():
    s = M.Sprite(W, H)
    peak = (58, 9)
    for x in range(W):                                        # montagne : face éclairée / face ombrée
        top = round(47 - (47 - peak[1]) * x / peak[0]) if x <= peak[0] else round(peak[1] + (x - peak[0]) * 1.6)
        for y in range(max(0, top), H):
            s.put(x, y, C["ciel2"] if x <= peak[0] else C["ciel3"], solid=False)
        s.put(x, top, C["white"], solid=False)
    for k in range(6, 56, 5):                                 # sentier en pointillés
        y = round(47 - 38 * k / 58) + 3
        s.put(k, y, C["creme"], solid=False); s.put(k + 1, y, C["creme"], solid=False)
    line(s, (peak[0], peak[1] - 8), (peak[0], peak[1]), C["ink"], 1)
    s.rect(peak[0] + 1, peak[1] - 8, peak[0] + 5, peak[1] - 5, C["orange"])
    for (pal, ox, oy, bag) in ((SYN, 4, 15, C["orange"]), (NEO, 22, 5, C["blue"])):
        _, r = char(s, pal, ox, oy, look=1, arms="none", legs="walk")
        s.rect(ox + 5, oy + 13, ox + 8, oy + 19, bag)         # sac à dos
        s.rect(ox + 5, oy + 13, ox + 8, oy + 13, C["ink"])
        line(s, r, (ox + 18, oy + 16), pal["main"])           # bras vers le bâton
        line(s, (ox + 19, oy + 12), (ox + 21, oy + 23), C["wood_d"], 1)
    done(s, "randonnee", [SYN, NEO])


def poignee():
    s = M.Sprite(W, H)
    s.rect(0, 44, W - 1, H - 1, C["ciel"])                    # sol
    s.rect(0, 44, W - 1, 44, C["white"])
    # Syn derrière, tient le dossier
    char(s, SYN, 2, 22, look=1, arms="right_hold")
    s.rect(19, 30, 24, 37, C["creme"]); s.rect(20, 32, 23, 32, C["grey"]); s.rect(20, 34, 22, 34, C["grey"])
    # Néo et le partenaire se serrent la main
    _, nr = char(s, NEO, 20, 21, look=1, arms="none")
    pl, _ = char(s, PART, 42, 21, look=-1, arms="none")
    line(s, (20 + 7, 21 + 14), (20 + 7, 21 + 18), NEO["main"])
    line(s, (42 + 15, 21 + 14), (42 + 15, 21 + 18), PART["main"])
    line(s, nr, (40, 37), NEO["main"])
    line(s, pl, (41, 37), PART["main"])
    s.rect(39, 36, 42, 38, NEO["light"])
    # bulle avec un cœur
    s.rect(52, 6, 66, 16, C["white"]); s.put(54, 17, C["white"]); s.put(54, 18, C["white"])
    for x, y in ((57, 9), (58, 9), (61, 9), (62, 9), (56, 10), (59, 10), (60, 10), (63, 10), (57, 11), (62, 11), (58, 12), (61, 12), (59, 13), (60, 13),
                 (57, 10), (58, 10), (61, 10), (62, 10), (58, 11), (59, 11), (60, 11), (61, 11), (59, 12), (60, 12)):
        s.put(x, y, C["orange"])
    done(s, "poignee", [SYN, NEO, PART])


def conference():
    s = M.Sprite(W, H)
    for y in range(0, 34):                                    # faisceau du projecteur (non cerné)
        half = 3 + y // 2
        for x in range(36 - half, 36 + half):
            if (x + y) % 2 == 0:
                s.put(x, y, C["peche"], solid=False)
    s.rect(14, 33, 58, 37, C["wood"]); s.rect(14, 33, 58, 33, C["wood_l"]); s.rect(14, 37, 58, 37, C["wood_d"])   # scène
    char(s, NEO, 24, 9, look=1, arms="mic")
    s.rect(41, 16, 43, 18, C["grey"]); s.put(41, 16, C["grey_l"]); s.put(42, 19, C["ink"])
    s.rect(30, 23, 42, 32, C["blue"]); s.rect(30, 23, 42, 24, C["blue_l"])                                     # pupitre
    s.rect(34, 27, 38, 29, C["orange"])
    for i, (x, col) in enumerate(((6, SYN), (18, NEO), (30, PART), (42, SYN), (54, NEO))):                     # public de dos
        s.disc(x + 4.5, 43 + (i % 2), 4.2, col["main"])
        s.rect(x, 46, x + 9, 47, col["main"])
    done(s, "conference", [SYN, NEO, PART])


def etudier():
    s = M.Sprite(W, H)
    s.rect(46, 4, 66, 22, C["white"]); s.rect(48, 7, 60, 7, C["blue"]); s.rect(48, 10, 64, 10, C["grey_l"])     # tableau
    s.rect(48, 13, 58, 13, C["grey_l"]); s.rect(48, 16, 62, 16, C["orange_l"]); s.rect(55, 22, 57, 26, C["grey"])
    char(s, SYN, 10, 12, look=1, arms="right_hold")
    s.disc(22, 5, 3, M.GOLD); s.put(21, 4, M.GOLD_L); s.rect(21, 9, 23, 9, C["grey"])                           # l'idée
    for x, y in ((16, 3), (28, 3), (15, 7), (29, 7)):
        s.put(x, y, M.GOLD, solid=False)
    s.rect(2, 31, 50, 34, C["wood"]); s.rect(2, 31, 50, 31, C["wood_l"])                                        # bureau
    s.rect(5, 35, 7, 47, C["wood_d"]); s.rect(45, 35, 47, 47, C["wood_d"])
    s.rect(24, 27, 34, 30, C["white"]); s.rect(29, 27, 29, 30, C["grey"])                                      # livre ouvert
    for i, col in enumerate((C["orange"], C["blue_l"], C["peche"], C["blue"])):                                 # pile de livres
        s.rect(37 - (i % 2), 27 - i * 3, 46 - (i % 2), 29 - i * 3, col)
    done(s, "etudier", [SYN])


def atelier():
    s = M.Sprite(W, H)
    s.rect(4, 3, 40, 22, C["creme"])                                                                             # tableau de post-it
    for x, y, col in ((7, 6, C["peche"]), (14, 5, C["ciel2"]), (21, 7, C["orange_l"]), (8, 14, C["ciel2"]), (15, 14, C["peche"])):
        s.rect(x, y, x + 5, y + 5, col)
    for x, y in ((31, 6), (31, 7), (30, 8), (31, 8), (32, 8), (30, 9), (31, 9), (32, 9), (30, 10), (31, 10), (32, 10), (29, 11), (33, 11)):
        s.put(x, y, C["orange"])                                                                                # fusée
    s.put(31, 12, C["peche"]); s.put(31, 13, C["orange_l"])
    char(s, NEO, 44, 25, look=-1, arms="left_up")                                                               # Néo montre l'écran
    char(s, SYN, 8, 18, look=1, arms="right_hold")
    s.rect(2, 36, 40, 38, C["wood"]); s.rect(2, 36, 40, 36, C["wood_l"]); s.rect(4, 39, 6, 47, C["wood_d"]); s.rect(36, 39, 38, 47, C["wood_d"])
    s.rect(24, 26, 36, 34, C["grey"]); s.rect(26, 28, 34, 32, C["screen"]); s.rect(22, 35, 38, 35, C["ink"])   # ordinateur
    s.rect(27, 29, 31, 29, C["blue"]); s.rect(27, 31, 33, 31, C["blue"])
    done(s, "atelier", [SYN, NEO])


def tournage():
    s = M.Sprite(W, H)
    s.rect(0, 44, W - 1, H - 1, C["ciel"]); s.rect(0, 44, W - 1, 44, C["white"])
    char(s, SYN, 0, 21, look=1, arms="right_hold")
    s.rect(18, 26, 28, 32, C["grey"]); s.rect(18, 26, 28, 26, C["grey_l"])                                     # caméra
    s.rect(29, 27, 32, 31, C["ink"]); s.rect(30, 28, 31, 30, C["screen"])
    s.rect(19, 23, 22, 25, C["grey"]); s.put(26, 27, C["orange"])                                              # voyant REC
    line(s, (23, 33), (19, 43), C["ink"], 1); line(s, (23, 33), (27, 43), C["ink"], 1); line(s, (23, 33), (23, 43), C["ink"], 1)
    char(s, NEO, 44, 21, look=-1, arms="right_up")
    s.rect(60, 38, 70, 43, C["ink"])                                                                           # clap au sol
    for x in range(60, 71, 3):
        s.rect(x, 36, x + 1, 37, C["white"])
    s.rect(60, 37, 70, 37, C["ink"])
    done(s, "tournage", [SYN, NEO])


def forum():
    s = M.Sprite(W, H)
    s.rect(4, 2, 68, 9, C["orange"]); s.rect(4, 2, 68, 2, C["orange_l"])                                       # banderole
    for k, x in enumerate(range(10, 64, 9)):
        s.rect(x, 5, x + 4, 6, C["white"] if k % 2 else C["blue"])
    line(s, (4, 9), (4, 44), C["ink"], 1); line(s, (68, 9), (68, 44), C["ink"], 1)
    s.rect(0, 44, W - 1, H - 1, C["ciel"]); s.rect(0, 44, W - 1, 44, C["white"])
    char(s, SYN, 2, 21, look=1, arms="right_up")
    char(s, PART, 24, 21, look=1, arms="right_hold")
    char(s, NEO, 46, 21, look=-1, arms="left_up")
    for bx, by, col in ((6, 12, C["blue"]), (30, 12, C["orange"])):                                            # bulles
        s.rect(bx, by, bx + 10, by + 6, C["white"])
        for k in range(3):
            s.rect(bx + 2 + k * 3, by + 3, bx + 2 + k * 3, by + 3, col)
    done(s, "forum", [SYN, NEO, PART])


if __name__ == "__main__":
    for f in (escalier, randonnee, poignee, conference, etudier, atelier, tournage, forum):
        f()
