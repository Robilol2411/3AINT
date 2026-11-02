import tkinter as tk

from constantes import (
    COULEUR_JOUEUR_1,
    COULEUR_JOUEUR_2,
    COULEUR_MARQUE,
    COULEUR_SURLIGNAGE,
    COULEUR_VIDE,
    HAUTEUR_MAX,
    LARGEUR_MAX,
    MARQUE,
)
from manic_minelayers import ManicMinelayers

class Interface:
    def __init__(self, jeu: ManicMinelayers) -> None:
        self.__jeu = jeu
        self.__m = jeu.get_m()
        self.__n = jeu.get_n()
        self.__taille_case = min(LARGEUR_MAX // self.__n, HAUTEUR_MAX // self.__m)
        self.__clic = None
        self.__attend_clic = False
        self.__fermee = False

        self.__fenetre = tk.Tk()
        self.__fenetre.title("Manic Minelayers")
        self.__fenetre.protocol("WM_DELETE_WINDOW", self.__fermer)
        # sert a bloquer le programme dans attendre_clic et pause
        self.__attente = tk.IntVar(self.__fenetre, 0)

        self.__message = tk.Label(self.__fenetre, font=("Arial", 14))
        self.__message.pack(pady=5)

        largeur = self.__n * self.__taille_case
        hauteur = self.__m * self.__taille_case
        self.__canevas = tk.Canvas(self.__fenetre, width=largeur, height=hauteur)
        self.__canevas.pack(padx=10, pady=10)
        self.__canevas.bind("<Button-1>", self.__sur_clic)

    def afficher(self) -> None:
        #Dessine le plateau, les marques et les deux pions.
        self.__canevas.delete("all")
        for ligne in range(self.__m):
            for colonne in range(self.__n):
                self.__dessiner_case(ligne, colonne)
        self.__fenetre.update_idletasks()

    def surligner(self, coups: list[tuple[int, int]]) -> None:
        """Met en évidence des cases du plateau.

        Paramètre : coups la liste des cases à surligner.
        """
        for ligne, colonne in coups:
            x1, y1, x2, y2 = self.__coordonnees(ligne, colonne)
            self.__canevas.create_rectangle(x1, y1, x2, y2, fill=COULEUR_SURLIGNAGE)
        self.__fenetre.update_idletasks()

    def attendre_clic(self) -> tuple[int, int]:
        #Bloque jusqu'au clic sur une case et renvoie (ligne, colonne).
        self.__attend_clic = True
        self.__fenetre.wait_variable(self.__attente)
        self.__attend_clic = False
        self.__verifier_fermeture()
        return self.__clic

    def afficher_message(self, texte: str) -> None:
        #Affiche un texte au dessus du plateau.
        self.__message.config(text=texte)
        self.__fenetre.update_idletasks()

    def pause(self, ms: int) -> None:
        #Attend un moment pour laisser voir le coup joué.
        self.__fenetre.after(ms, self.__reveiller)
        self.__fenetre.wait_variable(self.__attente)
        self.__verifier_fermeture()

    def attendre_fermeture(self) -> None:
        #Garde la fenêtre ouverte jusqu'à ce que l'utilisateur la ferme.
        self.__fenetre.mainloop()
        self.__fenetre.destroy()

    def __dessiner_case(self, ligne: int, colonne: int) -> None:
        #Dessine une case et le pion qu'elle contient.
        valeur = self.__jeu.get_case(ligne, colonne)
        if valeur == MARQUE:
            couleur = COULEUR_MARQUE
        else:
            couleur = COULEUR_VIDE

        x1, y1, x2, y2 = self.__coordonnees(ligne, colonne)
        self.__canevas.create_rectangle(x1, y1, x2, y2, fill=couleur)

        marge = self.__taille_case // 6
        if valeur == 1:
            self.__canevas.create_oval(x1 + marge, y1 + marge, x2 - marge, y2 - marge,
                                       fill=COULEUR_JOUEUR_1)
        elif valeur == 2:
            self.__canevas.create_oval(x1 + marge, y1 + marge, x2 - marge, y2 - marge,
                                       fill=COULEUR_JOUEUR_2)

    def __coordonnees(self, ligne: int, colonne: int) -> tuple[int, int, int, int]:
        #Renvoie les coins d'une case en pixels.
        x1 = colonne * self.__taille_case
        y1 = ligne * self.__taille_case
        return x1, y1, x1 + self.__taille_case, y1 + self.__taille_case

    def __sur_clic(self, evenement: tk.Event) -> None:
        #Enregistre la case cliquée si on attendait un clic.
        if not self.__attend_clic:
            return

        ligne = evenement.y // self.__taille_case
        colonne = evenement.x // self.__taille_case
        if 0 <= ligne < self.__m and 0 <= colonne < self.__n:
            self.__clic = (ligne, colonne)
            self.__reveiller()

    def __reveiller(self) -> None:
        #Débloque attendre_clic ou pause.
        self.__attente.set(self.__attente.get() + 1)

    def __fermer(self) -> None:
        #Note que l'utilisateur a fermé la fenêtre.
        self.__fermee = True
        self.__reveiller()
        self.__fenetre.quit()

    def __verifier_fermeture(self) -> None:
        #Arrête le programme si la fenêtre a été fermée pendant une attente.
        if self.__fermee:
            self.__fenetre.destroy()
            raise SystemExit
