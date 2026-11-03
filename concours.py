
import time

from manic_minelayers import ManicMinelayers
from partie import Partie


class Concours:
    

    def __init__(self, nb_parties: int = 100, taille: tuple[int, int] = (5, 10)) -> None:
        
        self.__nb_parties = nb_parties
        self.__taille = taille
        self.__historique = []

    def affronter(self, config_j1: tuple, config_j2: tuple) -> list[int]:
        
        debut = time.perf_counter()
        resultats = [0, 0, 0]

        for _ in range(self.__nb_parties):
            gagnant = self.__jouer_une_partie(config_j1, config_j2)
            if gagnant == 1:
                resultats[0] += 1
            elif gagnant == 2:
                resultats[1] += 1
            else:
                resultats[2] += 1

        duree = time.perf_counter() - debut
        self.__enregistrer(config_j1, config_j2, resultats, duree)
        return resultats

    def affronter_alterne(self, config_a: tuple, config_b: tuple) -> list[int]:
        
        moitie = self.__nb_parties // 2
        debut = time.perf_counter()
        resultats = [0, 0, 0]

        # Première moitié : A est le joueur 1.
        for _ in range(moitie):
            gagnant = self.__jouer_une_partie(config_a, config_b)
            if gagnant == 1:
                resultats[0] += 1
            elif gagnant == 2:
                resultats[1] += 1
            else:
                resultats[2] += 1

        # Seconde moitié : B est le joueur 1, on inverse donc les compteurs.
        for _ in range(self.__nb_parties - moitie):
            gagnant = self.__jouer_une_partie(config_b, config_a)
            if gagnant == 1:
                resultats[1] += 1
            elif gagnant == 2:
                resultats[0] += 1
            else:
                resultats[2] += 1

        duree = time.perf_counter() - debut
        self.__enregistrer(config_a, config_b, resultats, duree)
        return resultats

    def tableau_resultats(self) -> None:
        
        for affiche in self.__historique:
            total = affiche["victoires_j1"] + affiche["victoires_j2"] + affiche["nuls"]
            if total == 0:
                continue

            pourcent_j1 = 100 * affiche["victoires_j1"] / total
            pourcent_j2 = 100 * affiche["victoires_j2"] / total
            pourcent_nuls = 100 * affiche["nuls"] / total

            print(f"{affiche['nom_j1']} contre {affiche['nom_j2']}")
            print(f"  parties jouées : {total}")
            print(f"  victoires {affiche['nom_j1']} : {pourcent_j1:.1f} %")
            print(f"  victoires {affiche['nom_j2']} : {pourcent_j2:.1f} %")
            print(f"  nuls : {pourcent_nuls:.1f} %")
            print(f"  temps moyen par partie : {affiche['temps_moyen']:.4f} s")
            print()

    def __jouer_une_partie(self, config_j1: tuple, config_j2: tuple) -> int:
        # Joue une partie complète sur un plateau neuf et renvoie le gagnant.
        m, n = self.__taille
        jeu = ManicMinelayers(m, n)
        joueur1 = self.__creer_joueur(config_j1, jeu, 1)
        joueur2 = self.__creer_joueur(config_j2, jeu, 2)
        partie = Partie(jeu, joueur1, joueur2)
        return partie.lancer()

    def __creer_joueur(self, config: tuple, jeu: ManicMinelayers, numero: int):
        # Crée un joueur à partir de sa configuration (classe, paramètres).
        classe, parametres = config
        return classe(jeu, numero, **parametres)

    def __enregistrer(self, config_j1: tuple, config_j2: tuple, resultats: list[int],
                      duree: float) -> None:
        # Ajoute un affrontement à l'historique pour le tableau final.
        self.__historique.append({
            "nom_j1": self.__nom_du_joueur(config_j1, 1),
            "nom_j2": self.__nom_du_joueur(config_j2, 2),
            "victoires_j1": resultats[0],
            "victoires_j2": resultats[1],
            "nuls": resultats[2],
            "temps_moyen": duree / self.__nb_parties,
        })

    def __nom_du_joueur(self, config: tuple, numero: int) -> str:
        # Crée un joueur sur un plateau neuf juste pour lire son nom.
        classe, parametres = config
        jeu = ManicMinelayers(*self.__taille)
        return classe(jeu, numero, **parametres).get_nom()
