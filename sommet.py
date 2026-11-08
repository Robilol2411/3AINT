import math
import random


class Sommet:
    # Un sommet de l'arbre de Monte-Carlo : une position du jeu, ses enfants
    # et ses statistiques (visites et gains du joueur qui a joué le coup menant ici).

    def __init__(self, jeu, coup=None, parent=None):
        self.__jeu = jeu.cloner()
        self.__coup = coup
        self.__parent = parent
        self.__enfants = []
        self.__visites = 0
        self.__gains = 0.0

        if coup is None:
            self.__auteur = self.__jeu.autre(self.__jeu.trait())
        else:
            self.__auteur = self.__jeu.trait()
            self.__jeu.appliquer(coup)

        if self.__jeu.terminee():
            self.__a_essayer = []
        else:
            self.__a_essayer = self.__jeu.mouvements()
            random.shuffle(self.__a_essayer)

    def coup(self):
        return self.__coup

    def parent(self):
        return self.__parent

    def enfants(self):
        return self.__enfants[:]

    def auteur(self):
        return self.__auteur

    def visites(self):
        return self.__visites

    def taux_de_gain(self):
        if self.__visites == 0:
            return 0.0
        return self.__gains / self.__visites

    def partie(self):
        # copie de la position, qu'on peut modifier librement
        return self.__jeu.cloner()

    def est_terminal(self):
        return self.__jeu.terminee()

    def est_plein(self):
        # vrai quand tous les coups possibles ont déjà un enfant
        return len(self.__a_essayer) == 0

    def descendre(self, exploration):
        # sélection (récursive) on descend jusqu'à un sommet à développer
        if self.est_terminal() or not self.est_plein():
            return self
        return self.__meilleur_enfant(exploration).descendre(exploration)

    def etendre(self):
        # expansion crée l'enfant d'un coup pas encore essayé
        coup = self.__a_essayer.pop()
        enfant = Sommet(self.__jeu, coup, self)
        self.__enfants.append(enfant)
        return enfant

    def remonter(self, vainqueur):
        # rétropropagation (récursive) jusqu'à la racine
        self.__visites += 1
        if vainqueur == self.__auteur:
            self.__gains += 1
        elif vainqueur == 0:
            self.__gains += 0.5
        if self.__parent is not None:
            self.__parent.remonter(vainqueur)

    def __meilleur_enfant(self, exploration):
        # UCB1 = gain moyen + C * racine(ln(N parent) / N enfant)
        meilleur_score = -1
        meilleurs = []
        for enfant in self.__enfants:
            score = enfant.taux_de_gain() + exploration * (
                math.log(self.__visites) / enfant.visites()) ** 0.5
            if score > meilleur_score:
                meilleur_score = score
                meilleurs = [enfant]
            elif score == meilleur_score:
                meilleurs.append(enfant)
        return random.choice(meilleurs)
