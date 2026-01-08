
# Nomina-desktop — Application PyQt6
Présenté par : Sonia Corbin  
Date : 05/11/2025

> Application desktop multiplateforme pour la génération et la narration de noms, réalisée avec Python et PyQt6.

---

## Table des matières

- [Nomina-desktop — Application PyQt6](#nomina-desktop--application-pyqt6)
  - [Table des matières](#table-des-matières)
  - [Présentation](#présentation)
  - [Architecture technique](#architecture-technique)
  - [Installation \& lancement](#installation--lancement)
  - [Structure du projet](#structure-du-projet)
  - [Contribution \& contact](#contribution--contact)
  - [Licence](#licence)

---

## Présentation

Nomina-desktop est une application graphique permettant de générer des noms (personnages, lieux, objets, etc.) et de les enrichir de mini-descriptions narratives. Elle vise les auteurs, MJ, créateurs de jeux ou toute personne en quête d’inspiration.

---

## Architecture technique

- **Langage** : Python 3.10+
- **Framework GUI** : PyQt6
- **UI** : Fichiers .ui (Qt Designer)
- **Styles** : CSS (styles.qss)
- **Organisation** : MVC simplifié (src/, ui/, assets/, styles/)

---

## Installation & lancement

1. Installe Python 3.10 ou plus récent.
2. Clone le dépôt et place-toi dans le dossier :

```bash
git clone <url-du-repo>
cd Nomina-desktop
```

3. Installe les dépendances :

```bash
pip install -r requirements.txt
```

4. Lance l’application :

```bash
python src/main.py
```

---

## Structure du projet

- `src/` : code source principal (main.py, logique, contrôleurs)
- `ui/` : fichiers d’interface graphique générés avec Qt Designer (`nomina_main.ui`)
- `styles/` : fichiers de styles (`styles.qss`, `index.css`)
- `assets/` : images, icônes, ressources graphiques
- `requirements.txt` : dépendances Python

---

## Contribution & contact

- Pour contribuer : crée une issue ou une pull request sur le dépôt GitHub.
- Pour retours : soniacorbin4@gmail.com

> Nomina-desktop est un projet en cours. Contributions, idées et retours sont les bienvenus — ouvre une issue ou contacte-moi directement.

---

## Licence

MIT License — voir fichier LICENSE.
