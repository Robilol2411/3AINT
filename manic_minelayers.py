from constantes import DEPLACEMENTS_CAVALIER, M_DEFAUT, MARQUE, N_DEFAUT, VIDE


class ManicMinelayers:
    def __init__(self, m: int = M_DEFAUT, n: int = N_DEFAUT) -> None:
        #Crée un plateau vide, le joueur 1 commence.
        self.__m = m
        self.__n = n
        self.__plateau = []
        for _ in range(m):
            self.__plateau.append([VIDE] * n)
        # indice = numero du joueur, la case 0 ne sert pas
        self.__positions = [None, None, None]
        self.__joueur_courant = 1
        self.__historique = []
        self.__gagnant = None

    def get_m(self) -> int:
        #Renvoie le nombre de lignes
        return self.__m

    def get_n(self) -> int:
        #Renvoie le nombre de colonnes
        return self.__n

    def get_case(self, ligne: int, colonne: int) -> int:
        #Renvoie le contenu d'une case : VIDE, MARQUE, 1 ou 2.
        return self.__plateau[ligne][colonne]

    def get_plateau(self) -> list[list[int]]:
        #Renvoie une copie du plateau, jamais l'original.
        return self.__copie_plateau()

    def get_position(self, joueur: int) -> tuple[int, int] | None:
        #Renvoie la position du pion d'un joueur, None s'il n'est pas posé.
        return self.__positions[joueur]

    def get_joueur_courant(self) -> int:
        #Renvoie le numéro du joueur qui doit jouer.
        return self.__joueur_courant

    def get_adversaire(self, joueur: int) -> int:
        #Renvoie le numéro de l'autre joueur.
        if joueur == 1:
            return 2
        return 1

    def est_en_placement(self) -> bool:
        #Renvoie True tant que les deux pions ne sont pas posés.
        return self.__positions[1] is None or self.__positions[2] is None

    def coups_possibles(self, joueur: int | None = None) -> list[tuple[int, int]]:
        #Renvoie les coups d'un joueur sous forme de liste de tuples.
        if joueur is None:
            joueur = self.__joueur_courant
        if self.__positions[joueur] is None:
            return self.__cases_de_placement(joueur)
        return self.__sauts_possibles(joueur)

    def est_licite(self, coup: tuple[int, int]) -> bool:
        #Renvoie True si le coup est permis au joueur courant.
        return coup in self.coups_possibles()

    def jouer(self, coup: tuple[int, int]) -> None:
        #Joue un coup pour le joueur courant et passe la main.
        if not self.est_licite(coup):
            raise ValueError(f"Coup illégal : {coup}")

        joueur = self.__joueur_courant
        ancienne_pos = self.__positions[joueur]
        if ancienne_pos is not None:
            ancienne_ligne, ancienne_colonne = ancienne_pos
            self.__plateau[ancienne_ligne][ancienne_colonne] = MARQUE

        ligne, colonne = coup
        self.__plateau[ligne][colonne] = joueur
        self.__positions[joueur] = coup
        self.__historique.append((joueur, ancienne_pos, coup))
        self.__verifier_fin(joueur)
        self.__joueur_courant = self.get_adversaire(joueur)

    def annuler(self) -> None:
        if len(self.__historique) == 0:
            raise ValueError("Aucun coup à annuler")

        joueur, ancienne_pos, nouvelle_pos = self.__historique.pop()
        ligne, colonne = nouvelle_pos
        self.__plateau[ligne][colonne] = VIDE
        if ancienne_pos is not None:
            ancienne_ligne, ancienne_colonne = ancienne_pos
            self.__plateau[ancienne_ligne][ancienne_colonne] = joueur

        self.__positions[joueur] = ancienne_pos
        self.__joueur_courant = joueur
        # on ne peut pas jouer une partie finie, donc elle etait en cours
        self.__gagnant = None

    def copier(self) -> "ManicMinelayers":
        #Renvoie une copie indépendante de tout l'état du jeu.
        copie = ManicMinelayers(self.__m, self.__n)
        copie.__plateau = self.__copie_plateau()
        copie.__positions = self.__positions[:]
        copie.__joueur_courant = self.__joueur_courant
        copie.__historique = self.__historique[:]
        copie.__gagnant = self.__gagnant
        return copie

    def est_finie(self) -> bool:
        #Renvoie True si la partie est terminée.
        return self.__gagnant is not None

    def get_gagnant(self) -> int | None:
        #Renvoie 1 ou 2 pour le gagnant, 0 pour un nul, None si la partie continue.
        return self.__gagnant

    def __copie_plateau(self) -> list[list[int]]:
        #Renvoie une nouvelle liste de listes identique au plateau.
        copie = []
        for ligne in self.__plateau:
            copie.append(ligne[:])
        return copie

    def __cases_de_placement(self, joueur: int) -> list[tuple[int, int]]:
        #Renvoie les cases vides de la colonne de départ du joueur.
        if joueur == 1:
            colonne = 0
        else:
            colonne = self.__n - 1

        coups = []
        for ligne in range(self.__m):
            if self.__plateau[ligne][colonne] == VIDE:
                coups.append((ligne, colonne))
        return coups

    def __sauts_possibles(self, joueur: int) -> list[tuple[int, int]]:
        #Renvoie les sauts en L du joueur vers une case vide.
        ligne, colonne = self.__positions[joueur]
        coups = []
        for dl, dc in DEPLACEMENTS_CAVALIER:
            nouvelle_ligne = ligne + dl
            nouvelle_colonne = colonne + dc
            if 0 <= nouvelle_ligne < self.__m and 0 <= nouvelle_colonne < self.__n:
                if self.__plateau[nouvelle_ligne][nouvelle_colonne] == VIDE:
                    coups.append((nouvelle_ligne, nouvelle_colonne))
        return coups

    def __verifier_fin(self, joueur: int) -> None:
        #Met à jour le gagnant après un coup du joueur.
        adversaire = self.get_adversaire(joueur)
        if len(self.coups_possibles(adversaire)) > 0:
            return

        if len(self.coups_possibles(joueur)) > 0:
            self.__gagnant = joueur
        else:
            self.__gagnant = 0
