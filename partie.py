from constantes import DELAI_COUP_MS, MARQUE, VIDE


class Partie:
    # Fait jouer deux joueurs à tour de rôle avec ou sans fenêtre.

    def __init__(self, jeu, joueur1, joueur2, interface=None, verbeux=False):
        self.__jeu = jeu
        # indice = numéro du joueur
        self.__joueurs = [None, joueur1, joueur2]
        self.__interface = interface
        self.__verbeux = verbeux

    def lancer(self):
        # joue jusqu'à la fin et renvoie 1, 2 ou 0 (nul)
        self.__montrer()
        while not self.__jeu.terminee():
            numero = self.__jeu.trait()
            joueur = self.__joueurs[numero]
            self.__annoncer(joueur.nom() + " (joueur " + str(numero) + ") réfléchit...")
            coup = joueur.proposer_coup()
            self.__jeu.appliquer(coup)
            if self.__interface is not None:
                self.__interface.memoriser_dernier_coup(coup)
            self.__montrer()
            self.__annoncer(joueur.nom() + " (joueur " + str(numero) + ") joue " + str(coup))
            if self.__interface is not None:
                self.__interface.temporiser(DELAI_COUP_MS)
        self.__annoncer(self.__bilan())
        return self.__jeu.vainqueur()

    def __bilan(self):
        gagnant = self.__jeu.vainqueur()
        if gagnant == 0:
            return "Match nul"
        return "Victoire de " + self.__joueurs[gagnant].nom() + " (joueur " + str(gagnant) + ")"

    def __annoncer(self, texte):
        if self.__interface is not None:
            self.__interface.message(texte)
        if self.__verbeux:
            print(texte)

    def __montrer(self):
        if self.__interface is not None:
            self.__interface.dessiner()
        if self.__verbeux:
            for ligne in self.__jeu.grille():
                texte = ""
                for case in ligne:
                    if case == VIDE:
                        texte += ". "
                    elif case == MARQUE:
                        texte += "x "
                    else:
                        texte += str(case) + " "
                print(texte)
            print()
