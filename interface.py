import tkinter as tk

from constantes import (
    COULEUR_CASE_LIBRE, COULEUR_CASE_MARQUEE, COULEUR_CIBLE, COULEUR_DERNIER_COUP,
    COULEUR_PION_1, COULEUR_PION_2, HAUTEUR_MAX, LARGEUR_MAX, MARQUE,
)


class Interface:
    # Fenêtre Tkinter : affiche la partie et récupère les clics du joueur humain.

    def __init__(self, jeu):
        self.__jeu = jeu
        self.__cote = min(LARGEUR_MAX // jeu.nb_colonnes(), HAUTEUR_MAX // jeu.nb_lignes())
        self.__dernier_clic = None
        self.__clic_attendu = False
        self.__ferme = False
        self.__dernier_coup = None

        self.__racine = tk.Tk()
        self.__racine.title("Manic Minelayers")
        self.__racine.protocol("WM_DELETE_WINDOW", self.__fermer)
        # sert à bloquer le programme pendant une attente
        self.__reveil = tk.IntVar(self.__racine, 0)
        self.__bandeau = tk.Label(self.__racine, font=("Arial", 13))
        self.__bandeau.pack(pady=6)
        self.__toile = tk.Canvas(self.__racine,
                                 width=jeu.nb_colonnes() * self.__cote,
                                 height=jeu.nb_lignes() * self.__cote)
        self.__toile.pack(padx=8, pady=8)
        self.__toile.bind("<Button-1>", self.__sur_clic)

    def memoriser_dernier_coup(self, case):
        self.__dernier_coup = case

    def dessiner(self, cibles=()):
        # redessine le plateau ; les cases de 'cibles' sont surlignées
        self.__toile.delete("all")
        for l in range(self.__jeu.nb_lignes()):
            for c in range(self.__jeu.nb_colonnes()):
                self.__dessiner_case(l, c, (l, c) in cibles)
        self.__racine.update_idletasks()

    def message(self, texte):
        self.__bandeau.config(text=texte)
        self.__racine.update_idletasks()

    def attendre_case(self):
        # bloque jusqu'à un clic sur le plateau et renvoie (ligne, colonne)
        self.__clic_attendu = True
        self.__racine.wait_variable(self.__reveil)
        self.__clic_attendu = False
        self.__quitter_si_ferme()
        return self.__dernier_clic

    def temporiser(self, ms):
        # pause pour laisser voir le coup joué
        self.__racine.after(ms, self.__signaler)
        self.__racine.wait_variable(self.__reveil)
        self.__quitter_si_ferme()

    def garder_ouverte(self):
        self.__racine.mainloop()
        self.__racine.destroy()

    def __dessiner_case(self, l, c, cible):
        contenu = self.__jeu.contenu(l, c)
        if cible:
            fond = COULEUR_CIBLE
        elif (l, c) == self.__dernier_coup:
            fond = COULEUR_DERNIER_COUP
        elif contenu == MARQUE:
            fond = COULEUR_CASE_MARQUEE
        else:
            fond = COULEUR_CASE_LIBRE
        x = c * self.__cote
        y = l * self.__cote
        self.__toile.create_rectangle(x, y, x + self.__cote, y + self.__cote, fill=fond)
        if contenu == 1 or contenu == 2:
            if contenu == 1:
                couleur = COULEUR_PION_1
            else:
                couleur = COULEUR_PION_2
            marge = self.__cote // 7
            self.__toile.create_oval(x + marge, y + marge,
                                     x + self.__cote - marge, y + self.__cote - marge,
                                     fill=couleur)

    def __sur_clic(self, evenement):
        if not self.__clic_attendu:
            return
        l = evenement.y // self.__cote
        c = evenement.x // self.__cote
        if 0 <= l < self.__jeu.nb_lignes() and 0 <= c < self.__jeu.nb_colonnes():
            self.__dernier_clic = (l, c)
            self.__signaler()

    def __signaler(self):
        self.__reveil.set(self.__reveil.get() + 1)

    def __fermer(self):
        self.__ferme = True
        self.__signaler()
        self.__racine.quit()

    def __quitter_si_ferme(self):
        if self.__ferme:
            self.__racine.destroy()
            raise SystemExit
