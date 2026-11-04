#!/usr/bin/env python3
"""Insère la scène « ligne PRISME » (SVG) dans la maquette d'accueil.

Usage : python3 scripts/scene_prisme.py && python3 scripts/build_maquette.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENE = ROOT / "docs" / "design" / "scene-prisme.html"
PAGE = ROOT / "docs" / "design" / "maquette-accueil.html"

svg = re.search(r"<svg .*?</svg>", SCENE.read_text(encoding="utf-8"), re.S).group(0)
svg = re.sub(r' width="\d+" height="\d+"', ' preserveAspectRatio="xMidYMid slice"', svg, count=1)
block = f"<!--LIGNE-->\n    {svg}\n    <!--/LIGNE-->"

page = PAGE.read_text(encoding="utf-8")
page = re.sub(r"<!--LIGNE-->(.*?<!--/LIGNE-->)?", lambda m: block, page, count=1, flags=re.S)
PAGE.write_text(page, encoding="utf-8")
print("✓ scène insérée dans", PAGE.relative_to(ROOT))
