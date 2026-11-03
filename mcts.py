import random
import time

from glouton import Glouton
from manic_minelayers import ManicMinelayers
from sommet import Sommet


# Joueur qui choisit son coup par recherche arborescente de Monte Carlo.
# Chaque itération enchaîne sélection, expansion, simulation et rétropropagation.
class MCTS:
    __POLITIQUES = ("aleatoire", "gloutonne")

    def __init__(self, jeu: ManicMinelayers, numero: int, temperature: float = 1.414,
                 iterations_max: int | None = 1000, temps_max: float | None = None,
                 politique: str = "aleatoire") -> None:
        #Il faut au moins une limite, sinon la recherche ne s'arrêterait jamais.
        if iterations_max is None and temps_max is None:
            raise ValueError("Il faut une limite en iterations ou en temps.")
        if politique not in self.__POLITIQUES:
            raise ValueError(f"Politique inconnue : {politique}")
        self.__jeu = jeu
        self.__numero = numero
        self.__temperature = temperature
        self.__iterations_max = iterations_max
        self.__temps_max = temps_max
        self.__politique = politique
        self.__iterations_effectuees = 0

    def get_nom(self) -> str:
        #Par exemple "MCTS c1.414 it1000" ou "MCTS c1.414 t0.5s glouton".
        nom = f"MCTS c{self.__temperature}"
        if self.__iterations_max is not None:
            nom += f" it{self.__iterations_max}"
        if self.__temps_max is not None:
            nom += f" t{self.__temps_max}s"
        if self.__politique == "gloutonne":
            nom += " glouton"
        return nom

    def get_iterations_effectuees(self) -> int:
        return self.__iterations_effectuees

    def choisir_coup(self) -> tuple[int, int]:
        #Renvoie le coup à jouer sans le jouer : l'arbre travaille sur des copies.
        coups = self.__jeu.coups_possibles()
        self.__iterations_effectuees = 0
        if len(coups) == 1:
            return coups[0]

        racine = Sommet(self.__jeu)
        debut = time.perf_counter()
        while not self.__limite_atteinte(debut):
            # étape 1
            sommet_selectionne = self.__selection(racine)
            # étape 2
            sommet_ajoute = self.__expansion(sommet_selectionne)
            # étape 3
            gagnant = self.__simulation(sommet_ajoute)
            # étape 4
            self.__retropropagation(sommet_ajoute, gagnant)
            self.__iterations_effectuees += 1

        return self.__meilleur_coup(racine, coups)

    def __limite_atteinte(self, debut: float) -> bool:
        if (self.__iterations_max is not None
                and self.__iterations_effectuees >= self.__iterations_max):
            return True
        if self.__temps_max is not None and time.perf_counter() - debut >= self.__temps_max:
            return True
        return False

    def __selection(self, racine: Sommet) -> Sommet:
        #On descend par UCB1 tant que le sommet est complètement développé.
        sommet = racine
        while not sommet.est_terminal() and sommet.est_completement_developpe():
            sommet = sommet.meilleur_enfant(self.__temperature)
        return sommet

    def __expansion(self, sommet: Sommet) -> Sommet:
        if sommet.est_terminal():
            return sommet
        return sommet.developper()

    def __simulation(self, sommet: Sommet) -> int:
        #Joue la partie jusqu'au bout sur une copie et renvoie le gagnant (1, 2 ou 0).
        jeu_simule = sommet.get_jeu()
        if self.__politique == "gloutonne":
            gloutons = [None, Glouton(jeu_simule, 1), Glouton(jeu_simule, 2)]
            while not jeu_simule.est_finie():
                joueur = jeu_simule.get_joueur_courant()
                jeu_simule.jouer(gloutons[joueur].choisir_coup())
        else:
            while not jeu_simule.est_finie():
                jeu_simule.jouer(random.choice(jeu_simule.coups_possibles()))
        return jeu_simule.get_gagnant()

    def __retropropagation(self, sommet: Sommet, gagnant: int) -> None:
        #Remonte jusqu'à la racine : 1 si le joueur du sommet a gagné, 0.5 si nul, 0 sinon.
        courant = sommet
        while courant is not None:
            if gagnant == courant.get_joueur():
                courant.mettre_a_jour(1.0)
            elif gagnant == 0:
                courant.mettre_a_jour(0.5)
            else:
                courant.mettre_a_jour(0.0)
            courant = courant.get_parent()

    def __meilleur_coup(self, racine: Sommet, coups: list[tuple[int, int]]) -> tuple[int, int]:
        #Coup de l'enfant le plus visité, au hasard en cas d'égalité.
        enfants = racine.get_enfants()
        if len(enfants) == 0:
            return random.choice(coups)
        visites_max = -1
        meilleurs_coups = []
        for enfant in enfants:
            if enfant.get_nb_visites() > visites_max:
                visites_max = enfant.get_nb_visites()
                meilleurs_coups = [enfant.get_coup()]
            elif enfant.get_nb_visites() == visites_max:
                meilleurs_coups.append(enfant.get_coup())
        return random.choice(meilleurs_coups)