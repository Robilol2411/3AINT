import random

from constantes import GAIN, PERTE


class MinMax:
    # MinMax avec élagage alpha-bêta (écrit en négamax : la valeur d'une position
    # est toujours vue du joueur qui a le trait, et on change le signe à chaque niveau).
    # heuristique 1 = mobilité, heuristique 2 = territoire (cases atteintes en premier).

    def __init__(self, jeu, numero, profondeur=4, heuristique=1):
        if heuristique != 1 and heuristique != 2:
            raise ValueError("L'heuristique doit valoir 1 ou 2")
        self.__jeu = jeu
        self.__numero = numero
        self.__profondeur = profondeur
        self.__heuristique = heuristique

    def nom(self):
        return "MinMax(h" + str(self.__heuristique) + ", p" + str(self.__profondeur) + ")"

    def proposer_coup(self):
        meilleur_score = None
        meilleurs = []
        for coup in self.__jeu.mouvements(self.__numero):
            self.__jeu.appliquer(coup)
            score = -self.__negamax(self.__profondeur - 1, -100000, 100000,
                                    self.__jeu.trait())
            self.__jeu.retirer_dernier()
            if meilleur_score is None or score > meilleur_score:
                meilleur_score = score
                meilleurs = [coup]
            elif score == meilleur_score:
                meilleurs.append(coup)
        return random.choice(meilleurs)

    def __negamax(self, reste, alpha, beta, joueur):
        # valeur de la position pour 'joueur', qui a le trait
        if self.__jeu.terminee():
            gagnant = self.__jeu.vainqueur()
            if gagnant == joueur:
                return GAIN + reste      # victoire rapide = mieux
            if gagnant == 0:
                return 0
            return PERTE - reste         # défaite lointaine = moins mal
        if reste == 0:
            return self.__evaluer(joueur)

        meilleur = -100000
        for coup in self.__jeu.mouvements():
            self.__jeu.appliquer(coup)
            valeur = -self.__negamax(reste - 1, -beta, -alpha, self.__jeu.autre(joueur))
            self.__jeu.retirer_dernier()
            if valeur > meilleur:
                meilleur = valeur
            if meilleur > alpha:
                alpha = meilleur
            if alpha >= beta:
                break   # élagage
        return meilleur

    def __evaluer(self, joueur):
        if self.__jeu.phase_placement():
            return 0
        if self.__heuristique == 2:
            return self.__territoire(joueur)
        return self.__mobilite(joueur)

    def __mobilite(self, joueur):
        # heuristique 1 : mes coups moins ceux de l'adversaire,
        # en comptant aussi les cases à deux sauts
        adversaire = self.__jeu.autre(joueur)
        moi = self.__cases_a_deux_sauts(joueur)
        lui = self.__cases_a_deux_sauts(adversaire)
        return 3 * (moi[0] - lui[0]) + (moi[1] - lui[1])

    def __cases_a_deux_sauts(self, joueur):
        # renvoie (nombre de cases à 1 saut, nombre de cases à 1 ou 2 sauts)
        premieres = self.__jeu.mouvements(joueur)
        toutes = premieres[:]
        for case in premieres:
            for suivante in self.__jeu.sauts_depuis(case):
                if suivante not in toutes:
                    toutes.append(suivante)
        return len(premieres), len(toutes)

    def __territoire(self, joueur):
        # heuristique 2 : les deux pions s'étendent couche par couche ; on compte
        # les cases atteintes en premier par chacun. Le joueur qui a le trait
        # commence, donc il gagne les égalités.
        adversaire = self.__jeu.autre(joueur)
        front_moi = [self.__jeu.pion(joueur)]
        front_lui = [self.__jeu.pion(adversaire)]
        pris = [self.__jeu.pion(joueur), self.__jeu.pion(adversaire)]
        cases_moi = 0
        cases_lui = 0
        while len(front_moi) > 0 or len(front_lui) > 0:
            front_moi = self.__etendre(front_moi, pris)
            cases_moi += len(front_moi)
            front_lui = self.__etendre(front_lui, pris)
            cases_lui += len(front_lui)
        return cases_moi - cases_lui

    def __etendre(self, front, pris):
        # nouvelles cases atteintes en un saut depuis le front (ajoutées à 'pris')
        suivant = []
        for case in front:
            for voisine in self.__jeu.sauts_depuis(case):
                if voisine not in pris:
                    pris.append(voisine)
                    suivant.append(voisine)
        return suivant
