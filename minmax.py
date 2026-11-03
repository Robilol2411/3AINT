
import random
from collections import deque

from constantes import DEPLACEMENTS_CAVALIER, SCORE_DEFAITE, SCORE_VICTOIRE, VIDE
from manic_minelayers import ManicMinelayers


class MinMax:

    def __init__(self, jeu: ManicMinelayers, numero: int, profondeur: int = 4,
                 heuristique: int = 1) -> None:
       
        self.__jeu = jeu
        self.__numero = numero
        self.__profondeur = profondeur
        self.__heuristique = heuristique

    def choisir_coup(self) -> tuple[int, int]:
        """Cherche le meilleur coup avec l'alpha-bêta, sans le jouer.

        Paramètres : aucun.

        Retour : le coup choisi sous la forme (ligne, colonne).
        """
        meilleurs_coups = []
        meilleur_score = float("-inf")

        for coup in self.__jeu.coups_possibles(self.__numero):
            self.__jeu.jouer(coup)
            # Après mon coup, c'est à l'adversaire de jouer : on minimise.
            score = self.__alphabeta(self.__profondeur - 1, float("-inf"),
                                     float("inf"), False)
            self.__jeu.annuler()

            if score > meilleur_score:
                meilleur_score = score
                meilleurs_coups = [coup]
            elif score == meilleur_score:
                meilleurs_coups.append(coup)

        return random.choice(meilleurs_coups)

    def get_nom(self) -> str:
        """Donne le nom du joueur.

        Paramètres : aucun.

        Retour : le nom, par exemple "MinMax h1 p4".
        """
        return f"MinMax h{self.__heuristique} p{self.__profondeur}"

    def __alphabeta(self, profondeur: int, alpha: float, beta: float,
                    maximiser: bool) -> float:
        # Score de la position avec élagage alpha-bêta (positif = bon pour le bot).
        # alpha = meilleur score du bot, beta = meilleur score de l'adversaire.
        # 1. Partie terminée : on note selon le vainqueur, en favorisant les
        #    victoires rapides et en retardant les défaites.
        if self.__jeu.est_finie():
            gagnant = self.__jeu.get_gagnant()
            if gagnant == self.__numero:
                return SCORE_VICTOIRE + profondeur
            if gagnant == 0 or gagnant is None:
                return 0
            return SCORE_DEFAITE - profondeur

        # 2. Limite de profondeur atteinte : on estime la position.
        if profondeur == 0:
            return self.__evaluer()

        # 3. Sinon on explore tous les coups du joueur courant.
        if maximiser:
            meilleur = float("-inf")
        else:
            meilleur = float("inf")

        for coup in self.__jeu.coups_possibles():
            self.__jeu.jouer(coup)
            score = self.__alphabeta(profondeur - 1, alpha, beta, not maximiser)
            self.__jeu.annuler()

            if maximiser:
                if score > meilleur:
                    meilleur = score
                alpha = max(alpha, meilleur)
            else:
                if score < meilleur:
                    meilleur = score
                beta = min(beta, meilleur)

            # Élagage : la branche ne peut plus changer le résultat.
            if alpha >= beta:
                break

        return meilleur

    def __evaluer(self) -> int:
        # Renvoie le score de la position avec l'heuristique choisie.
        if self.__heuristique == 2:
            return self.__heuristique_2()
        return self.__heuristique_1()

    def __heuristique_1(self) -> int:
        # Heuristique locale : mes coups moins ceux de l'adversaire (0 au placement).
        if self.__jeu.est_en_placement():
            return 0

        adversaire = self.__jeu.get_adversaire(self.__numero)
        mes_coups = self.__jeu.coups_possibles(self.__numero)
        ses_coups = self.__jeu.coups_possibles(adversaire)
        return len(mes_coups) - len(ses_coups)

    def __heuristique_2(self) -> int:
        # Heuristique globale : différence de l'espace atteignable (0 au placement).
        if self.__jeu.est_en_placement():
            return 0

        adversaire = self.__jeu.get_adversaire(self.__numero)
        mon_espace = self.__espace_atteignable(self.__numero)
        son_espace = self.__espace_atteignable(adversaire)
        return mon_espace - son_espace

    def __espace_atteignable(self, joueur: int) -> int:
        # Compte les cases vides atteignables en 3 sauts de cavalier (BFS).
        depart = self.__jeu.get_position(joueur)
        if depart is None:
            return 0

        visites = {depart}
        a_explorer = deque([(depart, 0)])
        atteignables = 0

        while a_explorer:
            (ligne, colonne), sauts = a_explorer.popleft()
            if sauts == 3:
                continue

            for dl, dc in DEPLACEMENTS_CAVALIER:
                nouvelle_ligne = ligne + dl
                nouvelle_colonne = colonne + dc
                if not (0 <= nouvelle_ligne < self.__jeu.get_m()
                        and 0 <= nouvelle_colonne < self.__jeu.get_n()):
                    continue
                if (nouvelle_ligne, nouvelle_colonne) in visites:
                    continue
                if self.__jeu.get_case(nouvelle_ligne, nouvelle_colonne) != VIDE:
                    continue

                visites.add((nouvelle_ligne, nouvelle_colonne))
                atteignables += 1
                a_explorer.append(((nouvelle_ligne, nouvelle_colonne), sauts + 1))

        return atteignables