#!/usr/bin/env python3
"""Bandeau « La ligne PRISME » : scène de fin de page aux couleurs SYNEO.

Le prisme doré reçoit la lumière et la sépare en deux cordes (bleue et orange)
qui courent au sol comme des lignes de métro ; leurs stations sont les
filières de PRISME. Syn et Néo attendent au départ, devant Yaoundé.

Usage : python3 scripts/scene_prisme.py → docs/design/scene-prisme.html
"""
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "design" / "scene-prisme.html"
W, H, HZ = 1800, 600, 400        # largeur, hauteur, ligne d'horizon
rnd = random.Random(3)

NUIT, NUIT2, SOL = "#0B1A3A", "#10265A", "#0D2150"
GRILLE = "#1D3C82"
BLEU, BLEU_L, ORANGE, OR, OR_L, OR_D, PAPIER = "#2E6FD3", "#5E93E6", "#FC4C02", "#FF8A3D", "#FFC29A", "#C2410C", "#FBF8F3"


def grid():
    lines = []
    vx = W / 2
    for xb in range(-2400, W + 2400, 110):                       # fuyantes
        lines.append(f'<line x1="{vx + (xb - vx) * .12:.1f}" y1="{HZ}" x2="{xb}" y2="{H}"/>')
    for k in range(1, 9):                                         # horizontales
        y = HZ + (H - HZ) * (k / 8) ** 1.8
        lines.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')
    return f'<g stroke="{GRILLE}" stroke-width="1.5" opacity=".7">{"".join(lines)}</g>'


def stars():
    out = []
    cols = [PAPIER, PAPIER, PAPIER, ORANGE, OR, BLEU_L]
    while len(out) < 34:
        x, y = rnd.randint(20, W - 20), rnd.randint(20, HZ - 120)
        if 120 < x < 1120 and 30 < y < 300:                     # zone du texte
            continue
        s = rnd.choice((4, 4, 5, 6))
        out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{rnd.choice(cols)}"/>')
    return "".join(out)


def station(x, y, label, color, up=86, big=False, below=False):
    s = 30 if big else 24
    i = 12 if big else 10
    ty = y + up - 4 if below else y - up - 26
    ly1, ly2 = (y + s / 2 + 4, y + up - 6) if below else (y - s / 2 - 4, y - up + 6)
    return f'''
    <line x1="{x}" y1="{ly1}" x2="{x}" y2="{ly2}" stroke="{PAPIER}" stroke-width="2" stroke-dasharray="5 5" opacity=".7"/>
    <rect x="{x - s / 2}" y="{y - s / 2}" width="{s}" height="{s}" fill="{NUIT}" stroke="{PAPIER}" stroke-width="3"/>
    <rect x="{x - i / 2}" y="{y - i / 2}" width="{i}" height="{i}" fill="{color}"/>
    <g transform="translate({x - 14},{ty})">
      <rect width="{len(label) * 9.6 + 28}" height="30" fill="{color}"/>
      <rect x="{len(label) * 9.6 + 28}" y="0" width="8" height="8" fill="{color}"/>
      <rect x="{len(label) * 9.6 + 28}" y="-8" width="8" height="8" fill="{color}"/>
      <rect x="{len(label) * 9.6 + 20}" y="-8" width="8" height="8" fill="{color}"/>
      <text x="14" y="20" fill="{PAPIER if color != OR else NUIT}" font-family="Instrument Sans" font-weight="600" font-size="15">{label}</text>
    </g>'''


def build():
    hills = (f'<path d="M0 {HZ} L0 330 Q 160 270 330 318 T 700 300 T 1050 326 T 1420 280 T 1800 300 L1800 {HZ} Z" fill="{NUIT2}"/>'
             f'<path d="M0 {HZ} L0 360 Q 260 330 520 352 T 1100 344 T 1800 336 L1800 {HZ} Z" fill="#0F2457"/>')
    ropes = f'''
    <defs>
      <linearGradient id="fb" gradientUnits="userSpaceOnUse" x1="560" y1="0" x2="820" y2="0"><stop offset="0" stop-color="{BLEU}" stop-opacity="0"/><stop offset="1" stop-color="{BLEU}"/></linearGradient>
      <linearGradient id="fo" gradientUnits="userSpaceOnUse" x1="300" y1="0" x2="520" y2="0"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
      <linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PAPIER}" stop-opacity="0"/><stop offset="1" stop-color="{PAPIER}"/></linearGradient>
    </defs>
    <!-- lumière qui entre dans le prisme -->
    <path d="M 1170 0 L 1262 178" stroke="url(#beam)" stroke-width="5" fill="none"/>
    <!-- corde bleue : sort du prisme, descend, file vers la gauche -->
    <path d="M 1330 168 H 1440 A 60 60 0 0 1 1500 228 V 400 A 56 56 0 0 1 1444 456 H 560" stroke="url(#fb)" stroke-width="22" fill="none"/>
    <!-- corde orange : passe par-dessus la bleue -->
    <path d="M 1334 196 H 1352 A 58 58 0 0 1 1410 254 V 470 A 56 56 0 0 1 1354 526 H 300" stroke="url(#fo)" stroke-width="22" fill="none"/>'''
    prism = f'''
    <g>
      <circle cx="1292" cy="178" r="96" fill="{OR}" opacity=".08"/>
      <circle cx="1292" cy="178" r="70" fill="{OR}" opacity=".1"/>
      <polygon points="1292,92 1214,232 1370,232" fill="{OR}"/>
      <polygon points="1292,92 1214,232 1292,232" fill="{OR_L}"/>
      <polygon points="1292,150 1262,206 1322,206" fill="{OR_D}" opacity=".55"/>
    </g>'''
    stations = (station(1240, 456, "Intelligence artificielle", BLEU, 92)
                + station(1020, 456, "Géospatial", BLEU, 78)
                + station(820, 456, "Cybersécurité", BLEU, 100)
                + station(1110, 526, "Données", ORANGE, 34, below=True)
                + station(700, 526, "Entrepreneuriat", ORANGE, 34, below=True))
    rings = (f'<circle cx="1240" cy="456" r="44" fill="none" stroke="{PAPIER}" stroke-width="2" stroke-dasharray="6 7" opacity=".45"/>'
             f'<path d="M 1240 412 A 44 44 0 0 1 1284 456" fill="none" stroke="{OR}" stroke-width="4"/>')
    svg = (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="La ligne PRISME : le prisme doré sépare la lumière en deux cordes, bleue et orange, dont les stations sont les filières du programme ; Syn et Néo attendent au départ, devant Yaoundé">'
           f'<rect width="{W}" height="{HZ}" fill="{NUIT}"/>{stars()}'
           f'<image href="../../assets/img/mascotte/yaounde-nuit.svg" x="-40" y="{HZ - 150}" width="800" height="150" style="image-rendering:pixelated"/>'
           f'{hills}<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="{SOL}"/>{grid()}{ropes}{prism}{rings}{stations}</svg>')
    html = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>SYNEO — La ligne PRISME</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&amp;family=Instrument+Sans:wght@400;600&amp;display=swap">
<style>
body{{margin:0;background:{NUIT}}}
.scene{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:'Instrument Sans',sans-serif}}
.scene svg{{position:absolute;inset:0;display:block}}
.txt{{position:absolute;left:150px;top:52px;color:{PAPIER}}}
h2{{margin:0;font-family:Syne,sans-serif;font-weight:800;font-size:40px;line-height:1.1;letter-spacing:-.01em}}
h2 span{{color:{ORANGE}}}
.btn{{display:inline-flex;align-items:center;gap:14px;margin-top:26px;height:58px;padding:0 30px;background:{ORANGE};color:#fff;font-family:Syne,sans-serif;font-weight:700;font-size:20px;text-decoration:none;
  clip-path:polygon(0 16px,8px 16px,8px 8px,16px 8px,16px 0,calc(100% - 16px) 0,calc(100% - 16px) 8px,calc(100% - 8px) 8px,calc(100% - 8px) 16px,100% 16px,100% calc(100% - 16px),calc(100% - 8px) calc(100% - 16px),calc(100% - 8px) calc(100% - 8px),calc(100% - 16px) calc(100% - 8px),calc(100% - 16px) 100%,16px 100%,16px calc(100% - 8px),8px calc(100% - 8px),8px calc(100% - 16px),0 calc(100% - 16px))}}
.duo{{position:absolute;left:150px;top:{526 - 11 - 150}px;width:220px;image-rendering:pixelated}}
</style>
</head>
<body>
<section class="scene">
{svg}
<div class="txt">
  <h2>Il est temps de bâtir ensemble.<br>Prêt à monter dans<br>la <span>ligne PRISME</span> ?</h2>
  <a class="btn" href="#">rejoindre prisme →</a>
</div>
<img class="duo" src="../../assets/img/mascotte/duo-main-dans-la-main.svg" alt="">
</section>
</body>
</html>
'''
    OUT.write_text(html, encoding="utf-8")
    print("✓", OUT.relative_to(ROOT))


if __name__ == "__main__":
    build()
