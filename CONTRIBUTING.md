# Contribuer à Sineo

## Règles d'or

1. **Une issue = une tâche = une branche.**
2. **Aucun commit direct sur `main`.** Tout passe par une Pull Request.
3. **Une PR = une issue**, liée avec `Closes #<numéro>`.
4. Au moins **1 relecture approuvée** avant merge.

## Workflow

```bash
# 1. Partir d'un main à jour
git checkout main
git pull origin main

# 2. Créer la branche de la tâche
git checkout -b feat/12-page-conferences

# 3. Travailler, committer petit et souvent
git add .
git commit -m "feat(conferences): ajoute la liste des événements"

# 4. Pousser et ouvrir la PR
git push -u origin feat/12-page-conferences
gh pr create --fill
```

## Nommage des branches

Format : `<type>/<n°-issue>-<description-courte>`

| Type | Usage | Exemple |
|---|---|---|
| `feat` | Nouvelle page / fonctionnalité | `feat/3-page-vulgarisation` |
| `fix` | Correction de bug | `fix/15-menu-mobile-ios` |
| `style` | Charte, CSS sans changement de contenu | `style/8-tokens-couleurs` |
| `content` | Textes, images | `content/20-bio-equipe` |
| `docs` | README, CONTRIBUTING… | `docs/2-guide-contrib` |
| `chore` | Outillage, config | `chore/5-editorconfig` |

## Messages de commit

Convention [Conventional Commits](https://www.conventionalcommits.org/fr/) :

```
<type>(<portée>): <résumé à l'impératif, en minuscules>
```

Exemples : `feat(accueil): ajoute la section partenaires`, `fix(header): corrige le focus clavier`.

## Pull Requests

- Remplir le **modèle de PR** (checklist incluse).
- Titre = résumé clair, ex. `Page Conférences : liste des événements`.
- Captures **mobile + desktop** pour tout changement visuel.
- Squash & merge, puis **supprimer la branche**.

## Standards de code

- **HTML** sémantique (`header`, `nav`, `main`, `section`, `footer`), un seul `h1` par page.
- **CSS** : uniquement des valeurs issues de `css/tokens.css` (`var(--…)`). Mobile-first (`min-width` en media queries).
- **JS** : vanilla, pas de dépendance sans discussion préalable en issue. Le site doit rester utilisable sans JS.
- **Accessibilité** : contrastes AA, `alt` sur les images, navigation clavier, `:focus-visible` visible.
- **Images** : WebP/AVIF quand possible, `width`/`height` renseignés, `loading="lazy"` sous la ligne de flottaison.

## Avant d'ouvrir la PR

- [ ] Testé à 360 px, 768 px et 1280 px de large
- [ ] Aucune erreur dans la console
- [ ] Navigation clavier OK
- [ ] Aucune valeur de design en dur
