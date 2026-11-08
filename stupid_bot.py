import random


class StupidBot:
    # Joue un coup legal au hasard.

    def __init__(self, jeu, numero):
        self.__jeu = jeu
        self.__numero = numero

    def nom(self):
        return "StupidBot"

    def proposer_coup(self):
        return random.choice(self.__jeu.mouvements(self.__numero))
