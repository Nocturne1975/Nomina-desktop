
# Nomina-desktop — Electron + React (Vite)

Application desktop basée sur **Electron** avec une UI **React/TSX** (bundlée par **Vite**).

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

- **UI** : React 18 + TypeScript (TSX)
- **Dev server / build** : Vite
- **Desktop shell** : Electron
- **Styles** : Tailwind CSS (voir `web/styles/globals.css`)

---

## Installation & lancement

### Prérequis

- Node.js (LTS recommandé)

### Dev (UI web)

```bash
npm install
npm run dev
```

### Dev (Electron)

1) Démarrer Vite : `npm run dev`

2) Dans un autre terminal :

```bash
npm run electron:dev
```

### Dev (1 commande)

Lance Vite + Electron ensemble :

```bash
npm run app:dev
```

### Build

```bash
npm run build
npm run electron
```

---

## Structure du projet

- `electron/` : process principal Electron (fenêtre, chargement dev/prod)
- `web/` : UI React (TSX)
- `assets/` : ressources (images, icônes, etc.)

---

## Contribution & contact

- Pour contribuer : crée une issue ou une pull request sur le dépôt GitHub.
- Pour retours : soniacorbin4@gmail.com

> Nomina-desktop est un projet en cours. Contributions, idées et retours sont les bienvenus — ouvre une issue ou contacte-moi directement.

---

## Licence

MIT License — voir fichier LICENSE.
