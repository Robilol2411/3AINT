from constantes import M_DEFAUT, MARQUE, N_DEFAUT, SAUTS, VIDE


class ManicMinelayers:
    # Le moteur du jeu. Le plateau est une liste de lignes (listes de cases).
    # Tout est privé : on ne peut utiliser que les méthodes ci-dessous.

    def __init__(self, lignes=M_DEFAUT, colonnes=N_DEFAUT):
        self.__lignes = lignes
        self.__colonnes = colonnes
        self.__plateau = []
        for i in range(lignes):
            self.__plateau.append([VIDE] * colonnes)
        # pions[1] et pions[2] : position (ligne, colonne) ou None
        self.__pions = [None, None, None]
        self.__trait = 1
        self.__historique = []
        self.__vainqueur = None

    def nb_lignes(self):
        return self.__lignes

    def nb_colonnes(self):
        return self.__colonnes

    def contenu(self, ligne, colonne):
        # VIDE, MARQUE, 1 ou 2
        return self.__plateau[ligne][colonne]

    def grille(self):
        # copie du plateau (jamais l'original)
        copie = []
        for ligne in self.__plateau:
            copie.append(ligne[:])
        return copie

    def pion(self, joueur):
        return self.__pions[joueur]

    def trait(self):
        # numéro du joueur qui doit jouer
        return self.__trait

    def autre(self, joueur):
        if joueur == 1:
            return 2
        return 1

    def phase_placement(self):
        return self.__pions[1] is None or self.__pions[2] is None

    def nb_coups_joues(self):
        return len(self.__historique)

    def mouvements(self, joueur=None):
        # liste des coups possibles du joueur (par défaut celui qui a le trait)
        if joueur is None:
            joueur = self.__trait
        if self.__pions[joueur] is None:
            return self.__placements(joueur)
        return self.sauts_depuis(self.__pions[joueur])

    def sauts_depuis(self, case):
        # cases vides atteignables par un saut de cavalier depuis la case
        ligne, colonne = case
        coups = []
        for dl, dc in SAUTS:
            l = ligne + dl
            c = colonne + dc
            if 0 <= l < self.__lignes and 0 <= c < self.__colonnes:
                if self.__plateau[l][c] == VIDE:
                    coups.append((l, c))
        return coups

    def est_permis(self, coup):
        return not self.terminee() and coup in self.mouvements()

    def appliquer(self, coup):
        # joue le coup pour le joueur qui a le trait
        if not self.est_permis(coup):
            raise ValueError("Coup interdit : " + str(coup))
        joueur = self.__trait
        ancienne = self.__pions[joueur]
        if ancienne is not None:
            self.__plateau[ancienne[0]][ancienne[1]] = MARQUE
        self.__plateau[coup[0]][coup[1]] = joueur
        self.__pions[joueur] = coup
        self.__historique.append((joueur, ancienne, coup))
        self.__verifier_fin(joueur)
        self.__trait = self.autre(joueur)

    def retirer_dernier(self):
        # annule le dernier coup
        if len(self.__historique) == 0:
            raise ValueError("Aucun coup à retirer")
        joueur, ancienne, nouvelle = self.__historique.pop()
        self.__plateau[nouvelle[0]][nouvelle[1]] = VIDE
        if ancienne is not None:
            self.__plateau[ancienne[0]][ancienne[1]] = joueur
        self.__pions[joueur] = ancienne
        self.__trait = joueur
        self.__vainqueur = None

    def cloner(self):
        # copie indépendante de la partie
        copie = ManicMinelayers(self.__lignes, self.__colonnes)
        copie.__plateau = self.grille()
        copie.__pions = self.__pions[:]
        copie.__trait = self.__trait
        copie.__historique = self.__historique[:]
        copie.__vainqueur = self.__vainqueur
        return copie

    def terminee(self):
        return self.__vainqueur is not None

    def vainqueur(self):
        # 1 ou 2, 0 pour un nul, None si la partie continue
        return self.__vainqueur

    def __placements(self, joueur):
        if joueur == 1:
            colonne = 0
        else:
            colonne = self.__colonnes - 1
        coups = []
        for l in range(self.__lignes):
            if self.__plateau[l][colonne] == VIDE:
                coups.append((l, colonne))
        return coups

    def __verifier_fin(self, joueur):
        # si l'adversaire est bloqué : victoire si je peux encore bouger, sinon nul
        if len(self.mouvements(self.autre(joueur))) > 0:
            return
        if len(self.mouvements(joueur)) > 0:
            self.__vainqueur = joueur
        else:
            self.__vainqueur = 0
