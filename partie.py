from constantes import MARQUE, PAUSE_ENTRE_COUPS, VIDE
from interface import Interface
from manic_minelayers import ManicMinelayers


class Partie:
    def __init__(self, jeu: ManicMinelayers, joueur1, joueur2,
                 interface: Interface | None = None, console: bool = False) -> None:
        self.__jeu = jeu
        # indice = numero du joueur, comme dans le moteur
        self.__joueurs = [None, joueur1, joueur2]
        self.__interface = interface
        self.__console = console

    def lancer(self) -> int:
        #Joue la partie jusqu'au bout et renvoie le gagnant (1, 2 ou 0 pour un nul).
        self.__afficher_plateau()
        while not self.__jeu.est_finie():
            numero = self.__jeu.get_joueur_courant()
            joueur = self.__joueurs[numero]
            self.__afficher_texte(f"Tour de {joueur.get_nom()} (joueur {numero})")

            coup = joueur.choisir_coup()
            self.__jeu.jouer(coup)

            self.__afficher_plateau()
            self.__afficher_texte(f"{joueur.get_nom()} (joueur {numero}) joue {coup}")
            if self.__interface is not None:
                self.__interface.pause(PAUSE_ENTRE_COUPS)

        self.__afficher_texte(self.__texte_resultat())
        return self.__jeu.get_gagnant()

    def __texte_resultat(self) -> str:
        #Renvoie la phrase de fin de partie.
        gagnant = self.__jeu.get_gagnant()
        if gagnant == 0:
            return "Match nul"
        return f"Victoire de {self.__joueurs[gagnant].get_nom()} (joueur {gagnant})"

    def __afficher_texte(self, texte: str) -> None:
        #Affiche un message dans la fenêtre et dans le terminal
        if self.__interface is not None:
            self.__interface.afficher_message(texte)
        if self.__console:
            print(texte)

    def __afficher_plateau(self) -> None:
        #Affiche le plateau dans la fenêtre et dans le terminal
        if self.__interface is not None:
            self.__interface.afficher()
        if self.__console:
            self.__afficher_plateau_console()

    def __afficher_plateau_console(self) -> None:
        #Ecrit le plateau dans le terminal : . vide, x marque, 1 et 2 les pions.
        plateau = self.__jeu.get_plateau()
        for ligne in plateau:
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
