#!/usr/bin/env python3
"""Exploration « illustration à grain » : haut de la page d'accueil SYNEO.

Les 4 personnages du logo SYNEO (du petit bleu au grand orange, main dans la main)
debout sur la courbe du logo, entourés d'un grand ruban doré en forme de S.

Usage : python3 scripts/hero_illustre.py → docs/design/maquette-hero-illustre.html
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "design" / "maquette-hero-illustre.html"

# Couleurs prises sur le logo (du bleu à l'orange)
PEOPLE = [("#0B4DB3", "#083A8A", "#2E6FD3"), ("#1C5CC8", "#12459C", "#4A86E0"),
          ("#FC6A1A", "#D0500C", "#FF9150"), ("#FC4C02", "#C93C00", "#FF7A3D")]


def curve_y(x):
    """Courbe du logo (arc qui porte les personnages) : quadratique de (60,470) à (560,410), contrôle (300,560)."""
    # on résout x(t) puis on renvoie y(t)
    x0, cx, x1 = 60, 300, 560
    y0, cy, y1 = 470, 560, 410
    a, b, c = x0 - 2 * cx + x1, 2 * (cx - x0), x0 - x
    t = (-c / b) if abs(a) < 1e-9 else (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    return (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1


def person(x, feet, h, col, dark, light, wave=False):
    """Silhouette dans l'esprit du logo : tête ronde, buste arrondi, jambes, ombre à droite, reflet à gauche."""
    r = h * .11
    hy = feet - h + r
    t_top, t_bot, tw = hy + r * 1.35, feet - h * .44, h * .30
    lw, gap = h * .105, h * .035
    leg_l = x - gap / 2 - lw
    parts = []
    # jambes
    for lx, c in ((leg_l, col), (x + gap / 2, dark)):
        parts.append(f'<rect x="{lx:.1f}" y="{t_bot - 6:.1f}" width="{lw:.1f}" height="{feet - t_bot + 6:.1f}" rx="{lw / 2:.1f}" fill="{c}"/>')
    # buste
    parts.append(f'<rect x="{x - tw / 2:.1f}" y="{t_top:.1f}" width="{tw:.1f}" height="{t_bot - t_top:.1f}" rx="{tw * .42:.1f}" fill="{col}"/>')
    parts.append(f'<rect x="{x + tw * .12:.1f}" y="{t_top + 6:.1f}" width="{tw * .34:.1f}" height="{t_bot - t_top - 12:.1f}" rx="{tw * .17:.1f}" fill="{dark}" opacity=".55"/>')
    parts.append(f'<rect x="{x - tw * .38:.1f}" y="{t_top + 8:.1f}" width="{tw * .14:.1f}" height="{(t_bot - t_top) * .45:.1f}" rx="{tw * .07:.1f}" fill="{light}" opacity=".7"/>')
    # tête
    parts.append(f'<circle cx="{x:.1f}" cy="{hy:.1f}" r="{r:.1f}" fill="{col}"/>')
    parts.append(f'<path d="M {x + r * .1:.1f} {hy - r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x + r * .1:.1f} {hy + r:.1f} A {r * .8:.1f} {r:.1f} 0 0 0 {x + r * .1:.1f} {hy - r:.1f} Z" fill="{dark}" opacity=".45"/>')
    parts.append(f'<circle cx="{x - r * .38:.1f}" cy="{hy - r * .4:.1f}" r="{r * .22:.1f}" fill="{light}" opacity=".8"/>')
    sh = (x - tw / 2 + lw * .3, t_top + r * .5), (x + tw / 2 - lw * .3, t_top + r * .5)
    if wave:                                                   # le plus petit salue
        hx, hy2 = x - h * .32, t_top - h * .28
        parts.append(f'<path d="M {sh[0][0]:.1f} {sh[0][1]:.1f} Q {sh[0][0] - h * .2:.1f} {sh[0][1] - h * .02:.1f} {hx:.1f} {hy2:.1f}" stroke="{col}" stroke-width="{lw:.1f}" stroke-linecap="round" fill="none"/>')
        parts.append(f'<circle cx="{hx:.1f}" cy="{hy2:.1f}" r="{lw * .62:.1f}" fill="{col}"/>')
    return "\n".join(parts), sh


def illustration():
    xs = [150, 245, 360, 475]
    hs = [150, 196, 236, 272]
    figs, shoulders, feet = [], [], []
    for i, (x, h) in enumerate(zip(xs, hs)):
        f = curve_y(x) - 10
        col, dark, light = PEOPLE[i]
        svg, sh = person(x, f, h, col, dark, light, wave=(i == 0))
        figs.append(svg); shoulders.append(sh); feet.append(f)
    # bras qui se tiennent : de l'épaule droite d'une personne à l'épaule gauche de la suivante, mains jointes au milieu
    arms = []
    for i in range(3):
        (ax, ay), (bx, by) = shoulders[i][1], shoulders[i + 1][0]
        mx, my = (ax + bx) / 2, max(ay, by) + 44
        lw = hs[i] * .095
        arms.append(f'<path d="M {ax:.1f} {ay:.1f} Q {ax + 6:.1f} {my:.1f} {mx:.1f} {my:.1f}" stroke="{PEOPLE[i][0]}" stroke-width="{lw:.1f}" stroke-linecap="round" fill="none"/>')
        arms.append(f'<path d="M {bx:.1f} {by:.1f} Q {bx - 6:.1f} {my:.1f} {mx:.1f} {my:.1f}" stroke="{PEOPLE[i + 1][0]}" stroke-width="{lw:.1f}" stroke-linecap="round" fill="none"/>')
        arms.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{lw * .75:.1f}" fill="{PEOPLE[i + 1][0]}"/>')
    # bras extérieur du plus grand, le long du corps
    (ox, oy) = shoulders[3][1]
    arms.append(f'<path d="M {ox:.1f} {oy:.1f} Q {ox + 18:.1f} {oy + 60:.1f} {ox + 10:.1f} {oy + 105:.1f}" stroke="{PEOPLE[3][0]}" stroke-width="{hs[3] * .095:.1f}" stroke-linecap="round" fill="none"/>')
    shadows = "".join(f'<ellipse cx="{x:.1f}" cy="{f + 4:.1f}" rx="{h * .2:.1f}" ry="6" fill="#06142F" opacity=".35"/>' for x, f, h in zip(xs, feet, hs))
    return f'''
<svg class="ill" viewBox="0 0 620 600" role="img" aria-label="Les quatre personnages du logo SYNEO, du plus petit en bleu au plus grand en orange, se tiennent la main sur la courbe du logo, entourés d'un grand ruban doré">
  <defs>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0" result="na"/>
      <feComposite in="na" in2="SourceGraphic" operator="in" result="g"/>
      <feBlend in="SourceGraphic" in2="g" mode="multiply"/>
    </filter>
    <linearGradient id="arc" x1="0" x2="1"><stop offset="0" stop-color="#0B4DB3"/><stop offset=".55" stop-color="#5A4FA8"/><stop offset="1" stop-color="#FC4C02"/></linearGradient>
  </defs>
  <g filter="url(#grain)">
    <circle cx="330" cy="300" r="250" fill="#14305F"/>
    <circle cx="96" cy="120" r="22" fill="#F2B233"/>
    <circle cx="560" cy="250" r="16" fill="#FC4C02"/>
    <circle cx="540" cy="540" r="28" fill="#C2410C"/>
    <!-- grand ruban en S, derrière -->
    <path d="M 500 60 C 420 0, 270 30, 280 130 C 288 215, 470 205, 480 300" stroke="#F2B233" stroke-width="38" stroke-linecap="round" fill="none"/>
    {shadows}
    {"".join(figs)}
    {"".join(arms)}
    <!-- la courbe du logo, qui porte le groupe -->
    <path d="M 60 470 Q 300 560 560 410" stroke="url(#arc)" stroke-width="30" stroke-linecap="round" fill="none"/>
    <!-- le ruban repasse devant -->
    <path d="M 480 300 C 590 315, 598 455, 530 512 C 470 556, 400 548, 360 586" stroke="#F2B233" stroke-width="38" stroke-linecap="round" fill="none"/>
    <path d="M 548 335 C 580 380, 578 440, 548 478" stroke="#FFD66E" stroke-width="8" stroke-linecap="round" fill="none" opacity=".6"/>
  </g>
  <g fill="#FBF8F3"><circle cx="210" cy="40" r="5"/><circle cx="600" cy="140" r="4"/><circle cx="40" cy="300" r="4"/><circle cx="590" cy="380" r="5"/><circle cx="130" cy="560" r="4"/></g>
  <path d="M 60 230 l 6 14 l 14 6 l -14 6 l -6 14 l -6 -14 l -14 -6 l 14 -6 z" fill="#F2B233"/>
</svg>'''


def chip():
    """Trois petits avatars en ligne dans le titre."""
    faces = [("#0B4DB3", 14), ("#F2B233", 38), ("#FC4C02", 62)]
    return ('<svg class="chip" viewBox="0 0 92 46" aria-hidden="true">'
            + "".join(f'<circle cx="{cx}" cy="23" r="21" fill="{c}" stroke="#0E2347" stroke-width="3"/>'
                      f'<circle cx="{cx}" cy="18" r="6.5" fill="#FBF8F3"/><path d="M {cx - 11} 38 Q {cx} 22 {cx + 11} 38 Z" fill="#FBF8F3"/>'
                      for c, cx in faces) + '</svg>')


def bust(col, skin, x=0):
    return (f'<svg class="bust" viewBox="0 0 160 120" aria-hidden="true"><circle cx="80" cy="44" r="28" fill="{skin}"/>'
            f'<rect x="34" y="80" width="92" height="70" rx="40" fill="{col}"/><circle cx="70" cy="38" r="6" fill="#FBF8F3" opacity=".6"/></svg>')


HTML = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SYNEO — exploration illustrée</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&amp;display=swap">
<style>
:root{{--bg:#F3E9DD;--nuit:#0E2347;--nuit2:#14305F;--bleu:#02449B;--orange:#FC4C02;--or:#F2B233;--creme:#FBF8F3;--gris:#5A6478}}
*{{box-sizing:border-box}}
body{{margin:0;background:#3A2E2A;font-family:Outfit,system-ui,sans-serif;color:var(--nuit)}}
.page{{max-width:1360px;margin:40px auto;background:var(--bg);border-radius:36px;padding:26px 36px 0;overflow:hidden}}
nav{{display:flex;align-items:center;justify-content:space-between;padding:4px 20px 22px}}
.brand{{display:flex;align-items:center;gap:10px;text-decoration:none}}
.brand img{{height:46px}}
nav ul{{display:flex;gap:36px;list-style:none;margin:0;padding:0;font-size:15px}}
nav a{{color:var(--nuit);text-decoration:none}}
nav a[aria-current]{{font-weight:600}}
.tools{{display:flex;align-items:center;gap:16px}}
.ico{{width:20px;height:20px;border:2px solid var(--nuit);border-radius:50%}}
.pill{{display:inline-flex;white-space:nowrap;align-items:center;justify-content:center;height:42px;padding:0 24px;border-radius:999px;font-weight:600;font-size:15px;text-decoration:none}}
.pill.dark{{background:var(--bleu);color:#fff}}
.pill.gold{{background:var(--or);color:var(--nuit);height:48px;padding:0 28px}}

.hero{{position:relative;display:grid;grid-template-columns:1.02fr 1fr;min-height:560px}}
.card{{position:absolute;inset:0 0 60px 0;background:var(--nuit);border-radius:44px}}
.copy{{position:relative;padding:70px 0 0 64px;color:#fff;z-index:2}}
h1{{margin:0;font-weight:600;font-size:clamp(36px,4.1vw,56px);line-height:1.08;letter-spacing:-.015em}}
h1 em{{font-style:normal;color:var(--or)}}
.chip{{display:inline-block;width:2.1em;height:1em;vertical-align:-.12em;margin:0 .15em}}
.row{{display:flex;align-items:center;gap:40px;margin-top:38px}}
.stat b{{display:block;font-size:30px;font-weight:600;line-height:1}}
.stat span{{display:block;font-size:13px;color:var(--or);margin-top:6px}}
.ill{{position:relative;z-index:2;overflow:visible;width:112%;margin:-28px 0 0 -6%;height:auto}}
.tags{{position:absolute;left:0;bottom:0;width:47%;background:var(--bleu);border-radius:30px;padding:26px 30px;display:flex;flex-wrap:wrap;gap:12px;z-index:3;box-shadow:0 0 0 16px var(--bg)}}
.tags span{{border:1.5px solid rgba(255,255,255,.8);color:#fff;border-radius:999px;padding:6px 14px;font-size:14px}}

.mission{{display:grid;grid-template-columns:1fr 150px;align-items:center;gap:40px;padding:70px 40px 40px}}
.mission h2{{margin:0;font-weight:600;font-size:clamp(28px,2.9vw,40px);line-height:1.18;letter-spacing:-.01em}}
.mission h2 mark{{background:linear-gradient(transparent 58%,#FFD66E 58% 92%,transparent 92%);color:inherit}}
.badge{{position:relative;width:140px;height:140px}}
.badge svg.ring{{position:absolute;inset:0;animation:spin 16s linear infinite}}
.badge .core{{position:absolute;inset:44px;border-radius:50%;background:var(--orange);display:flex;align-items:center;justify-content:center}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{.badge svg.ring{{animation:none}}}}

.cards{{display:grid;grid-template-columns:140px repeat(3,1fr);gap:22px;padding:0 20px;align-items:start}}
.cards .lbl{{margin-top:6px}}
.outline{{display:inline-block;border:1.5px solid currentColor;border-radius:999px;padding:5px 14px;font-size:14px}}
.c{{border-radius:40px 40px 0 0;height:190px;padding:20px 24px;position:relative;overflow:hidden;color:#fff}}
.c.o{{background:#E2622A}}.c.g{{background:var(--or);color:var(--nuit)}}.c.b{{background:var(--bleu)}}
.c .bust{{position:absolute;left:50%;bottom:-30px;width:150px;transform:translateX(-50%)}}
@media (max-width:900px){{
  .page{{margin:0;border-radius:0;padding:16px 16px 0}}
  nav ul,.tools .ico{{display:none}}
  .hero{{grid-template-columns:1fr}}
  .card{{inset:0 0 0 0}}
  .copy{{padding:44px 28px 0}}
  .ill{{width:100%;margin:0}}
  .tags{{position:relative;width:100%;margin-top:16px;box-shadow:none}}
  .mission{{grid-template-columns:1fr;padding:48px 8px 24px}}
  .cards{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div class="page">
  <nav>
    <a class="brand" href="#"><img src="../../assets/img/logo-syneo-transparent.png" alt="SYNEO"></a>
    <ul><li><a href="#" aria-current="page">Accueil</a></li><li><a href="#">PRISME</a></li><li><a href="#">Conférences</a></li><li><a href="#">Partenaires</a></li></ul>
    <div class="tools"><span class="ico" aria-hidden="true"></span><span class="ico" aria-hidden="true"></span><a class="pill dark" href="#">Rejoindre</a></div>
  </nav>

  <section class="hero">
    <div class="card" aria-hidden="true"></div>
    <div class="copy">
      <h1>Connecter les talents<br>{chip()} pour <em>construire</em> le développement</h1>
      <div class="row">
        <a class="pill gold" href="#">Je m'inscris</a>
        <div class="stat"><b>500 – 1 000</b><span>participants attendus le 18 novembre</span></div>
        <div class="stat"><b>60 000</b><span>spécialistes IA visés d'ici 2040</span></div>
      </div>
    </div>
    <div>{illustration()}</div>
    <div class="tags"><span>Sensibilisation</span><span>Formation</span><span>Incubation</span><span>Mise en réseau</span></div>
  </section>

  <section class="mission">
    <h2>Seuls, nous créons des entreprises. <mark>Ensemble, nous bâtissons des écosystèmes.</mark></h2>
    <a class="badge" href="#" aria-label="En savoir plus sur SYNEO">
      <svg class="ring" viewBox="0 0 140 140" aria-hidden="true"><defs><path id="circ" d="M 70 70 m -52 0 a 52 52 0 1 1 104 0 a 52 52 0 1 1 -104 0"/></defs>
        <text font-family="Outfit" font-size="12.5" font-weight="600" letter-spacing="2.4" fill="#0E2347"><textPath href="#circ">EN SAVOIR PLUS · SUR SYNEO · EN SAVOIR PLUS ·</textPath></text></svg>
      <span class="core"><svg width="30" height="20" viewBox="0 0 30 20" aria-hidden="true"><path d="M 2 8 Q 15 22 28 4" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></svg></span>
    </a>
  </section>

  <section class="cards">
    <div class="lbl"><span class="outline">À propos</span></div>
    <div class="c o"><span class="outline">Notre mission</span>{bust("#0B4DB3", "#FBF8F3")}</div>
    <div class="c g"><span class="outline">Le programme PRISME</span>{bust("#FC4C02", "#0E2347")}</div>
    <div class="c b"><span class="outline">Nos partenaires</span>{bust("#F2B233", "#FBF8F3")}</div>
  </section>
</div>
</body>
</html>
'''

OUT.write_text(HTML, encoding="utf-8")
print("✓", OUT.relative_to(ROOT))
