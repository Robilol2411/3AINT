from fabrique import creer_joueur
from manic_minelayers import ManicMinelayers
from partie import Partie


class Concours:
    # Fait s'affronter des joueurs sans affichage et calcule des statistiques.
    # Un joueur est décrit par un tuple (nom, parametres)("minmax", {"profondeur": 3}).
    # Dans un duel chaque joueur commence la moitié des parties.

    def __init__(self, parties=100, lignes=5, colonnes=10):
        self.__parties = parties
        self.__lignes = lignes
        self.__colonnes = colonnes
        self.__resultats = []

    def duel(self, config_a, config_b):
        # compteurs : victoires de A en commençant / en second, pareil pour B, match nuls
        a_premier = 0
        a_second = 0
        b_premier = 0
        b_second = 0
        nuls = 0
        for i in range(self.__parties):
            if i % 2 == 0:
                gagnant = self.__jouer(config_a, config_b)
                if gagnant == 1:
                    a_premier += 1
                elif gagnant == 2:
                    b_second += 1
                else:
                    nuls += 1
            else:
                gagnant = self.__jouer(config_b, config_a)
                if gagnant == 1:
                    b_premier += 1
                elif gagnant == 2:
                    a_second += 1
                else:
                    nuls += 1

        resultat = {"nom_a": self.__nom(config_a), "nom_b": self.__nom(config_b),
                    "a_premier": a_premier, "a_second": a_second,
                    "b_premier": b_premier, "b_second": b_second, "nuls": nuls}
        self.__resultats.append(resultat)
        return resultat

    def tournoi(self, configs):
        # chaque joueur affronte tous les autres
        for i in range(len(configs)):
            for j in range(i + 1, len(configs)):
                self.duel(configs[i], configs[j])

    def afficher(self):
        for r in self.__resultats:
            victoires_a = r["a_premier"] + r["a_second"]
            victoires_b = r["b_premier"] + r["b_second"]
            print()
            print(r["nom_a"], "contre", r["nom_b"], "-", self.__parties, "parties")
            print("  victoires", r["nom_a"], ":", victoires_a,
                  "(dont", r["a_premier"], "en commençant)")
            print("  victoires", r["nom_b"], ":", victoires_b,
                  "(dont", r["b_premier"], "en commençant)")
            print("  nuls :", r["nuls"])

    def __jouer(self, config_1, config_2):
        jeu = ManicMinelayers(self.__lignes, self.__colonnes)
        joueur1 = creer_joueur(config_1[0], jeu, 1, None, **config_1[1])
        joueur2 = creer_joueur(config_2[0], jeu, 2, None, **config_2[1])
        return Partie(jeu, joueur1, joueur2).lancer()

    def __nom(self, config):
        jeu = ManicMinelayers(self.__lignes, self.__colonnes)
        return creer_joueur(config[0], jeu, 1, None, **config[1]).nom()
