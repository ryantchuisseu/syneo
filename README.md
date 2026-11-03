# Sineo — site vitrine

Site vitrine de **Sineo** : vulgarisation tech, conférences, partenariats et networking.

- **Stack** : HTML / CSS / JavaScript statiques, sans build.
- **Langues** : FR d'abord, EN prévu (voir [Internationalisation](#internationalisation)).
- **Statut** : squelette de l'accueil en place, les autres pages sont suivies dans les issues.

## Démarrage rapide

```bash
git clone git@github.com:ryantchuisseu/sineo.git
cd sineo
python3 -m http.server 8000   # puis http://localhost:8000
```

N'importe quel serveur statique fait l'affaire (`npx serve`, extension Live Server…).

## Arborescence

```
sineo/
├── index.html              # Accueil
├── css/
│   ├── tokens.css          # Charte : couleurs, typo, espacements, rayons, ombres
│   ├── base.css            # Reset + styles globaux (s'appuie sur tokens.css)
│   └── components.css      # Header, boutons, cartes, sections, footer
├── js/
│   └── main.js             # Menu mobile, année du footer
├── assets/img/             # Images, logos, favicon
├── scripts/
│   └── create-issues.sh    # Crée les issues "une par page" via gh
└── .github/                # Modèles d'issue et de PR
```

## Pages prévues

| Page | Fichier | Issue |
|---|---|---|
| Accueil | `index.html` | Page : Accueil |
| Vulgarisation | `vulgarisation.html` | Page : Vulgarisation |
| Conférences | `conferences.html` | Page : Conférences |
| Partenariats | `partenariats.html` | Page : Partenariats |
| Networking | `networking.html` | Page : Networking |
| À propos | `a-propos.html` | Page : À propos |
| Contact | `contact.html` | Page : Contact |

## Charte graphique

Toutes les valeurs de design vivent dans **`css/tokens.css`** (custom properties CSS).

- **Ne jamais** écrire une couleur, une taille de police ou un espacement en dur ailleurs : utiliser `var(--…)`.
- Changer la charte = modifier `tokens.css` uniquement.
- Le mode sombre est géré dans ce même fichier (`prefers-color-scheme`).

## Internationalisation

Prévu plus tard, convention retenue dès maintenant :

- FR à la racine (`/index.html`), EN sous `/en/` (`/en/index.html`).
- Attribut `lang` correct sur chaque page, liens `hreflang` dans le `<head>`.
- Aucun texte dans le JS : tout le contenu reste dans le HTML.

## Contribuer

Une branche par tâche, PR obligatoire : voir **[CONTRIBUTING.md](CONTRIBUTING.md)**.
