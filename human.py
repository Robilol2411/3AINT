class Human:
    # Joueur humain : le coup est choisi par un clic sur une case surlignée.

    def __init__(self, jeu, numero, interface):
        self.__jeu = jeu
        self.__numero = numero
        self.__interface = interface

    def nom(self):
        return "Humain"

    def proposer_coup(self):
        permis = self.__jeu.mouvements(self.__numero)
        self.__interface.dessiner(permis)
        case = self.__interface.attendre_case()
        while case not in permis:
            case = self.__interface.attendre_case()
        return case
