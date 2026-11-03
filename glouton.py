import math
import random

from constantes import SCORE_DEFAITE, SCORE_NUL, SCORE_VICTOIRE
from manic_minelayers import ManicMinelayers


# Joueur qui choisit le coup menant à la meilleure position immédiate, sans anticiper.
class Glouton:
    __POIDS_PRESSION = 3
    __POIDS_SORTIES_SURES = 2
    __POIDS_CENTRAGE = 1
    __PENALITE_IMPASSE = SCORE_DEFAITE // 2

    def __init__(self, jeu: ManicMinelayers, numero: int) -> None:
        self.__jeu = jeu
        self.__numero = numero

    def get_nom(self) -> str:
        return "Glouton"

    def choisir_coup(self) -> tuple[int, int]:
        #Renvoie le coup de meilleur score, au hasard parmi les ex aequo, sans le jouer.
        meilleur_score = -math.inf
        meilleurs_coups = []
        for coup in self.__jeu.coups_possibles():
            score = self.evaluer_coup(coup)
            if score > meilleur_score:
                meilleur_score = score
                meilleurs_coups = [coup]
            elif score == meilleur_score:
                meilleurs_coups.append(coup)
        return random.choice(meilleurs_coups)

    def evaluer_coup(self, coup: tuple[int, int]) -> float:
        #Joue le coup, note la position obtenue puis annule le coup.
        # On retient le joueur avant jouer(), car ensuite la main passe à l'adversaire.
        joueur = self.__jeu.get_joueur_courant()
        self.__jeu.jouer(coup)
        score = self.__evaluer_position(joueur)
        self.__jeu.annuler()
        return score

    def __evaluer_position(self, joueur: int) -> float:
        #Note la position du point de vue du joueur qui vient de jouer.
        if self.__jeu.est_finie():
            gagnant = self.__jeu.get_gagnant()
            if gagnant == joueur:
                return SCORE_VICTOIRE
            if gagnant == 0:
                return SCORE_NUL
            return SCORE_DEFAITE

        coups_adversaire = self.__jeu.coups_possibles(self.__jeu.get_adversaire(joueur))
        mes_sorties = self.__jeu.coups_possibles(joueur)

        # L'adversaire n'a pas encore posé son pion : on ne juge que ma case.
        if self.__jeu.est_en_placement():
            return (self.__POIDS_SORTIES_SURES * len(mes_sorties)
                    + self.__POIDS_CENTRAGE * self.__centrage(joueur))

        # Je me suis enfermé : je perdrai dès que l'adversaire jouera.
        if len(mes_sorties) == 0:
            return self.__PENALITE_IMPASSE

        # Une sortie que l'adversaire peut atteindre risque de m'être prise.
        cases_adversaire = set(coups_adversaire)
        nb_sorties_sures = 0
        for case in mes_sorties:
            if case not in cases_adversaire:
                nb_sorties_sures += 1

        return (-self.__POIDS_PRESSION * len(coups_adversaire)
                + self.__POIDS_SORTIES_SURES * nb_sorties_sures
                + self.__POIDS_CENTRAGE * self.__centrage(joueur))

    def __centrage(self, joueur: int) -> float:
        #Renvoie 1 au centre du plateau et 0 dans un coin.
        ligne, colonne = self.__jeu.get_position(joueur)
        centre_ligne = (self.__jeu.get_m() - 1) / 2
        centre_colonne = (self.__jeu.get_n() - 1) / 2
        distance = abs(ligne - centre_ligne) + abs(colonne - centre_colonne)
        return 1 - distance / (centre_ligne + centre_colonne)