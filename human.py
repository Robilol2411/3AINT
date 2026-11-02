from interface import Interface
from manic_minelayers import ManicMinelayers


class Human:
    def __init__(self, jeu: ManicMinelayers, numero: int, interface: Interface) -> None:
        #Crée le joueur.
        self.__jeu = jeu
        self.__numero = numero
        self.__interface = interface

    def choisir_coup(self) -> tuple[int, int]:
        #Surligne les coups possibles et renvoie la case cliquée, sans la jouer.
        coups = self.__jeu.coups_possibles()
        self.__interface.surligner(coups)
        coup = self.__interface.attendre_clic()
        while coup not in coups:
            coup = self.__interface.attendre_clic()
        return coup

    def get_nom(self) -> str:
        #Renvoie le nom du joueur.
        return "Humain"
