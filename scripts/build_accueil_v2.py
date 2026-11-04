#!/usr/bin/env python3
"""Assemble la maquette complète de l'accueil (v2, pixel art + blocs arrondis).

Part du haut de page docs/design/maquette-hero-pixel.html, ajoute les sections
suivantes et insère la scène « ligne PRISME ».

Usage : python3 scripts/scene_prisme.py && python3 scripts/build_accueil_v2.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "docs" / "design"
src = (D / "maquette-hero-pixel.html").read_text(encoding="utf-8")
ligne = re.search(r"<svg .*?</svg>", (D / "scene-prisme.html").read_text(encoding="utf-8"), re.S).group(0)
ligne = re.sub(r' width="\d+" height="\d+"', ' preserveAspectRatio="xMidYMid slice" class="ligne-svg"', ligne, count=1)

CSS = """
/* ======== Sections v2 ======== */
.sec{padding:96px 20px 0}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;flex-wrap:wrap;margin-bottom:40px}
.sec-head h2{margin:12px 0 0;font-family:Syne,sans-serif;font-weight:700;font-size:clamp(30px,3.4vw,48px);line-height:1.05;letter-spacing:-.02em}
.sec-head p{max-width:440px;color:var(--gris);font-size:17px;line-height:1.6;margin:0}
.hl{background:linear-gradient(transparent 58%,#FFD66E 58% 92%,transparent 92%)}

/* Cartes « à propos » remplies */
.c p{position:relative;z-index:1;margin:14px 0 0;font-size:15px;line-height:1.5;max-width:240px}
.c{height:auto;min-height:300px;padding-bottom:150px}

/* Programme : liste dans un bloc blanc arrondi */
.prog-box{background:var(--creme);border-radius:40px;padding:12px 44px}
.prow{position:relative;display:grid;grid-template-columns:minmax(0,1.15fr) 140px 56px minmax(0,1fr);align-items:center;gap:20px;padding:26px 0 30px;border-bottom:2px solid var(--nuit);text-decoration:none;color:inherit}
.prow:last-child{border-bottom:0}
.prow .tagp{grid-column:1/-1;justify-self:start;background:var(--nuit);color:#fff;font-size:13px;font-weight:700;padding:6px 12px;clip-path:var(--px)}
.prow .tagp em{font-style:normal;color:var(--or)}
.prow h3{margin:0;font-family:Syne,sans-serif;font-weight:700;font-size:clamp(26px,3vw,42px);line-height:1;letter-spacing:-.02em;color:var(--bleu)}
.prow .mas{justify-self:center;align-self:end;margin-bottom:-32px;height:100px}
.arw{width:48px;height:40px;position:relative;transition:transform .2s steps(2)}
.arw::before{content:"";position:absolute;left:0;top:16px;width:34px;height:8px;background:var(--nuit)}
.arw::after{content:"";position:absolute;right:6px;top:4px;width:22px;height:22px;border-top:8px solid var(--nuit);border-right:8px solid var(--nuit);transform:rotate(45deg)}
.prow:hover .arw{transform:translateX(8px)}
.prow .desc{margin:0;font-weight:600;font-size:17px;line-height:1.55}
.prow .desc u{text-decoration-color:var(--orange);text-decoration-thickness:3px;text-underline-offset:5px}

/* Agenda : bloc nuit arrondi, tuiles dates */
.agenda{background:var(--nuit);border-radius:44px;padding:56px 48px 48px;color:#fff;position:relative;overflow:hidden}
.agenda::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:8px 8px;pointer-events:none}
.agenda .sec-head p{color:#C9D3E6}
.agenda .hl{background:var(--or);color:var(--nuit);padding:0 .2em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;position:relative;z-index:1}
.tile{background:#14305F;border-radius:26px;padding:22px;display:flex;flex-direction:column;gap:8px;text-decoration:none;color:#fff;transition:transform .2s steps(2)}
.tile:hover{transform:translateY(-6px)}
.tile.hot{background:var(--orange)}
.tile small{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--or)}
.tile.hot small{color:var(--nuit)}
.tile b{font-family:Syne,sans-serif;font-size:22px;line-height:1.15}
.tile span{font-size:14px;color:#C9D3E6}
.tile.hot span{color:#fff}
.tile .big{font-family:Syne,sans-serif;font-weight:800;font-size:56px;line-height:.85}
.agenda .more{position:relative;z-index:1;margin-top:28px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.agenda .more p{margin:0;color:#C9D3E6;font-size:15px}

/* Tribune */
.trib{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.tc{border-radius:36px;padding:26px 24px 24px;display:flex;flex-direction:column;gap:12px;text-decoration:none;color:var(--nuit);background:var(--creme);transition:transform .2s steps(2)}
.tc:hover{transform:translateY(-6px)}
.tc.hot{background:var(--orange);color:#fff}
.tc .top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.tc h3{margin:0;font-family:Syne,sans-serif;font-weight:700;font-size:26px;line-height:1.05}
.tc p{margin:0;font-size:15px;line-height:1.5;min-height:66px}
.tc.hot p{color:var(--nuit);font-weight:500}
.go{flex-shrink:0;width:52px;height:52px;background:var(--orange);clip-path:var(--px);position:relative}
.tc.hot .go{background:var(--creme)}
.go::before{content:"";position:absolute;left:16px;top:24px;width:21px;height:4px;background:#fff;transform:rotate(-45deg)}
.go::after{content:"";position:absolute;left:22px;top:15px;width:12px;height:12px;border-top:4px solid #fff;border-right:4px solid #fff}
.tc.hot .go::before{background:var(--orange)}.tc.hot .go::after{border-color:var(--orange)}
.tc img{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:22px;image-rendering:pixelated}

/* Chiffres */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.st{border-radius:30px;padding:28px 24px;background:var(--creme)}
.st:nth-child(2){background:var(--or)}.st:nth-child(3){background:#E2622A;color:#fff}.st:nth-child(4){background:var(--bleu);color:#fff}
.st b{display:block;font-family:Syne,sans-serif;font-weight:800;font-size:clamp(34px,3.4vw,50px);line-height:1;white-space:nowrap}
.st span{display:block;margin-top:10px;font-size:15px;line-height:1.45}
.st small{display:block;margin-top:8px;font-size:12px;opacity:.75}

/* Partenaires */
.partners{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.pt{border-radius:30px;border:2px solid var(--nuit);padding:26px}
.pt strong{display:block;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--orange);margin-bottom:12px}
.pt span{display:block;font-family:Syne,sans-serif;font-weight:700;font-size:19px;line-height:1.5;color:var(--bleu)}

/* Ligne PRISME */
.ligne{position:relative;border-radius:44px;overflow:hidden;background:#0B1A3A;aspect-ratio:3/1;min-height:420px}
.ligne-svg{position:absolute;inset:0;width:100%;height:100%}
.ligne .txt{position:absolute;left:6%;top:10%;max-width:640px;color:#fff;z-index:2}
.ligne h2{margin:0 0 20px;font-family:Syne,sans-serif;font-weight:800;font-size:clamp(22px,2.2vw,32px);line-height:1.1}
.ligne h2 em{font-style:normal;color:var(--orange)}
.ligne .btn{background:var(--orange);color:#fff}
.ligne .duo{position:absolute;left:8.3%;bottom:13%;width:12%;z-index:2;image-rendering:pixelated}

/* Pied de page */
.foot{margin-top:96px;background:var(--bleu);color:#fff;border-radius:44px 44px 0 0;position:relative;overflow:hidden}
.foot .sky{display:block;width:100%;height:120px;object-fit:cover;object-position:bottom;background:var(--bg);image-rendering:pixelated}
.foot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.4fr;gap:36px;padding:40px 48px 32px}
.foot h4{margin:0 0 14px;font-family:Syne,sans-serif;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--or)}
.foot ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px;font-size:15px}
.foot a{color:#fff;text-decoration:none}
.foot p{margin:0;color:#DCE6F7;font-size:15px;line-height:1.6}
.nl{display:flex;margin-top:14px}
.nl input{flex:1;min-width:0;height:48px;border:0;padding:0 14px;font:inherit;font-size:15px}
.nl button{height:48px;border:0;background:var(--orange);color:#fff;font-family:Syne,sans-serif;font-weight:700;padding:0 18px;cursor:pointer}
.legal{border-top:1px solid rgba(255,255,255,.2);padding:18px 48px 26px;display:flex;justify-content:space-between;font-size:13px;color:#C9D8F0}
.wa{position:fixed;right:20px;bottom:20px;z-index:30;display:flex;align-items:center;gap:10px;background:var(--nuit);color:#fff;text-decoration:none;font-weight:700;font-size:15px;padding:8px 16px 8px 8px;clip-path:var(--px)}
.wa img{width:40px;height:40px;background:var(--creme);image-rendering:pixelated}

@media (max-width:1000px){
  .tiles,.stats{grid-template-columns:repeat(2,minmax(0,1fr))}
  .prow{grid-template-columns:1fr 110px minmax(0,1fr)}.arw{display:none}
  .foot .cols{grid-template-columns:1fr 1fr}
}
@media (max-width:900px){
  .sec{padding:64px 0 0}
  .prog-box{padding:8px 22px}
  .prow{grid-template-columns:1fr;gap:10px}.prow .mas{display:none}
  .agenda{padding:40px 22px}
  .tiles,.trib,.partners,.stats{grid-template-columns:1fr}
  .ligne{aspect-ratio:auto;min-height:0;display:flex;flex-direction:column}
  .ligne .txt{position:relative;left:auto;top:auto;padding:40px 22px 8px}
  .ligne-svg{position:relative;height:330px;width:990px;max-width:none;align-self:flex-end}
  .ligne .duo{width:100px;left:16px;bottom:22px}
  .foot{border-radius:30px 30px 0 0}
  .foot .cols{grid-template-columns:1fr;padding:32px 22px}
  .legal{padding:16px 22px 80px;flex-direction:column;gap:6px}
  .wa span{display:none}.wa{padding:8px}
}
</style>"""

CARDS = """  <section class="cards">
    <div><span class="outline">À propos</span></div>
    <a class="c o" href="#"><span class="outline">Notre mission</span><p>Sensibiliser, former, incuber et mettre en réseau les jeunes porteurs de projet.</p><img class="vig" src="../../assets/img/vignettes/escalier.png" alt="Néo tend la main à Syn pour l'aider à monter les marches"></a>
    <a class="c g" href="#programme"><span class="outline">Le programme PRISME</span><p>Treize mois et sept composantes, de la conférence inaugurale au Forum National.</p><img class="vig" src="../../assets/img/vignettes/randonnee.png" alt="Syn et Néo, sacs au dos, montent vers le drapeau au sommet"></a>
    <a class="c b" href="#partenaires"><span class="outline">Nos partenaires</span><p>Institutions, écoles, entreprises et médias qui bâtissent avec nous.</p><img class="vig" src="../../assets/img/vignettes/poignee.png" alt="Néo serre la main d'un partenaire, Syn tient le dossier"></a>
  </section>"""

SECTIONS = f"""
  <!-- Chiffres -->
  <section class="sec">
    <div class="stats">
      <div class="st"><b>27,7 %</b><span>des entreprises camerounaises passent le cap des 5 ans</span><small>Source : CAMERCAP-PARC</small></div>
      <div class="st"><b>60 000</b><span>spécialistes en IA à former d'ici 2040</span><small>Stratégie Nationale d'IA</small></div>
      <div class="st"><b>207</b><span>start-up IA actives en Afrique, 86 % toujours en activité</span><small>17 pays</small></div>
      <div class="st"><b>24</b><span>épisodes de la série « PRISME : Les Bâtisseurs »</span><small>CRTV et médias partenaires</small></div>
    </div>
  </section>

  <!-- Programme PRISME -->
  <section class="sec" id="programme">
    <div class="sec-head">
      <div><span class="outline">Programme PRISME</span><h2>Chaque étape compte.</h2></div>
      <p>Une plateforme nationale de sensibilisation, de formation, d'incubation et de mise en réseau, <span class="hl">de novembre 2026 à décembre 2027</span>.</p>
    </div>
    <div class="prog-box">
      <a class="prow" href="#"><span class="tagp">18 novembre 2026</span><h3>Conférence inaugurale</h3><img class="mas" src="../../assets/img/vignettes/conference.png" alt="Néo au pupitre devant le public"><span class="arw" aria-hidden="true"></span><p class="desc">À l'<u>ENSPY</u>, de 10 h à 13 h 30 : lancement officiel, panel et premier tournage de la série.</p></a>
      <a class="prow" href="maquette-conferences.html"><span class="tagp">Janvier → juin 2027</span><h3>Conférences thématiques</h3><img class="mas" src="../../assets/img/vignettes/etudier.png" alt="Syn révise au bureau, l'idée s'allume"><span class="arw" aria-hidden="true"></span><p class="desc"><u>6 conférences</u> itinérantes, chacune sur un site d'enseignement supérieur différent.</p></a>
      <a class="prow" href="#"><span class="tagp">Juillet → novembre 2027</span><h3>Formation &amp; incubation</h3><img class="mas" src="../../assets/img/vignettes/atelier.png" alt="Syn code, Néo le guide"><span class="arw" aria-hidden="true"></span><p class="desc">Une cohorte de <u>40 à 60 porteurs de projet</u> formés et accompagnés.</p></a>
      <a class="prow" href="#"><span class="tagp">Toute l'année · <em>série</em></span><h3>Les Bâtisseurs</h3><img class="mas" src="../../assets/img/vignettes/tournage.png" alt="Syn filme Néo qui salue"><span class="arw" aria-hidden="true"></span><p class="desc"><u>24 épisodes</u> diffusés sur la CRTV et les médias partenaires.</p></a>
      <a class="prow" href="#"><span class="tagp">Décembre 2027</span><h3>Forum National</h3><img class="mas" src="../../assets/img/vignettes/forum.png" alt="Trois personnages échangent sous une banderole"><span class="arw" aria-hidden="true"></span><p class="desc">Forum National de l'<u>écosystème entrepreneurial</u>, en clôture du programme.</p></a>
    </div>
  </section>

  <!-- Agenda -->
  <section class="sec">
    <div class="agenda">
      <div class="sec-head" style="position:relative;z-index:1">
        <div><span class="outline" style="color:#F2B233">Agenda</span><h2>Six campus, une saison.</h2></div>
        <p><span class="hl">Une conférence par mois, de janvier à juin 2027</span>, chacune dans une école différente.</p>
      </div>
      <div class="tiles">
        <a class="tile hot" href="#"><small>Lancement</small><span class="big">18.11</span><b>Conférence inaugurale</b><span>ENSPY, Yaoundé · 10 h</span></a>
        <a class="tile" href="maquette-conferences.html"><small>Conférence 1</small><b>Compréhension</b><span>ENSPY · campus suggéré</span></a>
        <a class="tile" href="maquette-conferences.html"><small>Conférence 2</small><b>Construction</b><span>Université de Yaoundé I · campus suggéré</span></a>
        <a class="tile" href="maquette-conferences.html"><small>Conférence 3</small><b>Application</b><span>SUP'PTIC · campus suggéré</span></a>
      </div>
      <div class="more"><p>Puis Production (IAI-Cameroun), Modèles économiques (ESSTIC) et Entrepreneuriat &amp; Écosystème (NUMIATECH).</p><a class="btn gold" href="maquette-conferences.html">Voir la route des campus</a></div>
    </div>
  </section>

  <!-- Tribune -->
  <section class="sec" id="tribune">
    <div class="sec-head">
      <div><span class="outline">La tribune</span><h2>La parole aux bâtisseurs.</h2></div>
      <p>Les membres publient, <span class="hl">l'équipe SYNEO vérifie chaque contenu</span> avant la mise en ligne.</p>
    </div>
    <div class="trib">
      <a class="tc" href="#"><div class="top"><h3>Raconte<br>ton parcours</h3><span class="go" aria-hidden="true"></span></div><p>Porteur de projet ? Partage tes réussites, tes galères et ce que tu as appris.</p><img src="../../assets/img/scenes/tribune-parcours.png" alt="Syn dans son bureau, la nuit, avec vue sur Yaoundé"></a>
      <a class="tc hot" href="#"><div class="top"><h3>Partage<br>ton expertise</h3><span class="go" aria-hidden="true"></span></div><p>Développeur, chercheur, mentor ? Publie une analyse ou un tutoriel.</p><img src="../../assets/img/scenes/tribune-expertise.png" alt="Néo présente des graphiques, Syn lève la main"></a>
      <a class="tc" href="#"><div class="top"><h3>Fais grandir<br>le réseau</h3><span class="go" aria-hidden="true"></span></div><p>Une rencontre, un stage, un appel à projets ? Propose-le à la communauté.</p><img src="../../assets/img/scenes/tribune-reseau.png" alt="Syn et Néo dans un espace de rencontre"></a>
    </div>
  </section>

  <!-- Partenaires -->
  <section class="sec" id="partenaires">
    <div class="sec-head">
      <div><span class="outline">Partenaires</span><h2>Une synergie nationale.</h2></div>
      <a class="btn dark" href="#">Dossier de sponsoring</a>
    </div>
    <div class="partners">
      <div class="pt"><strong>Institutionnels</strong><span>MINPOSTEL<br>Ministère de l'Enseignement Supérieur<br>ESSTIC · ENSPY</span></div>
      <div class="pt"><strong>Techniques</strong><span>Chaire UNESCO Accès TIC<br>Programme AgroPole · Néo Industry<br>Bass Technology · IAC</span></div>
      <div class="pt"><strong>Production</strong><span>MY LAB Production<br>CAMIGRA<br>TIIANA</span></div>
    </div>
  </section>

  <!-- Ligne PRISME -->
  <section class="sec">
    <div class="ligne">
      {ligne}
      <div class="txt"><h2>Il est temps de bâtir ensemble.<br>Prêt à monter dans la <em>ligne PRISME</em> ?</h2><a class="btn" href="#">Rejoindre PRISME</a></div>
      <img class="duo" src="../../assets/img/mascotte/duo-main-dans-la-main.svg" alt="">
    </div>
  </section>

  <footer class="foot">
    <img class="sky" src="../../assets/img/mascotte/yaounde-bleu.svg" alt="">
    <div class="cols">
      <div><img src="../../assets/img/logo-syneo-transparent.png" alt="SYNEO" style="height:52px;background:var(--creme);padding:4px 6px"><p style="margin-top:16px">Association pour la Synergie de l'Innovation, de l'Entrepreneuriat et des Opportunités.</p></div>
      <div><h4>Explorer</h4><ul><li><a href="#programme">Programme PRISME</a></li><li><a href="maquette-conferences.html">Conférences</a></li><li><a href="#tribune">La tribune</a></li><li><a href="#partenaires">Partenaires</a></li></ul></div>
      <div><h4>Nous trouver</h4><ul><li>Yaoundé, Biteng<br>Entrée Express Union</li><li><a href="mailto:syneo3123@gmail.com">syneo3123@gmail.com</a></li><li>657 30 04 79</li></ul></div>
      <div><h4>La lettre SYNEO</h4><p>Les dates, les appels à projets et les portraits.</p><form class="nl" onsubmit="return false"><label for="nlm" style="position:absolute;left:-999px">Adresse e-mail</label><input id="nlm" type="email" placeholder="ton@email.com"><button type="submit">ok</button></form></div>
    </div>
    <div class="legal"><span>© 2026 SYNEO · La Synergie pour le développement</span><span>FR · EN</span></div>
  </footer>
"""

out = src.replace("</style>", CSS, 1)
out = re.sub(r"  <section class=\"cards\">.*?</section>", CARDS, out, count=1, flags=re.S)
out = out.replace("</div>\n</body>", SECTIONS + "</div>\n<a class=\"wa\" href=\"#\" aria-label=\"Écrire à SYNEO sur WhatsApp\"><img src=\"../../assets/img/mascotte/avatar.svg\" alt=\"\"><span>Une question ? WhatsApp</span></a>\n</body>", 1)
out = out.replace("<title>SYNEO — accueil, pixel art animé</title>", "<title>SYNEO — Connecter les talents, construire le développement</title>")

# ---------------------------------------------------------------------------
# Grain 8 bits, bandes à vague pixel et décors (ajoutés après coup)
import math as _m


def wave(color, seed=0, flip=False):
    """Bord de vague en escalier de pixels (marches de 8 px)."""
    d = "M0 64 "
    for i in range(0, 1441, 16):
        y = 24 + 14 * _m.sin(i / 1440 * 2 * _m.pi * 1.5 + seed) + 6 * _m.sin(i / 90 + seed * 2)
        y = round(y / 8) * 8
        d += f"V{y} H{i + 16} "
    d += "V64 Z"
    tf = ' style="transform:scaleY(-1)"' if flip else ""
    return f'<svg class="wave" viewBox="0 0 1456 64" preserveAspectRatio="none" shape-rendering="crispEdges" aria-hidden="true"{tf}><path d="{d}" fill="{color}"/></svg>'


def deco(name, style):
    return f'<img class="deco" src="../../assets/img/deco/{name}.svg" alt="" style="{style}">'


CSS2 = """
/* ======== Grain 8 bits ======== */
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:60;background:url(../../assets/img/deco/grain-clair.png) 0 0/96px 96px;image-rendering:pixelated}
.card::after,.agenda::after{background:url(../../assets/img/deco/grain-sombre.png) 0 0/96px 96px!important;image-rendering:pixelated}
.ligne::after,.foot::after,.band.bleu::after{content:"";position:absolute;inset:0;pointer-events:none;background:url(../../assets/img/deco/grain-sombre.png) 0 0/96px 96px;image-rendering:pixelated;z-index:1}
.ligne .txt,.ligne .duo{z-index:3}
/* ======== Formes ======== */
.sec,.mission,.cards,.hero,.band{position:relative}
.deco{position:absolute;image-rendering:pixelated;pointer-events:none;z-index:0;opacity:.18}
.deco.vif{opacity:1}
.mission > *, .sec > *{position:relative;z-index:1}
.mission > .deco,.sec > .deco,.band > .deco{position:absolute;z-index:0}
.wave{display:block;width:calc(100% + 72px);height:56px;margin:96px -36px -1px}
.band{margin:0 -36px;padding:24px 56px 80px;background:var(--bc)}
.band .sec{padding-top:0}
.band.ciel{--bc:#DCEBFF}
.band.peche{--bc:#FCE3D2}
.wave + .band + .wave{margin-top:-1px}
@media (max-width:900px){
  .wave{width:calc(100% + 32px);margin:64px -16px -1px;height:36px}
  .band{margin:0 -16px;padding:16px 16px 56px}
  .deco{display:none}
}
</style>"""

out = out.replace("</style>", CSS2, 1)
out = out.replace(".card::after{content:\"\";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:8px 8px}",
                  ".card::after{content:\"\";position:absolute;inset:0;pointer-events:none}")
# bandes : tribune sur fond ciel, partenaires sur fond pêche
out = out.replace("  <!-- Tribune -->\n  <section class=\"sec\" id=\"tribune\">",
                  "  <!-- Tribune -->\n  " + wave("#DCEBFF", 1) + "\n  <div class=\"band ciel\">\n"
                  + "  " + deco("engrenage", "right:3%;top:-10px;width:120px;opacity:.16") + deco("etincelle-orange", "left:2%;top:40px;width:39px;opacity:1") + "\n"
                  + "  <section class=\"sec\" id=\"tribune\">")
out = out.replace("  <!-- Partenaires -->", "  </div>\n  " + wave("#FCE3D2", 2.4) + "\n  <div class=\"band peche\">\n  "
                  + deco("tuyau", "right:4%;top:-6px;width:200px;opacity:.16") + deco("anneau-orange", "left:3%;bottom:30px;width:60px;opacity:.9") + "\n  <!-- Partenaires -->")
out = out.replace("  <!-- Ligne PRISME -->", "  </div>\n  " + wave("#FCE3D2", 2.4, flip=True) + "\n  <!-- Ligne PRISME -->")
# décors semés
out = out.replace('<section class="mission">', '<section class="mission">' + deco("engrenage", "right:20%;top:20px;width:96px") + deco("zigzag-orange", "left:1%;top:28px;width:108px;opacity:1"), 1)
out = out.replace("  <!-- Chiffres -->\n  <section class=\"sec\">", "  <!-- Chiffres -->\n  <section class=\"sec\">" + deco("croix-or", "right:1%;top:44px;width:27px;opacity:1") + deco("anneau", "left:-14px;top:40px;width:60px"), 1)
out = out.replace("  <!-- Programme PRISME -->\n  <section class=\"sec\" id=\"programme\">", "  <!-- Programme PRISME -->\n  <section class=\"sec\" id=\"programme\">" + deco("etincelle-or", "left:46%;top:60px;width:39px;opacity:1") + deco("tuyau", "right:-10px;top:520px;width:160px"), 1)
out = out.replace('<div class="agenda">', '<div class="agenda">' + deco("engrenage-clair", "right:-30px;bottom:-30px;width:180px;opacity:.12") + deco("croix-or", "right:42%;top:36px;width:27px;opacity:1"), 1)

# ---------------------------------------------------------------------------
# Bits visibles sur les zones claires (7 à 9 par zone), à la place du grain fin
import random as _r


def bits(seed, n=8):
    return f'<div class="bits" data-seed="{seed}" data-n="{n}" aria-hidden="true"></div>'


CSS3 = """
/* Bits tech visibles sur les zones claires (remplacent le grain fin) */
body::after{display:none}
.bits{position:absolute;inset:0;pointer-events:none;z-index:0}
.bit{position:absolute;display:block}
.bit.blink{animation:led 3.2s steps(1) infinite}
@keyframes led{0%,70%{opacity:1}71%,85%{opacity:.15}86%,100%{opacity:1}}
@media (prefers-reduced-motion:reduce){.bit.blink{animation:none}}
@media (max-width:900px){.bits .bit:nth-child(n+5){display:none}}
</style>"""
out = out.replace("</style>", CSS3, 1)
zones = [('<section class="mission">', 11, 9), ('  <section class="cards">', 12, 9),
         ('  <!-- Chiffres -->\n  <section class="sec">', 13, 9), ('<section class="sec" id="programme">', 14, 14),
         ('<section class="sec" id="tribune">', 15, 9), ('<div class="band peche">', 16, 9)]
for marker, seed, n in zones:
    assert marker in out, marker
    out = out.replace(marker, marker + bits(seed, n), 1)

# ---------------------------------------------------------------------------
# Charte sans jaune + mise en page des vignettes + placement des bits
CSS4 = """
:root{--or:#FF8A3D;--ciel:#DCEBFF;--peche:#FFD2BD}
.btn.gold{background:var(--orange);color:#fff}
.c.g{background:var(--ciel);color:var(--nuit)}
.st:nth-child(2){background:var(--ciel)}
.hl,.mission mark{background:linear-gradient(transparent 58%,var(--peche) 58% 92%,transparent 92%)!important}
.agenda .hl{background:var(--peche)!important}
/* Cartes à propos : la scène occupe tout le bas */
.c{display:flex;flex-direction:column;min-height:0;padding:22px 22px 0}
.c .outline{align-self:flex-start}
.c img.vig{position:static;transform:none;display:block;width:100%;height:auto;margin-top:18px;image-rendering:pixelated}
.c:hover img.vig{transform:translateY(-6px)}
/* Programme : grande scène entre le titre et le texte */
.prow{grid-template-columns:minmax(0,.9fr) 252px 52px minmax(0,1fr)}
.prow .mas{width:252px;height:auto;margin:0;align-self:center;image-rendering:pixelated}
@media (max-width:1000px){.prow{grid-template-columns:1fr 200px minmax(0,1fr)}.prow .mas{width:200px}}
@media (max-width:900px){.prow .mas{display:block;width:100%;max-width:300px}}
</style>"""
out = out.replace("</style>", CSS4, 1)
for a, b in (("#F2B233", "#FF8A3D"), ("#FFD66E", "#FFD2BD"), ("#C98E1B", "#C2410C")):
    out = out.replace(a, b)

JS = """
<script>
/* Bits tech : placés au hasard (graine fixe) dans les espaces vides, jamais sur du texte ni sur une carte */
(function () {
  const COLS = ['#02449B', '#02449B', '#2E6FD3', '#FC4C02', '#FF8A3D'];
  const SHAPES = [[[0,0]], [[0,0]], [[0,0],[1,0]], [[0,0],[0,1]], [[0,0],[1,1]], [[0,0],[1,0],[1,1]]];
  const OBST = 'h2,h3,p,a,img,.outline,.st,.c,.prog-box,.tc,.pt,.tiles,.badge,.btn,.sec-head > *';
  function rng(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function place() {
    const small = innerWidth < 900;
    document.querySelectorAll('.bits').forEach(box => {
      box.innerHTML = '';
      const host = box.parentElement, hr = host.getBoundingClientRect();
      const r = rng(+box.dataset.seed), n = small ? Math.ceil(+box.dataset.n / 2) : +box.dataset.n;
      const obs = [...host.querySelectorAll(OBST)].filter(e => !box.contains(e)).map(e => { const b = e.getBoundingClientRect(); return [b.left - hr.left - 14, b.top - hr.top - 14, b.right - hr.left + 14, b.bottom - hr.top + 14]; });
      const placed = [];
      for (let k = 0, tries = 0; k < n && tries < 600; tries++) {
        const u = [8, 8, 10, 12][Math.floor(r() * 4)], sh = SHAPES[Math.floor(r() * SHAPES.length)];
        const x = r() * (hr.width - 3 * u), y = r() * (hr.height - 3 * u);
        const box2 = [x, y, x + 2 * u, y + 2 * u];
        const hit = q => !(box2[2] < q[0] || box2[0] > q[2] || box2[3] < q[1] || box2[1] > q[3]);
        if (obs.some(hit) || placed.some(q => Math.hypot(q[0] - x, q[1] - y) < 90)) continue;
        placed.push(box2); k++;
        const c = COLS[Math.floor(r() * COLS.length)];
        const i = document.createElement('i');
        i.className = 'bit' + (r() < .35 ? ' blink' : '');
        i.style.cssText = `left:${x}px;top:${y}px;width:${u}px;height:${u}px;background:${c};animation-delay:${(r() * 2.4).toFixed(1)}s;` +
          (sh.length > 1 ? 'box-shadow:' + sh.slice(1).map(([dx, dy]) => `${dx * u}px ${dy * u}px 0 ${c}`).join(',') : '');
        box.appendChild(i);
      }
    });
  }
  let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(place, 150); });
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => requestAnimationFrame(place));
})();
</script>
</body>"""
out = out.replace("</body>", JS, 1)
out = out.replace("@media (max-width:900px){.bits .bit:nth-child(n+5){display:none}}", "")

(D / "maquette-accueil-v2.html").write_text(out, encoding="utf-8")
print("✓ docs/design/maquette-accueil-v2.html")
