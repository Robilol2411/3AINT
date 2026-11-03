"""Bot qui joue au hasard pour Manic Minelayers."""

import random

from manic_minelayers import ManicMinelayers


class StupidBot:
 
    def __init__(self, jeu: ManicMinelayers, numero: int) -> None:
        
        self.__jeu = jeu
        self.__numero = numero

    def choisir_coup(self) -> tuple[int, int]:
        
        coups = self.__jeu.coups_possibles(self.__numero)
        return random.choice(coups)

    def get_nom(self) -> str:
      
        return "StupidBot"