# Adventure Game

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Lancement du jeu

Exécutez la commande suivante pour démarrer le jeu :

```bash
python -m src.game.main
```

## Contrôles

- Flèche gauche / `A` : déplacement vers la gauche
- Flèche droite / `D` : déplacement vers la droite
- Flèche haut / `W` : sauter (uniquement lorsqu'on est au sol)
- Barre d'espace : attaque au corps-à-corps
- `Échap` : quitter la partie
- `R` : recommencer après une défaite

Le héros dispose de trois cœurs visibles en haut de l'écran ; une collision avec un ennemi enlève un cœur. La caméra suit automatiquement le personnage au cours de sa progression dans le niveau.
