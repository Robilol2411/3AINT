# Vérifications automatiques : python test_jeu.py
import random

from concours import Concours
from fabrique import creer_joueur
from manic_minelayers import ManicMinelayers
from partie import Partie
from sommet import Sommet


def test_regles():
    jeu = ManicMinelayers(5, 10)
    assert jeu.mouvements(1) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    assert jeu.mouvements(2) == [(0, 9), (1, 9), (2, 9), (3, 9), (4, 9)]
    jeu.appliquer((2, 0))
    jeu.appliquer((2, 9))
    assert sorted(jeu.mouvements(1)) == [(0, 1), (1, 2), (3, 2), (4, 1)]
    jeu.appliquer((0, 1))
    assert jeu.contenu(2, 0) == -1 and jeu.contenu(0, 1) == 1
    assert not jeu.est_permis((2, 0)), "une case marquée est interdite"


def test_nul():
    jeu = ManicMinelayers(1, 2)
    jeu.appliquer((0, 0))
    jeu.appliquer((0, 1))
    assert jeu.terminee() and jeu.vainqueur() == 0


def test_annulation_et_copie():
    jeu = ManicMinelayers(5, 10)
    etats = []
    while not jeu.terminee():
        etats.append((jeu.grille(), jeu.trait()))
        jeu.appliquer(random.choice(jeu.mouvements()))
    copie = jeu.cloner()
    while len(etats) > 0:
        jeu.retirer_dernier()
        grille, trait = etats.pop()
        assert jeu.grille() == grille and jeu.trait() == trait
        assert jeu.vainqueur() is None
    assert copie.terminee()


def test_encapsulation():
    jeu = ManicMinelayers()
    jeu.grille()[0][0] = 99
    assert jeu.contenu(0, 0) == 0


def test_sommet():
    jeu = ManicMinelayers()
    racine = Sommet(jeu)
    n = len(jeu.mouvements())
    for i in range(n):
        racine.etendre()
    assert racine.est_plein() and len(racine.enfants()) == n
    assert jeu.nb_coups_joues() == 0
    racine.enfants()[0].remonter(1)
    assert racine.visites() == 1 and racine.enfants()[0].taux_de_gain() == 1.0


def test_joueurs():
    configs = [("stupid", {}), ("glouton", {}),
               ("minmax", {"profondeur": 3, "heuristique": 1}),
               ("minmax", {"profondeur": 3, "heuristique": 2}),
               ("mcts", {"iterations": 100}),
               ("mcts", {"iterations": 50, "politique": "glouton"})]
    for nom, parametres in configs:
        for i in range(3):
            jeu = ManicMinelayers()
            j1 = creer_joueur(nom, jeu, 1, None, **parametres)
            j2 = creer_joueur("stupid", jeu, 2)
            avant = jeu.grille()
            coup = j1.proposer_coup()
            assert jeu.grille() == avant, "proposer_coup ne doit pas jouer"
            assert jeu.est_permis(coup)
            Partie(jeu, j1, j2).lancer()


def test_concours():
    c = Concours(4)
    r = c.duel(("stupid", {}), ("glouton", {}))
    total = r["a_premier"] + r["a_second"] + r["b_premier"] + r["b_second"] + r["nuls"]
    assert total == 4


for nom_test in list(globals()):
    if nom_test.startswith("test_"):
        globals()[nom_test]()
        print(nom_test, ": OK")
