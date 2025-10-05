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
- Flèche haut / `W` : sauter ; ré-appuyez en l'air après avoir ramassé une boule d'énergie pour déclencher un double saut
- Barre d'espace : attaque au corps-à-corps
- `Échap` : quitter la partie
- `R` : recommencer après une défaite (retour au dernier checkpoint atteint)

## Éléments du niveau

- Des boules d'énergie dorées apparaissent sur certaines plateformes : en les ramassant, vous gagnez une charge de double saut. La charge est unique et ne peut pas se cumuler ; une nouvelle boule n'a d'effet que si vous avez dépensé la précédente. Elles réapparaissent automatiquement cinq secondes après leur collecte.
- Un checkpoint situé au milieu du parcours permet de repartir rapidement en cas de défaite en appuyant sur `R`.
- Le héros dispose de trois cœurs visibles en haut de l'écran ; une collision avec un ennemi enlève un cœur. Tomber dans le vide consomme toutes les vies et affiche l'écran de défaite (repartez ensuite du dernier checkpoint atteint en appuyant sur `R`).
- Une aura dorée s'affiche brièvement devant le personnage pour indiquer la zone d'impact de l'attaque.
- La caméra suit automatiquement le personnage au cours de sa progression dans le niveau.

## Personnaliser les sprites

Le moteur charge automatiquement des sprites si vous placez les fichiers suivants dans le dossier `assets/` :

- `hero.png` : sprite du personnage principal ; sans ce fichier un rectangle bleu est affiché.
- `monstre.png` : sprite des ennemis ; sans ce fichier ils restent dessinés en rouge.

Les images sont redimensionnées automatiquement pour correspondre aux hitbox du jeu.
