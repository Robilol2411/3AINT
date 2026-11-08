import random

from glouton import Glouton
from sommet import Sommet


class MCTS:
    # Recherche arborescente de Monte-Carlo.
    # exploration = température C de UCB1, iterations = nombre de tours de recherche.
    # politique : "aleatoire" ou "glouton" pour les simulations.

    def __init__(self, jeu, numero, exploration=1.4, iterations=1000,
                 politique="aleatoire"):
        if politique != "aleatoire" and politique != "glouton":
            raise ValueError("Politique inconnue : " + politique)
        self.__jeu = jeu
        self.__numero = numero
        self.__exploration = exploration
        self.__iterations = iterations
        self.__politique = politique

    def nom(self):
        texte = "MCTS(C=" + str(self.__exploration) + ", " + str(self.__iterations) + " it)"
        if self.__politique == "glouton":
            texte += "+glouton"
        return texte

    def proposer_coup(self):
        coups = self.__jeu.mouvements(self.__numero)
        if len(coups) == 1:
            return coups[0]

        racine = Sommet(self.__jeu)
        for i in range(self.__iterations):
            feuille = racine.descendre(self.__exploration)      # sélection
            if not feuille.est_terminal():
                feuille = feuille.etendre()                     # expansion
            vainqueur = self.__simuler(feuille)                 # simulation
            feuille.remonter(vainqueur)                         # rétropropagation

        # on garde l'enfant le plus visité
        meilleurs = []
        max_visites = -1
        for enfant in racine.enfants():
            if enfant.visites() > max_visites:
                max_visites = enfant.visites()
                meilleurs = [enfant.coup()]
            elif enfant.visites() == max_visites:
                meilleurs.append(enfant.coup())
        if len(meilleurs) == 0:
            return random.choice(coups)
        return random.choice(meilleurs)

    def __simuler(self, sommet):
        # joue la partie jusqu'au bout sur une copie et renvoie le gagnant
        partie = sommet.partie()
        if self.__politique == "glouton":
            bots = [None, Glouton(partie, 1), Glouton(partie, 2)]
            while not partie.terminee():
                partie.appliquer(bots[partie.trait()].proposer_coup())
        else:
            while not partie.terminee():
                partie.appliquer(random.choice(partie.mouvements()))
        return partie.vainqueur()
