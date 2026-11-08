import random

from constantes import GAIN, NUL, PERTE


class Glouton:
    # Tactique gloutonne : pour chaque coup possible on joue on note la position obtenue et on l'annule y'a aucune anticipation de plusieurs coups.
    # Note = 3 * (mes sorties - sorties de l'adversaire) + mes sorties non cul-de-sac.

    def __init__(self, jeu, numero):
        self.__jeu = jeu
        self.__numero = numero

    def nom(self):
        return "Glouton"

    def proposer_coup(self):
        meilleure_note = None
        meilleurs = []
        for coup in self.__jeu.mouvements(self.__numero):
            self.__jeu.appliquer(coup)
            note = self.__noter_position()
            self.__jeu.retirer_dernier()
            if meilleure_note is None or note > meilleure_note:
                meilleure_note = note
                meilleurs = [coup]
            elif note == meilleure_note:
                meilleurs.append(coup)
        return random.choice(meilleurs)

    def __noter_position(self):
        moi = self.__numero
        if self.__jeu.terminee():
            gagnant = self.__jeu.vainqueur()
            if gagnant == moi:
                return GAIN
            if gagnant == 0:
                return NUL
            return PERTE

        mes_sorties = self.__jeu.mouvements(moi)
        if self.__jeu.phase_placement():
            # l'adversaire n'a pas encore posé son pion
            return len(mes_sorties)

        ses_sorties = self.__jeu.mouvements(self.__jeu.autre(moi))
        # une sortie est bouchée si on ne pourrait plus repartir de cette case
        non_bouchees = 0
        for case in mes_sorties:
            if len(self.__jeu.sauts_depuis(case)) > 0:
                non_bouchees += 1
        return 3 * (len(mes_sorties) - len(ses_sorties)) + non_bouchees
