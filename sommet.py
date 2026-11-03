from __future__ import annotations

import math
import random

from manic_minelayers import ManicMinelayers


# Sommet de l'arbre de recherche de MCTS : une position, ses enfants et ses statistiques.
# Les récompenses sont comptées pour le joueur qui a joué le coup menant à ce sommet.
class Sommet:
    def __init__(self, jeu: ManicMinelayers, coup: tuple[int, int] | None = None,
                 parent: Sommet | None = None) -> None:
        #Le sommet garde sa propre copie de la partie, puis y joue le coup.
        self.__jeu = jeu.copier()
        self.__coup = coup
        self.__parent = parent
        self.__enfants = []
        self.__nb_visites = 0
        self.__total_recompenses = 0.0

        if coup is None:
            self.__joueur = self.__jeu.get_adversaire(self.__jeu.get_joueur_courant())
        else:
            self.__joueur = self.__jeu.get_joueur_courant()
            self.__jeu.jouer(coup)

        if self.__jeu.est_finie():
            self.__coups_non_explores = []
        else:
            self.__coups_non_explores = self.__jeu.coups_possibles()

    def get_coup(self) -> tuple[int, int] | None:
        return self.__coup

    def get_parent(self) -> Sommet | None:
        return self.__parent

    def get_jeu(self) -> ManicMinelayers:
        return self.__jeu.copier()

    def get_joueur(self) -> int:
        return self.__joueur

    def get_enfants(self) -> list[Sommet]:
        return self.__enfants[:]

    def get_nb_visites(self) -> int:
        return self.__nb_visites

    def get_valeur_moyenne(self) -> float:
        #Ratio U(x) / N(x) du cours, 0 si le sommet n'a jamais été visité.
        if self.__nb_visites == 0:
            return 0.0
        return self.__total_recompenses / self.__nb_visites

    def est_terminal(self) -> bool:
        return self.__jeu.est_finie()

    def est_completement_developpe(self) -> bool:
        return len(self.__coups_non_explores) == 0

    def developper(self) -> Sommet:
        #Crée l'enfant d'un coup non exploré choisi au hasard et le renvoie.
        if len(self.__coups_non_explores) == 0:
            raise ValueError("Le sommet est deja completement developpe.")
        indice = random.randrange(len(self.__coups_non_explores))
        coup = self.__coups_non_explores.pop(indice)
        enfant = Sommet(self.__jeu, coup, self)
        self.__enfants.append(enfant)
        return enfant

    def meilleur_enfant(self, temperature: float) -> Sommet:
        #Renvoie l'enfant de score UCB1 maximal, au hasard en cas d'égalité.
        meilleur_score = -math.inf
        meilleurs_enfants = []
        for enfant in self.__enfants:
            score = self.__score_ucb1(enfant, temperature)
            if score > meilleur_score:
                meilleur_score = score
                meilleurs_enfants = [enfant]
            elif score == meilleur_score:
                meilleurs_enfants.append(enfant)
        return random.choice(meilleurs_enfants)

    def mettre_a_jour(self, recompense: float) -> None:
        #Ajoute une visite et la récompense (1 victoire, 0.5 nul, 0 défaite).
        self.__nb_visites += 1
        self.__total_recompenses += recompense

    def __score_ucb1(self, enfant: Sommet, temperature: float) -> float:
        #UCB1(x) = U(x) / N(x) + C * racine(ln(N(parent)) / N(x))
        if enfant.get_nb_visites() == 0:
            return math.inf
        exploitation = enfant.get_valeur_moyenne()
        exploration = math.sqrt(math.log(self.__nb_visites) / enfant.get_nb_visites())
        return exploitation + temperature * exploration