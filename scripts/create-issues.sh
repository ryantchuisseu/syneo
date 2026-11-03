#!/usr/bin/env bash
# Crée les labels et une issue par page du site Sineo.
# Usage : ./scripts/create-issues.sh [owner/repo]   (défaut : ryantchuisseu/syneo)
set -euo pipefail

REPO="${1:-ryantchuisseu/syneo}"

# --- Labels (API REST) -----------------------------------------------------
label() {
  local name="$1" color="$2" desc="$3"
  gh api "repos/$REPO/labels" -f name="$name" -f color="$color" -f description="$desc" --silent 2>/dev/null \
    || gh api -X PATCH "repos/$REPO/labels/$name" -f color="$color" -f description="$desc" --silent
  echo "🏷️  label $name"
}
label page 4f46e5 "Création ou refonte d'une page"
label feat 06b6d4 "Nouvelle fonctionnalité"
label task f59e0b "Tâche (charte, contenu, outillage)"
label i18n 8b5cf6 "Traduction FR/EN"

DOD='## Definition of Done
- [ ] Responsive 360 / 768 / 1280 px
- [ ] Uniquement les tokens de `css/tokens.css`
- [ ] Accessibilité : contrastes AA, navigation clavier, `alt` sur les images
- [ ] Lien actif (`aria-current="page"`) dans la navigation, lien dans le footer
- [ ] `<title>` et `<meta name="description">` uniques
- [ ] Textes prêts pour la future version EN (aucun texte dans le JS)

> Branche : `feat/<n°>-page-<nom>` · PR obligatoire avec `Closes #<n°>`'

# Usage : new_issue "Titre" <<'EOF' ... EOF  (corps lu sur stdin)
new_issue() {
  local title="$1" body
  body="$(cat)"
  gh api "repos/$REPO/issues" -f title="$title" -f body="$body"$'\n\n'"$DOD" \
    -f 'labels[]=page' -f 'labels[]=feat' --jq '"✅ #\(.number) \(.title) → \(.html_url)"'
}

new_issue "Page : Accueil" <<'EOF'
**Fichier** : `index.html` (squelette déjà en place)

## Objectif
Présenter Sineo en 5 secondes et orienter vers les 4 piliers.

## Sections
- [x] Header + navigation responsive
- [x] Hero (accroche + 2 CTA)
- [x] 4 piliers (cartes)
- [x] Bandeau CTA contact + footer
- [ ] Chiffres clés (contenus publiés, conférences, participants, partenaires)
- [ ] Prochains événements (3 derniers)
- [ ] Logos partenaires
- [ ] Témoignages
- [ ] Visuel / illustration du hero
- [ ] Favicon + balises Open Graph
EOF

new_issue "Page : Vulgarisation" <<'EOF'
**Fichier** : `vulgarisation.html`

## Objectif
Donner accès aux contenus pédagogiques (articles, vidéos, fiches) et donner envie d'en lire plus.

## Sections
- [ ] Hero (promesse : « comprendre sans jargon »)
- [ ] Filtres par thème (IA, cloud, cybersécurité, data, web…) et par format
- [ ] Grille de contenus (carte : visuel, thème, titre, durée de lecture)
- [ ] Contenu mis en avant
- [ ] Inscription newsletter
EOF

new_issue "Page : Conférences" <<'EOF'
**Fichier** : `conferences.html`

## Objectif
Présenter les conférences à venir et passées, et faciliter l'inscription.

## Sections
- [ ] Hero + prochaine conférence mise en avant (date, lieu / en ligne, CTA inscription)
- [ ] Agenda des événements à venir
- [ ] Archives (replays, slides)
- [ ] Intervenants
- [ ] CTA « Proposer un talk »
EOF

new_issue "Page : Partenariats" <<'EOF'
**Fichier** : `partenariats.html`

## Objectif
Convaincre entreprises, écoles et associations de devenir partenaires.

## Sections
- [ ] Hero (bénéfices du partenariat)
- [ ] Types de partenariat (sponsoring, co-organisation, mécénat de compétences, média)
- [ ] Partenaires actuels (logos)
- [ ] Étapes pour devenir partenaire
- [ ] CTA vers le formulaire de contact (sujet pré-rempli) + kit partenaire PDF
EOF

new_issue "Page : Networking" <<'EOF'
**Fichier** : `networking.html`

## Objectif
Faire rejoindre la communauté et les événements de rencontre.

## Sections
- [ ] Hero (valeur de la communauté)
- [ ] Formats (afterworks, meetups, mentorat, communauté en ligne)
- [ ] Prochaines rencontres
- [ ] Témoignages de membres
- [ ] CTA « Rejoindre la communauté » (Discord / LinkedIn / WhatsApp à définir)
EOF

new_issue "Page : À propos" <<'EOF'
**Fichier** : `a-propos.html`

## Objectif
Inspirer confiance : qui est derrière Sineo, pourquoi, avec quelles valeurs.

## Sections
- [ ] Hero + mission
- [ ] Histoire de Sineo
- [ ] Valeurs (3 à 4)
- [ ] Équipe (photo, nom, rôle, lien LinkedIn)
- [ ] Chiffres clés / jalons
- [ ] CTA contact
EOF

new_issue "Page : Contact" <<'EOF'
**Fichier** : `contact.html`

## Objectif
Permettre de joindre Sineo simplement, avec le bon sujet.

## Sections
- [ ] Formulaire : nom, e-mail, sujet (Vulgarisation / Conférence / Partenariat / Networking / Autre), message
- [ ] Sujet pré-rempli via paramètre d'URL (`?sujet=partenariat`)
- [ ] Service d'envoi pour site statique (Formspree, Netlify Forms, Web3Forms… à choisir)
- [ ] Validation HTML5 + messages d'erreur accessibles + anti-spam (honeypot)
- [ ] Coordonnées et réseaux sociaux
- [ ] Mention RGPD sous le formulaire
EOF

echo "✅ Issues créées sur $REPO"
