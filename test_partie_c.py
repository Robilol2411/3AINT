# Tests de la partie C (Glouton, Sommet, MCTS) : python test_partie_c.py
# Utilise le vrai moteur de A s'il est présent, sinon le dossier bouchons_pour_tester.

import os
import sys
import time

if not os.path.exists(os.path.join(os.path.dirname(__file__), "manic_minelayers.py")):
    sys.path.append(os.path.join(os.path.dirname(__file__), "bouchons_pour_tester"))

from glouton import Glouton
from manic_minelayers import ManicMinelayers
from mcts import MCTS
from sommet import Sommet
from stupid_bot import StupidBot


def jouer_partie(classe1, params1: dict, classe2, params2: dict,
                 taille: tuple[int, int] = (5, 10)) -> int:
    #Joue une partie sans affichage et vérifie chaque coup, renvoie le gagnant.
    jeu = ManicMinelayers(*taille)
    joueurs = [None, classe1(jeu, 1, **params1), classe2(jeu, 2, **params2)]
    while not jeu.est_finie():
        plateau_avant = jeu.get_plateau()
        coup = joueurs[jeu.get_joueur_courant()].choisir_coup()
        assert jeu.get_plateau() == plateau_avant, "choisir_coup() a modifie le plateau"
        assert jeu.est_licite(coup), f"coup illegal {coup}"
        jeu.jouer(coup)
    return jeu.get_gagnant()


def test_sommet() -> None:
    #Vérifie le développement, la mise à jour et le choix UCB1 d'un sommet.
    jeu = ManicMinelayers()
    racine = Sommet(jeu)
    nb_coups = len(jeu.coups_possibles())
    enfants = [racine.developper() for _ in range(nb_coups)]
    assert racine.est_completement_developpe()
    assert len(racine.get_enfants()) == nb_coups
    assert jeu.get_plateau() == ManicMinelayers().get_plateau(), "le jeu d'origine a change"
    for i, enfant in enumerate(enfants):
        assert enfant.get_joueur() == 1 and enfant.get_parent() is racine
        enfant.mettre_a_jour(1.0 if i == 0 else 0.0)
        racine.mettre_a_jour(0.0)
    assert racine.meilleur_enfant(0) is enfants[0]
    assert enfants[0].get_valeur_moyenne() == 1.0
    print("Sommet : OK")


def serie(nom: str, classe1, params1: dict, classe2, params2: dict, nb: int) -> None:
    #Joue nb parties entre deux joueurs et affiche le bilan.
    resultats = [0, 0, 0]
    debut = time.perf_counter()
    for _ in range(nb):
        gagnant = jouer_partie(classe1, params1, classe2, params2)
        resultats[{1: 0, 2: 1, 0: 2}[gagnant]] += 1
    duree = time.perf_counter() - debut
    print(f"{nom:<40} J1 {resultats[0]:>3}  J2 {resultats[1]:>3}  nuls {resultats[2]:>3}"
          f"  ({duree:.1f} s)")


if __name__ == "__main__":
    test_sommet()
    serie("Glouton vs StupidBot", Glouton, {}, StupidBot, {}, 100)
    serie("StupidBot vs Glouton", StupidBot, {}, Glouton, {}, 100)
    serie("MCTS 300 it vs StupidBot", MCTS, {"iterations_max": 300}, StupidBot, {}, 20)
    serie("StupidBot vs MCTS 300 it", StupidBot, {}, MCTS, {"iterations_max": 300}, 20)
    serie("MCTS 300 it vs Glouton", MCTS, {"iterations_max": 300}, Glouton, {}, 20)
    serie("Glouton vs MCTS 300 it", Glouton, {}, MCTS, {"iterations_max": 300}, 20)
    serie("MCTS 0.2 s vs Glouton", MCTS, {"iterations_max": None, "temps_max": 0.2},
          Glouton, {}, 10)
    serie("MCTS gloutonne 100 it vs MCTS 300 it", MCTS,
          {"iterations_max": 100, "politique": "gloutonne"},
          MCTS, {"iterations_max": 300}, 10)