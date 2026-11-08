# Documentation technique - Manic Minelayers

## 1. Vue d'ensemble

Le projet suit le même principe que le TP Puissance 4 : une classe `ManicMinelayers` qui
contient les règles et l'état du jeu, et des classes de joueurs qui lui posent des questions
(« quels sont mes coups possibles ? », « joue ce coup ») sans jamais toucher à ses données.

Tous les attributs sont privés (`self.__nom`). Les autres classes ne peuvent utiliser que les
méthodes publiques. Les méthodes qui renvoient des données du plateau renvoient des **copies**
(par exemple `grille()`), jamais l'objet interne.

Chaque joueur (`Human`, `StupidBot`, `MinMax`, `Glouton`, `MCTS`) reçoit une instance de
`ManicMinelayers` dans son constructeur et possède deux méthodes :

- `proposer_coup()` : renvoie un coup `(ligne, colonne)` **sans le jouer**
- `nom()` : renvoie son nom (pour l'affichage et les statistiques)

C'est `Partie` qui joue ensuite le coup.

Un coup est toujours un tuple `(ligne, colonne)`. Au début de la partie, c'est la case où on
pose son pion ; ensuite c'est la case d'arrivée du pion.

## 2. Structures de données

| Donnée                              | Structure                                                                                             | Où                |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------- |
| Plateau                             | liste de listes d'entiers, `plateau[ligne][colonne]`                                                  | `ManicMinelayers` |
| Contenu d'une case                  | `VIDE = 0`, `MARQUE = -1`, `1` ou `2` (pion du joueur)                                                | `constantes.py`   |
| Positions des pions                 | liste `[None, pos1, pos2]` (l'indice est le numéro du joueur), `None` tant que le pion n'est pas posé | `ManicMinelayers` |
| Historique des coups                | liste de tuples `(joueur, ancienne_position, nouvelle_position)`, utilisée comme une pile             | `ManicMinelayers` |
| Coups possibles                     | liste de tuples `(ligne, colonne)`                                                                    | partout           |
| Sauts du cavalier                   | tuple des 8 déplacements `(dl, dc)`                                                                   | `constantes.py`   |
| Arbre de recherche MCTS             | objets `Sommet` qui contiennent la liste de leurs enfants et un lien vers leur parent                 | `sommet.py`       |
| Cases déjà atteintes (heuristiques) | listes de cases                                                                                       | `minmax.py`       |

Le plateau est une simple liste de listes car il est petit (5x10 par défaut). On peut ainsi
retrouver n'importe quelle case en une opération.

### Annuler un coup

`appliquer()` empile `(joueur, ancienne_position, nouvelle_position)` et `retirer_dernier()`
dépile : la nouvelle case redevient `VIDE`, l'ancienne case reprend le numéro du joueur (elle
était `MARQUE`), le pion revient en arrière et la main repasse au joueur. Cela évite de copier
le plateau à chaque coup dans MinMax et dans Glouton : on joue, on évalue, on annule.

MCTS a besoin de garder plusieurs positions en même temps (une par sommet), il utilise donc
`cloner()` qui copie le plateau, les pions, l'historique, le trait et le vainqueur.

## 3. Les classes

### `ManicMinelayers` (manic_minelayers.py) - le moteur

Attributs (tous privés) :

- `__lignes`, `__colonnes` : dimensions
- `__plateau` : la liste de listes
- `__pions` : positions des deux pions
- `__trait` : numéro du joueur qui doit jouer (1 ou 2)
- `__historique` : pile des coups joués
- `__vainqueur` : `None` si la partie continue, `1` ou `2` pour le gagnant, `0` pour un nul

Méthodes publiques :

- `nb_lignes()`, `nb_colonnes()` : dimensions
- `contenu(ligne, colonne)` : contenu d'une case
- `grille()` : copie du plateau
- `pion(joueur)` : position du pion d'un joueur (ou `None`)
- `trait()` : joueur qui doit jouer
- `autre(joueur)` : l'adversaire
- `phase_placement()` : vrai tant qu'un des deux pions n'est pas posé
- `nb_coups_joues()` : taille de l'historique
- `mouvements(joueur=None)` : liste des coups possibles (par défaut du joueur qui a le trait)
- `sauts_depuis(case)` : cases vides atteignables par un saut de cavalier depuis une case
- `est_permis(coup)` : vrai si le coup est possible et que la partie n'est pas finie
- `appliquer(coup)` : joue le coup (erreur `ValueError` s'il est interdit)
- `retirer_dernier()` : annule le dernier coup
- `cloner()` : copie indépendante de la partie
- `terminee()`, `vainqueur()` : état de fin de partie

Méthodes privées : `__placements(joueur)` (cases libres de la première colonne pour le
joueur 1, de la dernière pour le joueur 2) et `__verifier_fin(joueur)`.

**Fin de partie.** Après le coup d'un joueur, `__verifier_fin` regarde si l'adversaire a
encore un coup. Si oui, on continue. Sinon : si le joueur peut encore bouger, il gagne ; si
lui non plus ne peut pas, c'est un match nul.

### `Interface` (interface.py) - la fenêtre Tkinter

Attributs : `__jeu`, `__cote` (taille d'une case en pixels), `__racine` (fenêtre), `__bandeau`
(texte au-dessus), `__toile` (canvas), `__dernier_clic`, `__clic_attendu`, `__ferme`,
`__dernier_coup`, `__reveil` (variable Tkinter servant à bloquer le programme).

Méthodes : `dessiner(cibles)` (redessine le plateau en surlignant les cases de `cibles`),
`message(texte)`, `attendre_case()` (bloque jusqu'à un clic), `temporiser(ms)` (pause entre
les coups), `memoriser_dernier_coup(case)`, `garder_ouverte()`.

`attendre_case` et `temporiser` utilisent `wait_variable` : le programme s'arrête jusqu'à ce
que le clic ou le délai fasse changer la variable `__reveil`. Si on ferme la fenêtre pendant
ce temps, le programme s'arrête proprement.

### `Partie` (partie.py)

Attributs : `__jeu`, `__joueurs` (liste `[None, joueur1, joueur2]`), `__interface` (peut être
`None` pour les concours), `__verbeux` (affichage dans le terminal).

Méthode `lancer()` : tant que la partie n'est pas finie, elle demande son coup au joueur qui
a le trait, le joue avec `appliquer`, redessine, fait une pause, puis renvoie le vainqueur.

### `Human` (human.py)

Attributs : `__jeu`, `__numero`, `__interface`. `proposer_coup()` surligne les coups
possibles, attend un clic et recommence tant que la case cliquée n'est pas un coup possible.

### `StupidBot` (stupid_bot.py)

Attributs : `__jeu`, `__numero`. `proposer_coup()` renvoie `random.choice` des coups possibles.

### `MinMax` (minmax.py), `Glouton` (glouton.py), `Sommet` (sommet.py), `MCTS` (mcts.py)

Voir les parties 4 à 6.

### `Concours` (concours.py)

Attributs : `__parties`, `__lignes`, `__colonnes`, `__resultats` (liste de dictionnaires, un
par duel). Méthodes : `duel(config_a, config_b)`, `tournoi(configs)` (tous contre tous),
`afficher()`. Un joueur est décrit par `(nom, parametres)`, par exemple
`("minmax", {"profondeur": 4, "heuristique": 2})`. Dans un duel, le joueur A commence les
parties paires et B les parties impaires, ce qui permet de comparer les victoires en
commençant et en jouant second. Aucune fenêtre n'est ouverte.

### `fabrique.py`

Fonction `creer_joueur(nom, jeu, numero, interface, **parametres)` qui crée le bon joueur.
Elle est utilisée par `main.py` et par `Concours`.

## 4. MinMax avec élagage alpha-bêta

Attributs : `__jeu`, `__numero`, `__profondeur` (4 par défaut), `__heuristique` (1 ou 2).

**Principe.** Le joueur essaie chacun de ses coups, puis chaque réponse de l'adversaire, etc.
jusqu'à la profondeur maximale. Il suppose que l'adversaire joue toujours le meilleur coup
pour lui. À la profondeur maximale, on note la position avec l'heuristique.

**Négamax.** Pour avoir une seule fonction au lieu de deux (max et min), `__negamax` renvoie
toujours la valeur de la position du point de vue du joueur qui a le trait. Quand on passe au
niveau suivant, on change le signe : ce qui est bon pour l'adversaire est mauvais pour nous.
`valeur = -__negamax(reste - 1, -beta, -alpha, adversaire)`.

**Élagage alpha-bêta.** `alpha` est la meilleure valeur déjà garantie pour le joueur courant et
`beta` celle que l'adversaire peut déjà obtenir. Dès que `alpha >= beta`, la suite des coups
de ce niveau ne peut plus changer le résultat : on arrête (`break`). Le résultat est le même
que MinMax sans élagage mais avec beaucoup moins de positions examinées.

**Positions terminales.** Si la partie est finie, la valeur est `GAIN + reste` (1000 + le
nombre de niveaux restants) pour une victoire, `0` pour un nul, `PERTE - reste` (-1000 - reste)
pour une défaite. Le `reste` fait préférer les victoires rapides et les défaites lointaines.

**Choix à la racine.** `proposer_coup` évalue chaque coup possible, garde les coups qui ont
le meilleur score et en tire un au hasard parmi les égalitézs.

**Pendant le placement** (un des pions n'est pas posé), les heuristiques renvoient 0 car il
n'y a rien à comparer : le choix de la ligne de départ vient de la recherche en profondeur.

### Heuristique 1 : mobilité

Idée : plus un joueur a de possibilités de déplacement, mieux il est placé.

Pour chaque joueur, on calcule :

- `a` = nombre de cases libres atteignables en **1 saut** (ses coups possibles)
- `b` = nombre de cases libres atteignables en **1 ou 2 sauts** (sans compter deux fois la
  même case)

La note est `3 * (a_moi - a_adversaire) + (b_moi - b_adversaire)`.

Le premier terme compte plus car les coups immédiats sont ceux qui peuvent être pris ou
bloqués tout de suite. Le deuxième terme évite de se retrouver dans une zone où l'on a des
coups mais qui mène dans un cul-de-sac.

### Heuristique 2 : territoire

Idée : ce qui compte à la fin est de savoir qui a le plus de cases à lui, car celui qui
manque de cases se retrouve bloqué en premier.

On fait avancer les deux pions en même temps, **un saut à la fois** (un parcours en largeur).
À chaque étape, chaque pion « prend » les cases libres qu'il peut atteindre et que personne
n'a prises avant. On continue jusqu'à ce qu'aucun des deux ne puisse plus avancer. La note est
`cases_prises_par_moi - cases_prises_par_adversaire`.

Si une case est à la même distance des deux pions, elle va au joueur qui a le trait, car il
y arrive le premier. Dans le code, `__territoire` fait avancer les deux fronts et `__etendre`
calcule les nouvelles cases d'un front en ajoutant les cases prises dans la liste `pris`.

### Différence entre les deux heuristiques

L'heuristique 1 regarde seulement autour des pions (voisinage à 2 sauts), alors que la 2
regarde **tout le plateau** et la façon dont les deux pions se partagent l'espace. Dans les
résultats du concours, la 2 est meilleure (52 victoires contre 15 dans le duel direct).

## 5. Tactique de la sous-partie 2.7 : Glouton

Attributs : `__jeu`, `__numero`.

**Principe.** On étudie seulement la position **juste après** chaque coup possible, sans
regarder les coups suivants de l'adversaire. Contrairement à MinMax, il n'y a pas
d'arborescence. Pour chaque coup possible :

1. on joue le coup (`appliquer`)
2. on note la position obtenue (`__noter_position`)
3. on annule le coup (`retirer_dernier`)

On garde le coup de meilleure note (au hasard s'il y en a plusieurs).

**Note d'une position :**

- partie gagnée : `GAIN` (1000) ; nulle : `NUL` (0) ; perdue : `PERTE` (-1000)
- pendant le placement (l'adversaire n'a pas encore de pion) : le nombre de sorties de mon pion
- sinon : `3 * (mes_sorties - sorties_adverses) + sorties_non_bouchees`

Ici `mes_sorties` est le nombre de cases où je pourrai aller au prochain tour et
`sorties_adverses` celui de l'adversaire. Une sortie « non bouchée » est une de mes sorties
depuis laquelle je pourrais encore repartir (elle a au moins une case libre autour). Cela
évite de choisir un coup qui nous met dans un cul-de-sac.

Comme le coup est joué avant d'être noté, un coup qui va sur une case où l'adversaire voulait
aller diminue directement `sorties_adverses` : le Glouton « vole » les cases de l'adversaire.

Cette tactique est très rapide (environ 8 positions à noter par coup) et elle bat nettement le
joueur au hasard (80 victoires sur 100), mais elle perd contre MinMax et MCTS car elle ne voit
pas les pièges à plus d'un coup.

## 6. MCTS (Monte Carlo Tree Search)

### `Sommet` (sommet.py)

Un sommet représente une position de la partie. La définition est récursive : un sommet a un
parent et une liste d'enfants qui sont aussi des sommets.

Attributs :

- `__jeu` : sa propre copie de la partie, après le coup qui mène à ce sommet
- `__coup` : ce coup (`None` pour la racine)
- `__parent`, `__enfants`
- `__visites` : nombre de fois où une simulation est passée par ce sommet
- `__gains` : total des gains (1 par victoire, 0,5 par nul, 0 par défaite)
- `__auteur` : joueur qui a joué le coup menant au sommet. Les gains sont comptés de son
  point de vue
- `__a_essayer` : liste (mélangée) des coups pas encore transformés en enfants

Méthodes : `coup()`, `parent()`, `enfants()`, `auteur()`, `visites()`, `taux_de_gain()`
(gains / visites), `partie()` (copie de la position), `est_terminal()`, `est_plein()` (tous
les coups ont un enfant), et les trois méthodes des étapes de l'algorithme :

- `descendre(exploration)` : sélection, **récursive**
- `etendre()` : expansion, crée un enfant avec un coup de `__a_essayer`
- `remonter(vainqueur)` : rétropropagation, **récursive**, remonte jusqu'à la racine

### `MCTS` (mcts.py)

Attributs : `__jeu`, `__numero`, `__exploration` (la température C, 1,4 par défaut),
`__iterations` (1000 par défaut), `__politique` (`"aleatoire"` ou `"glouton"`).

`proposer_coup()` crée une racine à partir de la position actuelle puis répète `iterations`
fois les 4 étapes :

1. **Sélection** : à partir de la racine, tant que le sommet est complètement développé (tous
   ses coups ont un enfant) et non terminal, on descend vers l'enfant qui maximise UCB1 :

   `UCB1 = taux_de_gain + C * racine( ln(visites du parent) / visites de l'enfant )`

   Le premier terme favorise les coups qui gagnent souvent (exploitation), le second les coups
   peu essayés (exploration). `C` règle l'équilibre : plus il est grand, plus on explore.

2. **Expansion** : on crée un enfant pour un coup pas encore essayé (sauf si le sommet est
   terminal).
3. **Simulation** : on joue la partie jusqu'à la fin sur une copie. Avec la politique
   aléatoire, chaque joueur joue un coup au hasard. Avec la politique gloutonne (bonus), chacun
   joue le coup du `Glouton`.
4. **Rétropropagation** : on remonte du nouveau sommet jusqu'à la racine en ajoutant une
   visite et le résultat (1 si le joueur du sommet a gagné, 0,5 pour un nul, 0 sinon).

À la fin, on joue le coup de l'enfant de la racine **le plus visité** (plus fiable que le meilleur
taux de gain, qui peut venir de très peu de simulations). S'il n'y a qu'un seul coup possible,
on le joue directement sans chercher.

Les sommets travaillent sur des copies de la partie : `proposer_coup` ne modifie donc jamais
la vraie partie.

## 7. Résultats et choix de paramètres

Les statistiques de 100 parties par duel sont dans le `README.md`. Les paramètres utilisés :
MinMax en profondeur 4, MCTS avec 300 itérations et C = 1,4.

## 8. Tests

`python test_jeu.py` vérifie les règles, le match nul, que `appliquer` puis `retirer_dernier`
redonne exactement la position précédente, que `grille()` renvoie bien une copie, le
fonctionnement de `Sommet`, que chaque joueur propose un coup licite sans modifier la partie
et que `Concours` compte bien toutes les parties.
