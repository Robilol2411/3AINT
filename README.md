# Projet 3AINT - Manic Minelayers

Jeu à deux joueurs sur un plateau de 5 lignes et 10 colonnes. Chaque joueur a un pion qui
se déplace comme un cavalier aux échecs. Quand un pion quitte une case, il y laisse une marque
et plus personne ne peut aller dessus. Si on bloque l'adversaire alors qu'on peut encore
bouger, on gagne. Si les deux sont bloqués, c'est un match nul.

Le projet est fait en Python avec Tkinter pour l'affichage.

## Lancer le programme

```
python main.py
```

Un menu s'affiche dans le terminal :
- **1** : on joue une partie avec la fenêtre (humain à la souris ou IA contre IA)
- **2** : on lance un concours entre plusieurs IA, sans fenêtre, et on a les statistiques

Pour vérifier que tout marche : `python test_jeu.py`

## Les fichiers

- `constantes.py` : les constantes (taille du plateau, sauts du cavalier, couleurs...)
- `manic_minelayers.py` : la classe qui gère le jeu (plateau, coups possibles, fin de partie)
- `interface.py` : la fenêtre Tkinter
- `partie.py` : fait jouer les deux joueurs chacun leur tour
- `human.py` : le joueur humain (on clique sur une case)
- `stupid_bot.py` : joue au hasard
- `minmax.py` : algorithme MinMax avec élagage alpha-bêta
- `glouton.py` : l'autre tactique, qui regarde seulement le coup suivant
- `sommet.py` et `mcts.py` : l'arbre et l'algorithme de Monte Carlo
- `fabrique.py` : crée un joueur à partir de son nom
- `concours.py` : fait jouer les IA les unes contre les autres et compte les victoires

## Les IA

**StupidBot** : un coup au hasard parmi les coups possibles.

**MinMax** : regarde plusieurs coups à l'avance (profondeur 4 par défaut) et garde le meilleur.
Il y a deux heuristiques pour noter une position quand on arrête de chercher :
1. mobilité : on compare le nombre de cases où chacun peut aller (à 1 saut et à 2 sauts)
2. territoire : on regarde combien de cases chaque pion peut atteindre avant l'autre

**Glouton** : pour chaque coup possible, on le joue, on note le plateau obtenu (nos sorties
moins les sorties de l'adversaire) et on annule. On choisit le meilleur, sans regarder plus loin.

**MCTS** : on fait beaucoup de parties aléatoires pour voir quels coups gagnent le plus souvent.
Le nombre d'itérations et la température (exploration) peuvent être changés. Par défaut les
simulations sont aléatoires, mais on peut mettre la tactique gloutonne à la place (bonus).

## Résultats du concours

100 parties par duel, plateau 5x10, chaque joueur commence une partie sur deux.
MinMax est en profondeur 4 et MCTS fait 300 itérations.

| Duel | Victoires 1er nommé | Victoires 2e nommé | Nuls |
|---|---|---|---|
| StupidBot - Glouton | 12 | 80 | 8 |
| StupidBot - MinMax h1 | 3 | 95 | 2 |
| StupidBot - MinMax h2 | 3 | 94 | 3 |
| StupidBot - MCTS | 2 | 98 | 0 |
| Glouton - MinMax h1 | 12 | 80 | 8 |
| Glouton - MinMax h2 | 2 | 88 | 10 |
| Glouton - MCTS | 3 | 85 | 12 |
| MinMax h1 - MinMax h2 | 15 | 52 | 33 |
| MinMax h1 - MCTS | 19 | 57 | 24 |
| MinMax h2 - MCTS | 52 | 22 | 26 |

Ce qu'on remarque :
- toutes les IA battent très largement le joueur au hasard
- l'heuristique 2 (territoire) est meilleure que l'heuristique 1 (mobilité)
- MCTS bat MinMax avec l'heuristique 1, mais perd contre MinMax avec l'heuristique 2
- le fait de commencer ne change presque rien : dans chaque duel, les victoires en commençant
  et en jouant second sont à peu près égales (par exemple 47 et 48 pour MinMax h1 contre StupidBot)

## Bonus faits

- la tactique gloutonne peut servir de politique de jeu pour MCTS
