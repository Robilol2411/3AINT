"""Bot qui joue au hasard pour Manic Minelayers."""

import random

from manic_minelayers import ManicMinelayers


class StupidBot:
    """Joueur automatique qui joue complètement au hasard."""

    def __init__(self, jeu: ManicMinelayers, numero: int) -> None:
        """Crée le bot.

        :param jeu: la partie en cours
        :param numero: le numéro du joueur (1 ou 2)
        """
        self.__jeu = jeu
        self.__numero = numero

    def choisir_coup(self) -> tuple[int, int]:
        """Choisit un coup licite au hasard, sans le jouer.

        :return: un coup sous la forme (ligne, colonne)
        """
        coups = self.__jeu.coups_possibles(self.__numero)
        return random.choice(coups)

    def get_nom(self) -> str:
        """Renvoie le nom du bot.

        :return: le texte "StupidBot"
        """
        return "StupidBot"